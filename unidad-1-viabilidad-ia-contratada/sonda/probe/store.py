"""Synthetic proposal store for the U1 feasibility probe.

Every record is synthetic and marked as such. Contact data lives in its own table and no
public method reads it: it exists only so tests can prove it never leaks.
"""

import json
import random
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path

SYNTHETIC_MARK = "SINTETICO"
IN_SCOPE_CALL = "convocatoria-sonda"
OUT_OF_SCOPE_CALL = "convocatoria-fuera-de-alcance"
RESULTS = ("preseleccionada", "no_preseleccionada", "duda")

_TOPICS = [
    "un episodio sobre historia de la ciencia", "una serie de entrevistas a oyentes",
    "un taller en vivo de edición de audio", "un debate sobre hábitos de lectura",
    "una sección de preguntas de la audiencia", "un especial sobre música independiente",
    "una guía de herramientas gratuitas", "un recorrido por proyectos comunitarios",
    "una charla sobre divulgación responsable", "un reto semanal de escritura",
]
_REASONS = [
    "conecta con temas ya tratados en el canal", "suma voces que no suelen aparecer",
    "puede producirse con pocos recursos", "responde a dudas frecuentes del chat",
    "permite participación en directo",
]
_EXAMPLES = [
    "Un bloque de quince minutos con dos invitados.", "Tres preguntas enviadas antes del vivo.",
    "Una demostración paso a paso con material libre.", "", "Una lista breve de fuentes para seguir.",
]

_SCHEMA = """
CREATE TABLE IF NOT EXISTS proposals (
    id TEXT PRIMARY KEY, call_id TEXT NOT NULL, what TEXT NOT NULL, why TEXT NOT NULL,
    example TEXT NOT NULL, received_at TEXT NOT NULL, synthetic TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS contacts (
    proposal_id TEXT PRIMARY KEY REFERENCES proposals(id), email TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS evaluations (
    id INTEGER PRIMARY KEY AUTOINCREMENT, proposal_id TEXT NOT NULL REFERENCES proposals(id),
    result TEXT NOT NULL, reasons TEXT NOT NULL, doubts TEXT NOT NULL, saved_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS calls (
    id INTEGER PRIMARY KEY AUTOINCREMENT, tool TEXT NOT NULL, arguments TEXT NOT NULL,
    ok INTEGER NOT NULL, at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT, at TEXT NOT NULL, kind TEXT NOT NULL,
    method TEXT NOT NULL DEFAULT '', path_ok INTEGER NOT NULL DEFAULT 0,
    status INTEGER NOT NULL DEFAULT 0, rpc TEXT NOT NULL DEFAULT '', host TEXT NOT NULL DEFAULT '',
    origin TEXT NOT NULL DEFAULT '', user_agent TEXT NOT NULL DEFAULT '', note TEXT NOT NULL DEFAULT '');
"""

_PUBLIC_COLUMNS = "id, call_id, what, why, example, received_at, synthetic"


class NotInScopeError(LookupError):
    """The requested proposal does not exist inside the call exposed by the probe."""


def generate_dataset(in_scope: int = 100, out_of_scope: int = 3, seed: int = 20260910) -> dict:
    rng = random.Random(seed)
    start = datetime(2026, 9, 1, 12, 0, tzinfo=timezone.utc)
    proposals, contacts = [], []

    def add(prefix: str, number: int, call_id: str) -> None:
        pid = f"{prefix}-{number:03d}"
        proposals.append({
            "id": pid,
            "call_id": call_id,
            "what": f"[{SYNTHETIC_MARK}] Propongo {rng.choice(_TOPICS)}.",
            "why": f"Aporta porque {rng.choice(_REASONS)}.",
            "example": rng.choice(_EXAMPLES),
            "received_at": (start + timedelta(minutes=37 * len(proposals))).isoformat(),
            "synthetic": SYNTHETIC_MARK,
        })
        contacts.append({"proposal_id": pid, "email": f"{pid.lower()}.{SYNTHETIC_MARK.lower()}@example.invalid"})

    for n in range(1, in_scope + 1):
        add("P", n, IN_SCOPE_CALL)
    for n in range(1, out_of_scope + 1):
        add("X", n, OUT_OF_SCOPE_CALL)
    return {"proposals": proposals, "contacts": contacts}


class Store:
    def __init__(self, path: Path | str):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self._db = sqlite3.connect(str(path), check_same_thread=False)
        self._db.row_factory = sqlite3.Row
        self._db.executescript(_SCHEMA)

    def close(self) -> None:
        self._db.close()

    def seed(self, dataset: dict) -> None:
        with self._db:
            self._db.executemany(
                f"INSERT OR IGNORE INTO proposals ({_PUBLIC_COLUMNS}) "
                "VALUES (:id, :call_id, :what, :why, :example, :received_at, :synthetic)",
                dataset["proposals"],
            )
            self._db.executemany(
                "INSERT OR IGNORE INTO contacts (proposal_id, email) VALUES (:proposal_id, :email)",
                dataset["contacts"],
            )

    def list_proposals(self, call_id: str, cursor: str | None, limit: int) -> dict:
        limit = max(1, min(limit, 100))
        rows = self._db.execute(
            "SELECT id, what, received_at, synthetic FROM proposals "
            "WHERE call_id = ? AND id > ? ORDER BY id LIMIT ?",
            (call_id, cursor or "", limit + 1),
        ).fetchall()
        items = [dict(r) for r in rows[:limit]]
        next_cursor = items[-1]["id"] if len(rows) > limit else None
        return {"items": items, "next_cursor": next_cursor}

    def get_proposal(self, call_id: str, proposal_id: str) -> dict:
        row = self._db.execute(
            f"SELECT {_PUBLIC_COLUMNS} FROM proposals WHERE call_id = ? AND id = ?",
            (call_id, proposal_id),
        ).fetchone()
        if row is None:
            raise NotInScopeError("La propuesta solicitada no está disponible en esta convocatoria.")
        return dict(row)

    def save_evaluation(self, call_id: str, proposal_id: str, result: str, reasons: str, doubts: str) -> dict:
        if result not in RESULTS:
            raise ValueError(f"result debe ser uno de {RESULTS}")
        self.get_proposal(call_id, proposal_id)
        saved_at = datetime.now(timezone.utc).isoformat()
        with self._db:
            cur = self._db.execute(
                "INSERT INTO evaluations (proposal_id, result, reasons, doubts, saved_at) VALUES (?, ?, ?, ?, ?)",
                (proposal_id, result, reasons, doubts, saved_at),
            )
        return {"id": cur.lastrowid, "proposal_id": proposal_id, "result": result,
                "reasons": reasons, "doubts": doubts, "saved_at": saved_at}

    def get_evaluations(self, call_id: str, proposal_id: str) -> list[dict]:
        self.get_proposal(call_id, proposal_id)
        rows = self._db.execute(
            "SELECT id, proposal_id, result, reasons, doubts, saved_at FROM evaluations "
            "WHERE proposal_id = ? ORDER BY id",
            (proposal_id,),
        ).fetchall()
        return [dict(r) for r in rows]

    def all_evaluations(self) -> list[dict]:
        rows = self._db.execute(
            "SELECT id, proposal_id, result, reasons, doubts, saved_at FROM evaluations ORDER BY id"
        ).fetchall()
        return [dict(r) for r in rows]

    def log_call(self, tool: str, arguments: dict, ok: bool) -> None:
        with self._db:
            self._db.execute(
                "INSERT INTO calls (tool, arguments, ok, at) VALUES (?, ?, ?, ?)",
                (tool, json.dumps(arguments, ensure_ascii=False, sort_keys=True), int(ok),
                 datetime.now(timezone.utc).isoformat()),
            )

    def all_calls(self) -> list[dict]:
        rows = self._db.execute("SELECT id, tool, arguments, ok, at FROM calls ORDER BY id").fetchall()
        return [{**dict(r), "arguments": json.loads(r["arguments"]), "ok": bool(r["ok"])} for r in rows]

    def log_request(self, method: str, path_ok: bool, status: int, rpc: str,
                    host: str, origin: str, user_agent: str) -> None:
        """Record one HTTP request. The request path is never stored: it may contain the token."""
        with self._db:
            self._db.execute(
                "INSERT INTO requests (at, kind, method, path_ok, status, rpc, host, origin, user_agent) "
                "VALUES (?, 'http', ?, ?, ?, ?, ?, ?, ?)",
                (datetime.now(timezone.utc).isoformat(), method, int(path_ok), status, rpc, host, origin, user_agent),
            )

    def log_marker(self, note: str) -> None:
        with self._db:
            self._db.execute("INSERT INTO requests (at, kind, note) VALUES (?, 'marker', ?)",
                             (datetime.now(timezone.utc).isoformat(), note))

    def all_requests(self) -> list[dict]:
        rows = self._db.execute("SELECT * FROM requests ORDER BY id").fetchall()
        return [{**dict(r), "path_ok": bool(r["path_ok"])} for r in rows]
