"""Storage of the circuit.

Three shapes in here are deliberate and carry properties the manifest requires:

* the original proposal is written once and never updated; every later text is a row in
  ``records`` that points at it and carries its own author and kind;
* contact data lives in its own table and no method that feeds a public surface or a model
  reads it, so separation is structural instead of a filter applied at presentation time;
* every operation that publishes or invites goes through ``_run_once``, so a retry with the
  same operation id returns the first result instead of acting twice.
"""

import json
import secrets
import sqlite3
from pathlib import Path

from circuit import domain

_SCHEMA = """
CREATE TABLE IF NOT EXISTS channels (
    id TEXT PRIMARY KEY, kind TEXT NOT NULL, title TEXT NOT NULL, question TEXT NOT NULL,
    restrictions TEXT NOT NULL, criteria TEXT NOT NULL, selected_count INTEGER NOT NULL,
    max_votes INTEGER NOT NULL, opens_at TEXT NOT NULL, closes_at TEXT,
    status TEXT NOT NULL DEFAULT 'preparacion');
CREATE TABLE IF NOT EXISTS proposals (
    id TEXT PRIMARY KEY, channel_id TEXT NOT NULL REFERENCES channels(id), what TEXT NOT NULL,
    why TEXT NOT NULL, example TEXT NOT NULL, author TEXT NOT NULL, received_at TEXT NOT NULL,
    synthetic TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS contacts (
    proposal_id TEXT PRIMARY KEY REFERENCES proposals(id), contact TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS rounds (
    id TEXT PRIMARY KEY, channel_id TEXT NOT NULL REFERENCES channels(id), cut_at TEXT NOT NULL,
    previous_cut_at TEXT, criteria TEXT NOT NULL, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS records (
    id TEXT PRIMARY KEY, proposal_id TEXT NOT NULL REFERENCES proposals(id), kind TEXT NOT NULL,
    author TEXT NOT NULL, body TEXT NOT NULL, created_at TEXT NOT NULL, invitation_id TEXT);
CREATE TABLE IF NOT EXISTS evaluations (
    id INTEGER PRIMARY KEY AUTOINCREMENT, round_id TEXT NOT NULL REFERENCES rounds(id),
    proposal_id TEXT NOT NULL REFERENCES proposals(id), stage INTEGER NOT NULL, result TEXT NOT NULL,
    reasons TEXT NOT NULL, doubts TEXT NOT NULL, evaluator TEXT NOT NULL, saved_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS invitations (
    id TEXT PRIMARY KEY, round_id TEXT NOT NULL REFERENCES rounds(id),
    proposal_id TEXT NOT NULL REFERENCES proposals(id), question TEXT NOT NULL,
    witness TEXT NOT NULL UNIQUE, created_at TEXT NOT NULL, answered_at TEXT);
CREATE TABLE IF NOT EXISTS authorizations (
    round_id TEXT NOT NULL REFERENCES rounds(id), kind TEXT NOT NULL, granted_at TEXT NOT NULL,
    PRIMARY KEY (round_id, kind));
CREATE TABLE IF NOT EXISTS publications (
    round_id TEXT NOT NULL REFERENCES rounds(id), proposal_id TEXT NOT NULL REFERENCES proposals(id),
    published_at TEXT NOT NULL, PRIMARY KEY (round_id, proposal_id));
CREATE TABLE IF NOT EXISTS creator_choices (
    round_id TEXT NOT NULL REFERENCES rounds(id), proposal_id TEXT NOT NULL REFERENCES proposals(id),
    chosen_at TEXT NOT NULL, PRIMARY KEY (round_id, proposal_id));
CREATE TABLE IF NOT EXISTS votes (
    round_id TEXT NOT NULL REFERENCES rounds(id), proposal_id TEXT NOT NULL REFERENCES proposals(id),
    voter TEXT NOT NULL, voted_at TEXT NOT NULL, PRIMARY KEY (round_id, proposal_id, voter));
CREATE TABLE IF NOT EXISTS calibrations (
    channel_id TEXT PRIMARY KEY REFERENCES channels(id), interpretation TEXT NOT NULL,
    examples TEXT NOT NULL, reviewed_at TEXT, correction TEXT NOT NULL DEFAULT '');
CREATE TABLE IF NOT EXISTS operations (
    operation_id TEXT PRIMARY KEY, kind TEXT NOT NULL, result TEXT NOT NULL, at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS calls (
    id INTEGER PRIMARY KEY AUTOINCREMENT, tool TEXT NOT NULL, arguments TEXT NOT NULL,
    ok INTEGER NOT NULL, at TEXT NOT NULL, original_fp TEXT NOT NULL DEFAULT '');
CREATE TABLE IF NOT EXISTS requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT, at TEXT NOT NULL, kind TEXT NOT NULL,
    method TEXT NOT NULL DEFAULT '', surface TEXT NOT NULL DEFAULT '', path_ok INTEGER NOT NULL DEFAULT 0,
    status INTEGER NOT NULL DEFAULT 0, rpc TEXT NOT NULL DEFAULT '', host TEXT NOT NULL DEFAULT '',
    origin TEXT NOT NULL DEFAULT '', user_agent TEXT NOT NULL DEFAULT '', note TEXT NOT NULL DEFAULT '');
"""

_PROPOSAL_COLUMNS = "id, channel_id, what, why, example, author, received_at, synthetic"


class NotFoundError(LookupError):
    """The requested record does not exist."""


class ClosedChannelError(ValueError):
    """The reception channel is not accepting proposals."""


class NotAuthorizedError(PermissionError):
    """The creator has not authorized this consequential action for this round."""


class VoteRefused(ValueError):
    """The vote breaks the rules of the round: not published, repeated or over the maximum."""


class Store:
    def __init__(self, path: Path | str):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self._db = sqlite3.connect(str(path), check_same_thread=False)
        self._db.row_factory = sqlite3.Row
        self._db.execute("PRAGMA foreign_keys = ON")
        self._db.executescript(_SCHEMA)

    def close(self) -> None:
        self._db.close()

    # ---------------------------------------------------------------- channels and criteria

    def create_channel(self, channel_id: str, kind: str, title: str, question: str,
                       restrictions: str, criteria: str, selected_count: int, opens_at: str,
                       closes_at: str | None, max_votes: int = domain.DEFAULT_MAX_VOTES) -> dict:
        """Create a reception channel. It is born closed to participation.

        Opening it is not part of creating it: the manifest puts the creator's review of the
        interpretation of their criteria *before* the call opens, so the only way out of
        `preparacion` is ``approve_calibration``.
        """
        if kind not in domain.CHANNEL_KINDS:
            raise ValueError(f"kind debe ser uno de {domain.CHANNEL_KINDS}")
        if kind == "convocatoria" and not closes_at:
            raise ValueError("Una convocatoria delimitada necesita fecha de cierre.")
        with self._db:
            self._db.execute(
                "INSERT INTO channels (id, kind, title, question, restrictions, criteria, "
                "selected_count, max_votes, opens_at, closes_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (channel_id, kind, title, question, restrictions, criteria, selected_count,
                 max_votes, opens_at, closes_at))
        return self.get_channel(channel_id)

    def get_channel(self, channel_id: str) -> dict:
        row = self._db.execute("SELECT * FROM channels WHERE id = ?", (channel_id,)).fetchone()
        if row is None:
            raise NotFoundError(f"No existe el canal de recepción {channel_id}.")
        return dict(row)

    def open_channels(self) -> list[dict]:
        """Channels that accept proposals right now. The public guide only offers these."""
        rows = self._db.execute(
            "SELECT * FROM channels WHERE status = 'abierta' ORDER BY id").fetchall()
        return [dict(r) for r in rows]

    def all_channels(self) -> list[dict]:
        """Every channel, open or closed. A closed call keeps its rounds and its finalists."""
        rows = self._db.execute("SELECT * FROM channels ORDER BY id").fetchall()
        return [dict(r) for r in rows]

    def close_channel(self, channel_id: str, at: str) -> dict:
        self.get_channel(channel_id)
        with self._db:
            self._db.execute("UPDATE channels SET status = 'cerrada' WHERE id = ?", (channel_id,))
        return self.get_channel(channel_id)

    def update_channel_criteria(self, channel_id: str, **fields) -> dict:
        allowed = {"question", "restrictions", "criteria", "selected_count", "max_votes", "title"}
        unknown = set(fields) - allowed
        if unknown:
            raise ValueError(f"Campos no configurables: {sorted(unknown)}")
        self.get_channel(channel_id)
        with self._db:
            for name, value in fields.items():
                self._db.execute(f"UPDATE channels SET {name} = ? WHERE id = ?", (value, channel_id))
        return self.get_channel(channel_id)

    def save_calibration(self, channel_id: str, interpretation: str, examples: list[dict]) -> dict:
        """Record the interpretation of the criteria and its explained examples, for review.

        Only while the channel is still in preparation: once it is open, its criteria are what
        participants read, and reinterpreting them mid-flight is the reevaluation problem that
        belongs to the next unit.
        """
        channel = self.get_channel(channel_id)
        if channel["status"] != "preparacion":
            raise ClosedChannelError(
                f"El canal {channel_id} ya está {channel['status']}: su calibración se revisó "
                "antes de abrirlo y no se reinterpreta ahora.")
        with self._db:
            self._db.execute(
                "INSERT INTO calibrations (channel_id, interpretation, examples) VALUES (?, ?, ?) "
                # A new interpretation is never approved by arriving, and it does not erase the
                # discrepancy the creator wrote: that stays as evidence of what was corrected.
                "ON CONFLICT(channel_id) DO UPDATE SET interpretation = excluded.interpretation, "
                "examples = excluded.examples, reviewed_at = NULL",
                (channel_id, interpretation, json.dumps(examples, ensure_ascii=False)))
        return self.get_calibration(channel_id)

    def approve_calibration(self, channel_id: str, at: str) -> dict:
        """The creator approves the interpretation of their criteria, and that opens the channel.

        Approving and opening are the same act on purpose: it makes the property of the plan
        structural instead of a rule somebody has to remember. A channel is open if and only if
        its calibration was approved, and the state cannot say otherwise.
        """
        channel = self.get_channel(channel_id)
        if channel["status"] != "preparacion":
            raise ClosedChannelError(f"El canal {channel_id} ya está {channel['status']}.")
        self.get_calibration(channel_id)
        with self._db:
            self._db.execute("UPDATE calibrations SET reviewed_at = ? WHERE channel_id = ?",
                             (at, channel_id))
            self._db.execute("UPDATE channels SET status = 'abierta', opens_at = ? WHERE id = ?",
                             (at, channel_id))
        return self.get_channel(channel_id)

    def return_calibration(self, channel_id: str, at: str, correction: str) -> dict:
        """The creator returns the interpretation with a discrepancy, and the channel stays shut.

        The correction is recorded next to the interpretation it corrects; it is never a silent
        overwrite of the criteria, and it does not open anything.
        """
        if not correction.strip():
            raise ValueError("Devolver la calibración exige escribir la discrepancia.")
        self.get_calibration(channel_id)
        with self._db:
            self._db.execute(
                "UPDATE calibrations SET reviewed_at = NULL, correction = ? WHERE channel_id = ?",
                (correction.strip(), channel_id))
        return self.get_calibration(channel_id)

    def get_calibration(self, channel_id: str) -> dict:
        row = self._db.execute(
            "SELECT * FROM calibrations WHERE channel_id = ?", (channel_id,)).fetchone()
        if row is None:
            raise NotFoundError(f"El canal {channel_id} todavía no tiene calibración.")
        return {**dict(row), "examples": json.loads(row["examples"])}

    # ---------------------------------------------------------------------------- reception

    def receive_proposal(self, submission: dict, at: str) -> dict:
        channel = self.get_channel(submission["channel_id"])
        if channel["status"] != "abierta":
            raise ClosedChannelError(self._closed_message(channel))
        if channel["closes_at"] and at > channel["closes_at"]:
            raise ClosedChannelError(self._closed_message(channel))

        clean = domain.validate_submission(submission)
        proposal_id = self._next_proposal_id()
        row = {"id": proposal_id, "channel_id": channel["id"], "what": clean["what"],
               "why": clean["why"], "example": clean["example"], "author": clean["author"],
               "received_at": at, "synthetic": domain.SYNTHETIC_MARK}
        with self._db:
            self._db.execute(
                f"INSERT INTO proposals ({_PROPOSAL_COLUMNS}) VALUES "
                "(:id, :channel_id, :what, :why, :example, :author, :received_at, :synthetic)", row)
            self._db.execute("INSERT INTO contacts (proposal_id, contact) VALUES (?, ?)",
                             (proposal_id, clean["contact"]))
        return row

    def _closed_message(self, channel: dict) -> str:
        if channel["status"] == "preparacion":
            message = (f"«{channel['title']}» todavía no está abierta: el creador no revisó aún "
                       "la interpretación de sus criterios.")
        else:
            message = f"La convocatoria «{channel['title']}» está cerrada y no recibe propuestas."
        permanent = [c for c in self.open_channels() if c["kind"] == "permanente"]
        if permanent:
            message += (f" El canal permanente «{permanent[0]['title']}» sigue abierto: podés "
                        f"enviarla ahí ({permanent[0]['id']}). Nada se reasigna automáticamente.")
        return message

    def _next_proposal_id(self) -> str:
        count = self._db.execute("SELECT COUNT(*) AS n FROM proposals").fetchone()["n"]
        return f"P-{count + 1:03d}"

    def get_proposal(self, proposal_id: str) -> dict:
        row = self._db.execute(
            f"SELECT {_PROPOSAL_COLUMNS} FROM proposals WHERE id = ?", (proposal_id,)).fetchone()
        if row is None:
            raise NotFoundError(f"No existe la propuesta {proposal_id}.")
        return dict(row)

    def list_proposals(self, channel_id: str, cursor: str | None = None, limit: int = 50) -> dict:
        limit = max(1, min(limit, 100))
        rows = self._db.execute(
            "SELECT id, what, author, received_at, synthetic FROM proposals "
            "WHERE channel_id = ? AND id > ? ORDER BY id LIMIT ?",
            (channel_id, cursor or "", limit + 1)).fetchall()
        items = [dict(r) for r in rows[:limit]]
        return {"items": items, "next_cursor": items[-1]["id"] if len(rows) > limit else None}

    def contact_of(self, proposal_id: str) -> str:
        """Read one contact. Only invitation delivery may call this, and it never reaches a model."""
        row = self._db.execute(
            "SELECT contact FROM contacts WHERE proposal_id = ?", (proposal_id,)).fetchone()
        if row is None:
            raise NotFoundError(f"No hay contacto para {proposal_id}.")
        return row["contact"]

    # -------------------------------------------------------------------------------- rounds

    def open_round(self, channel_id: str, cut_at: str) -> dict:
        """Cut the channel: freeze the criteria in force and fix the set of proposals.

        Cutting a delimited call is what closes it: the plan defines a round as the closing of a
        call or a cut of the permanent channel, so a call cannot stay open past its own round.
        The permanent channel stays open and its next proposals fall into the next cut.
        """
        channel = self.get_channel(channel_id)
        if channel["status"] != "abierta":
            raise ClosedChannelError(
                f"El canal {channel_id} está {channel['status']} y no tiene una ronda para cortar.")
        previous = self._db.execute(
            "SELECT cut_at FROM rounds WHERE channel_id = ? ORDER BY cut_at DESC LIMIT 1",
            (channel_id,)).fetchone()
        criteria = {key: channel[key] for key in
                    ("title", "question", "restrictions", "criteria", "selected_count", "max_votes")}
        number = self._db.execute(
            "SELECT COUNT(*) AS n FROM rounds WHERE channel_id = ?", (channel_id,)).fetchone()["n"] + 1
        round_id = f"{channel_id}:ronda-{number}"
        with self._db:
            self._db.execute(
                "INSERT INTO rounds (id, channel_id, cut_at, previous_cut_at, criteria, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (round_id, channel_id, cut_at, previous["cut_at"] if previous else None,
                 json.dumps(criteria, ensure_ascii=False), cut_at))
            if channel["kind"] == "convocatoria":
                self._db.execute("UPDATE channels SET status = 'cerrada' WHERE id = ?", (channel_id,))
        return self.get_round(round_id)

    def get_round(self, round_id: str) -> dict:
        row = self._db.execute("SELECT * FROM rounds WHERE id = ?", (round_id,)).fetchone()
        if row is None:
            raise NotFoundError(f"No existe la ronda {round_id}.")
        return {**dict(row), "criteria": json.loads(row["criteria"])}

    def rounds_of(self, channel_id: str) -> list[dict]:
        rows = self._db.execute(
            "SELECT id FROM rounds WHERE channel_id = ? ORDER BY cut_at", (channel_id,)).fetchall()
        return [self.get_round(r["id"]) for r in rows]

    def round_proposals(self, round_id: str) -> list[dict]:
        round_ = self.get_round(round_id)
        rows = self._db.execute(
            f"SELECT {_PROPOSAL_COLUMNS} FROM proposals WHERE channel_id = ?",
            (round_["channel_id"],)).fetchall()
        return domain.round_membership([dict(r) for r in rows], round_["channel_id"],
                                       round_["cut_at"], round_["previous_cut_at"])

    # --------------------------------------------------------------------------- evaluation

    def save_evaluation(self, round_id: str, proposal_id: str, stage: int, result: str,
                        reasons: str, doubts: str, evaluator: str, at: str) -> dict:
        if result not in domain.EVALUATION_RESULTS:
            raise ValueError(f"result debe ser uno de {domain.EVALUATION_RESULTS}")
        if stage not in (1, 2):
            raise ValueError("stage debe ser 1 (primera evaluación) o 2 (segunda evaluación)")
        if not evaluator:
            raise ValueError("Toda evaluación registra quién la produjo.")
        self._require_in_round(round_id, proposal_id)
        with self._db:
            cur = self._db.execute(
                "INSERT INTO evaluations (round_id, proposal_id, stage, result, reasons, doubts, "
                "evaluator, saved_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (round_id, proposal_id, stage, result, reasons, doubts, evaluator, at))
        return {"id": cur.lastrowid, "round_id": round_id, "proposal_id": proposal_id,
                "stage": stage, "result": result, "reasons": reasons, "doubts": doubts,
                "evaluator": evaluator, "saved_at": at}

    def evaluations_of(self, round_id: str, proposal_id: str | None = None) -> list[dict]:
        sql = ("SELECT id, round_id, proposal_id, stage, result, reasons, doubts, evaluator, "
               "saved_at FROM evaluations WHERE round_id = ?")
        params: tuple = (round_id,)
        if proposal_id:
            sql += " AND proposal_id = ?"
            params += (proposal_id,)
        return [dict(r) for r in self._db.execute(sql + " ORDER BY id", params).fetchall()]

    def evaluation_material(self, round_id: str, proposal_id: str) -> dict:
        """Everything the evaluator may see about one proposal: the original and its records.

        The contact is not part of it, and neither is any text the participant did not write.
        """
        self._require_in_round(round_id, proposal_id)
        return {"original": self.get_proposal(proposal_id),
                "records": self.records_of(proposal_id),
                "criteria": self.get_round(round_id)["criteria"]}

    def preselected(self, round_id: str) -> list[str]:
        """Proposals whose latest evaluation in the round preselected them."""
        latest: dict[str, str] = {}
        for evaluation in self.evaluations_of(round_id):
            latest[evaluation["proposal_id"]] = evaluation["result"]
        return [pid for pid, result in sorted(latest.items()) if result == "preseleccionada"]

    # ------------------------------------------------------------ invitations and extensions

    def authorize(self, round_id: str, kind: str, at: str) -> dict:
        """Record the creator's authorization for a consequential action of this round."""
        if kind not in ("invitar", "publicar"):
            raise ValueError("kind debe ser 'invitar' o 'publicar'")
        self.get_round(round_id)
        with self._db:
            self._db.execute(
                "INSERT OR IGNORE INTO authorizations (round_id, kind, granted_at) VALUES (?, ?, ?)",
                (round_id, kind, at))
        return {"round_id": round_id, "kind": kind, "granted_at": at}

    def is_authorized(self, round_id: str, kind: str) -> bool:
        row = self._db.execute(
            "SELECT 1 FROM authorizations WHERE round_id = ? AND kind = ?", (round_id, kind)).fetchone()
        return row is not None

    def _require_authorization(self, round_id: str, kind: str) -> None:
        if not self.is_authorized(round_id, kind):
            raise NotAuthorizedError(
                f"La ronda {round_id} no tiene autorización del creador para {kind}. "
                "El sistema no ejecuta la acción y no cambia nada.")

    def prepare_invitation(self, round_id: str, proposal_id: str, question: str,
                           operation_id: str, at: str) -> dict:
        """Create the invitation and its witness link. Delivering it is a separate decision.

        The witness is issued by the system and is the only thing the participant needs: the
        link by itself identifies the proposal and its author, so nothing depends on the
        participant transcribing a code or a subject line correctly.
        """
        self._require_authorization(round_id, "invitar")
        self._require_in_round(round_id, proposal_id)

        def create() -> dict:
            invitation_id = f"INV-{secrets.token_hex(4)}"
            witness = secrets.token_urlsafe(24)
            with self._db:
                self._db.execute(
                    "INSERT INTO invitations (id, round_id, proposal_id, question, witness, created_at) "
                    "VALUES (?, ?, ?, ?, ?, ?)",
                    (invitation_id, round_id, proposal_id, question, witness, at))
            return {"id": invitation_id, "round_id": round_id, "proposal_id": proposal_id,
                    "question": question, "witness": witness, "created_at": at}

        return self._run_once(operation_id, "invitar", at, create)

    def invitations_of(self, round_id: str) -> list[dict]:
        rows = self._db.execute(
            "SELECT * FROM invitations WHERE round_id = ? ORDER BY created_at, id",
            (round_id,)).fetchall()
        return [dict(r) for r in rows]

    def invitation_by_witness(self, witness: str) -> dict:
        row = self._db.execute(
            "SELECT * FROM invitations WHERE witness = ?", (witness,)).fetchone()
        if row is None:
            raise NotFoundError("El enlace de ampliación no corresponde a ninguna invitación.")
        return dict(row)

    def add_record_from_invitation(self, witness: str, body: str, at: str,
                                   kind: str = "ampliacion_autor", author: str | None = None) -> dict:
        """Store an extension as a new record linked to the original, never as an overwrite."""
        if kind not in domain.RECORD_KINDS:
            raise ValueError(f"kind debe ser uno de {domain.RECORD_KINDS}")
        invitation = self.invitation_by_witness(witness)
        proposal = self.get_proposal(invitation["proposal_id"])
        record_id = f"REG-{secrets.token_hex(4)}"
        record = {"id": record_id, "proposal_id": proposal["id"], "kind": kind,
                  "author": author or proposal["author"], "body": body, "created_at": at,
                  "invitation_id": invitation["id"]}
        with self._db:
            self._db.execute(
                "INSERT INTO records (id, proposal_id, kind, author, body, created_at, invitation_id) "
                "VALUES (:id, :proposal_id, :kind, :author, :body, :created_at, :invitation_id)", record)
            self._db.execute("UPDATE invitations SET answered_at = ? WHERE id = ?",
                             (at, invitation["id"]))
        return record

    def records_of(self, proposal_id: str) -> list[dict]:
        rows = self._db.execute(
            "SELECT id, proposal_id, kind, author, body, created_at, invitation_id FROM records "
            "WHERE proposal_id = ? ORDER BY created_at, id", (proposal_id,)).fetchall()
        return [dict(r) for r in rows]

    # ------------------------------------------------------------- publication and the signals

    def set_creator_choice(self, round_id: str, proposal_ids: list[str], at: str) -> list[str]:
        self.get_round(round_id)
        with self._db:
            self._db.execute("DELETE FROM creator_choices WHERE round_id = ?", (round_id,))
            for proposal_id in dict.fromkeys(proposal_ids):
                self._require_in_round(round_id, proposal_id)
                self._db.execute(
                    "INSERT INTO creator_choices (round_id, proposal_id, chosen_at) VALUES (?, ?, ?)",
                    (round_id, proposal_id, at))
        return self.creator_choice(round_id)

    def creator_choice(self, round_id: str) -> list[str]:
        rows = self._db.execute(
            "SELECT proposal_id FROM creator_choices WHERE round_id = ? ORDER BY proposal_id",
            (round_id,)).fetchall()
        return [r["proposal_id"] for r in rows]

    def publish(self, round_id: str, proposal_ids: list[str], operation_id: str, at: str) -> dict:
        """Publish the finalists of a round. Refused without the creator's authorization."""
        self._require_authorization(round_id, "publicar")
        unique = list(dict.fromkeys(proposal_ids))
        for proposal_id in unique:
            self._require_in_round(round_id, proposal_id)

        def do_publish() -> dict:
            with self._db:
                for proposal_id in unique:
                    self._db.execute(
                        "INSERT OR IGNORE INTO publications (round_id, proposal_id, published_at) "
                        "VALUES (?, ?, ?)", (round_id, proposal_id, at))
            return {"round_id": round_id, "published": unique, "published_at": at}

        return self._run_once(operation_id, "publicar", at, do_publish)

    def is_published(self, round_id: str, proposal_id: str) -> bool:
        row = self._db.execute(
            "SELECT 1 FROM publications WHERE round_id = ? AND proposal_id = ?",
            (round_id, proposal_id)).fetchone()
        return row is not None

    def finalists(self, round_id: str) -> list[dict]:
        """The published list: publishable fields only, one entry per proposal."""
        rows = self._db.execute(
            f"SELECT p.id, p.channel_id, p.what, p.why, p.example, p.author, p.received_at, "
            "p.synthetic FROM publications pub JOIN proposals p ON p.id = pub.proposal_id "
            "WHERE pub.round_id = ? ORDER BY p.id", (round_id,)).fetchall()
        return [domain.public_projection(dict(r)) for r in rows]

    def published_rounds(self) -> list[str]:
        rows = self._db.execute(
            "SELECT DISTINCT round_id FROM publications ORDER BY round_id").fetchall()
        return [r["round_id"] for r in rows]

    def vote(self, round_id: str, proposal_id: str, voter: str, at: str) -> dict:
        """One vote of one participant for one published finalist of the round."""
        if not self.is_published(round_id, proposal_id):
            raise VoteRefused("Solo se vota sobre la lista publicada de finalistas.")
        already = self._db.execute(
            "SELECT proposal_id FROM votes WHERE round_id = ? AND voter = ?",
            (round_id, voter)).fetchall()
        if any(r["proposal_id"] == proposal_id for r in already):
            raise VoteRefused("Ya votaste esta propuesta en esta ronda.")
        maximum = self.get_round(round_id)["criteria"]["max_votes"]
        if len(already) >= maximum:
            raise VoteRefused(f"Alcanzaste el máximo de {maximum} votos de esta ronda.")
        with self._db:
            self._db.execute(
                "INSERT INTO votes (round_id, proposal_id, voter, voted_at) VALUES (?, ?, ?, ?)",
                (round_id, proposal_id, voter, at))
        return {"round_id": round_id, "proposal_id": proposal_id, "voted_at": at}

    def audience_preference(self, round_id: str) -> dict[str, int]:
        rows = self._db.execute(
            "SELECT proposal_id, COUNT(*) AS n FROM votes WHERE round_id = ? "
            "GROUP BY proposal_id ORDER BY proposal_id", (round_id,)).fetchall()
        return {r["proposal_id"]: r["n"] for r in rows}

    def signals(self, round_id: str) -> dict:
        """The three signals of the round, separate. Nothing here adds them up."""
        return domain.signals_view(ia=self.preselected(round_id),
                                   audiencia=self.audience_preference(round_id),
                                   creador=self.creator_choice(round_id))

    # ------------------------------------------------------------------------------ plumbing

    def _require_in_round(self, round_id: str, proposal_id: str) -> None:
        if proposal_id not in {p["id"] for p in self.round_proposals(round_id)}:
            raise NotFoundError(
                f"La propuesta {proposal_id} no pertenece a la ronda {round_id}.")

    def _run_once(self, operation_id: str, kind: str, at: str, action):
        """Idempotency by operation id: a retry returns the first result and acts once."""
        if not operation_id:
            raise ValueError("Toda operación consecuente necesita un identificador de operación.")
        row = self._db.execute(
            "SELECT result FROM operations WHERE operation_id = ?", (operation_id,)).fetchone()
        if row is not None:
            return json.loads(row["result"])
        result = action()
        with self._db:
            self._db.execute(
                "INSERT INTO operations (operation_id, kind, result, at) VALUES (?, ?, ?, ?)",
                (operation_id, kind, json.dumps(result, ensure_ascii=False), at))
        return result

    # ------------------------------------------------------------------- evidence of a run

    def all_evaluations(self) -> list[dict]:
        rows = self._db.execute(
            "SELECT id, round_id, proposal_id, stage, result, reasons, doubts, evaluator, "
            "saved_at FROM evaluations ORDER BY id").fetchall()
        return [dict(r) for r in rows]

    def all_invitations(self) -> list[dict]:
        """Invitations for the evidence. The witness never leaves: it would let anyone answer."""
        rows = self._db.execute(
            "SELECT id, round_id, proposal_id, question, witness, created_at, answered_at "
            "FROM invitations ORDER BY created_at, id").fetchall()
        return [{**{k: r[k] for k in r.keys() if k != "witness"},
                 "witness_fp": domain.fingerprint(r["witness"])} for r in rows]

    def witnesses(self) -> list[str]:
        """Every witness issued, in clear.

        It exists for one caller: the step that preserves an artefact and has to substitute the
        actionable secrets before writing. Nothing that answers a surface or a model reads it.
        """
        rows = self._db.execute("SELECT witness FROM invitations").fetchall()
        return [r["witness"] for r in rows]

    def all_records(self) -> list[dict]:
        rows = self._db.execute(
            "SELECT id, proposal_id, kind, author, body, created_at, invitation_id FROM records "
            "ORDER BY created_at, id").fetchall()
        return [dict(r) for r in rows]

    def all_votes(self) -> list[dict]:
        """Votes for the evidence. The voter mark is fingerprinted, not copied."""
        rows = self._db.execute(
            "SELECT round_id, proposal_id, voter, voted_at FROM votes ORDER BY voted_at").fetchall()
        return [{"round_id": r["round_id"], "proposal_id": r["proposal_id"],
                 "voter_fp": domain.fingerprint(r["voter"]), "voted_at": r["voted_at"]} for r in rows]

    def log_call(self, tool: str, arguments: dict, ok: bool, at: str, original_fp: str = "") -> None:
        with self._db:
            self._db.execute(
                "INSERT INTO calls (tool, arguments, ok, at, original_fp) VALUES (?, ?, ?, ?, ?)",
                (tool, json.dumps(arguments, ensure_ascii=False, sort_keys=True), int(ok), at,
                 original_fp))

    def all_calls(self) -> list[dict]:
        rows = self._db.execute(
            "SELECT id, tool, arguments, ok, at, original_fp FROM calls ORDER BY id").fetchall()
        return [{**dict(r), "arguments": json.loads(r["arguments"]), "ok": bool(r["ok"])} for r in rows]

    def log_request(self, at: str, surface: str, method: str, path_ok: bool, status: int,
                    rpc: str = "", host: str = "", origin: str = "", user_agent: str = "") -> None:
        """Record one HTTP request. The path is never stored: it may carry the capability."""
        with self._db:
            self._db.execute(
                "INSERT INTO requests (at, kind, surface, method, path_ok, status, rpc, host, origin, "
                "user_agent) VALUES (?, 'http', ?, ?, ?, ?, ?, ?, ?, ?)",
                (at, surface, method, int(path_ok), status, rpc, host, origin, user_agent))

    def log_marker(self, at: str, note: str) -> None:
        with self._db:
            self._db.execute("INSERT INTO requests (at, kind, note) VALUES (?, 'marker', ?)", (at, note))

    def all_requests(self) -> list[dict]:
        rows = self._db.execute("SELECT * FROM requests ORDER BY id").fetchall()
        return [{**dict(r), "path_ok": bool(r["path_ok"])} for r in rows]
