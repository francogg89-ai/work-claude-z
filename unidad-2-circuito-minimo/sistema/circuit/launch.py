"""Local command line to prepare, run and preserve a run of the circuit.

The capability is generated here and written under ``.data``, which is ignored by Git: no
secret enters the repository, the documentation or any material that gets distributed.
"""

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from circuit import access, domain, synthetic
from circuit.app import build_app, utc_now
from circuit.store import Store

DATA = Path(__file__).resolve().parent.parent / ".data"
DB = DATA / "circuito.sqlite"
CAPABILITY_FILE = DATA / "capacidad"


CONVOCATORIA = "convocatoria-1"
PERMANENTE = "permanente"


def calls_file() -> Path:
    """Where the body of every MCP call is preserved. Derived from DATA, never duplicated."""
    return DATA / "llamadas.jsonl"


def captures_dir() -> Path:
    return DATA / "capturas"


def sessions_dir() -> Path:
    return DATA / "sesiones"


_WITNESS_IN_URL = re.compile(r"/ampliar/[A-Za-z0-9_-]{16,}")


def redact(text: str) -> str:
    """Take the secrets out of anything that is going to be preserved and read later.

    Two things would let a reader of the evidence act in somebody else's name: the capability of
    the creator's surfaces and the witness of an invitation. Everything else is kept verbatim,
    and each substitution is visible as such.

    The witnesses are substituted **by value**, read from the store, so the substitution does
    not depend on recognising the shape they happen to travel in. The pattern over the link is
    kept as a second net, for a witness that this database does not know.
    """
    if CAPABILITY_FILE.exists():
        text = text.replace(capability(), "<capacidad>")
    for witness in _witnesses():
        text = text.replace(witness, "<testigo>")
    return _WITNESS_IN_URL.sub("/ampliar/<testigo>", text)


def _witnesses() -> list[str]:
    if not DB.exists():
        return []
    db = Store(DB)
    try:
        return db.witnesses()
    finally:
        db.close()


def _session(name: str) -> dict:
    path = sessions_dir() / f"{name}.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def _save_session(name: str, cookies: dict) -> None:
    sessions_dir().mkdir(parents=True, exist_ok=True)
    (sessions_dir() / f"{name}.json").write_text(json.dumps(cookies), encoding="utf-8")


def _preserve(name: str, response) -> int:
    folder = captures_dir()
    folder.mkdir(parents=True, exist_ok=True)
    destination = folder / f"{name}.html"
    destination.write_text(redact(response.text), encoding="utf-8")
    print(f"{response.status_code}  {response.headers.get('content-type', '')}  -> {destination}")
    return response.status_code


def capability() -> str:
    if not CAPABILITY_FILE.exists():
        DATA.mkdir(parents=True, exist_ok=True)
        CAPABILITY_FILE.write_text(access.new_capability(), encoding="utf-8")
    return access.check(CAPABILITY_FILE.read_text(encoding="utf-8").strip())


def store() -> Store:
    return Store(DB)


def cmd_init(args) -> int:
    db = store()
    db.create_channel(
        CONVOCATORIA, kind="convocatoria", title="Convocatoria de ejemplo",
        question="¿Qué tema querés que tratemos en profundidad?",
        restrictions="Una propuesta por persona. Sin contenido de terceros sin permiso.",
        criteria="Se valoran propuestas conectadas con el canal, concretas y realizables con "
                 "pocos recursos.",
        selected_count=args.seleccionadas, max_votes=args.votos, opens_at=utc_now(),
        closes_at=args.cierra)
    db.create_channel(
        PERMANENTE, kind="permanente", title="Buzón permanente",
        question="¿Qué te gustaría escuchar en el canal?",
        restrictions="Se evalúa por cortes, no por fecha de cierre.",
        criteria="Se valoran propuestas concretas y realizables.",
        selected_count=2, max_votes=args.votos, opens_at=utc_now(), closes_at=None)
    db.close()
    print(f"Base creada en {DB}")
    print("Los dos canales quedan en preparación: no reciben propuestas hasta que el creador "
          "apruebe en el panel la interpretación de sus criterios.")
    return cmd_enlaces(args)


def cmd_seed(args) -> int:
    db = store()
    for submission in synthetic.generate(args.canal, args.cantidad, start=args.desde):
        proposal = db.receive_proposal(submission, at=utc_now())
        print(f"{proposal['id']}  {proposal['what'][:60]}")
    db.close()
    return 0


def cmd_enlaces(args) -> int:
    base = args.base.rstrip("/")
    print(f"Guía y formulario público : {base}/")
    print(f"Portal de finalistas      : {base}/finalistas")
    print(f"Enlace de entrada del creador: {base}/entrada-creador")
    print(f"Panel del creador (privado)  : {base}{access.panel_path(capability())}")
    print(f"Conector MCP (privado)       : {base}{access.mcp_path(capability())}")
    print("El panel y el conector llevan la capacidad: no los pegues en material público.")
    return 0


def cmd_serve(args) -> int:
    import uvicorn

    db = store()
    app = build_app(db, capability(), public_base=args.base.rstrip("/"), exposed=args.expuesto)
    cmd_enlaces(args)
    uvicorn.run(app, host=args.host, port=args.puerto, log_level="info")
    db.close()
    return 0


def cmd_evaluar(args) -> int:
    """Run the local deterministic executor over a round.

    In a real operation the evaluator is the creator's AI through MCP. This command is the local
    executor of the frontier, and every evaluation it writes carries its name.
    """
    from circuit.evaluation import DeterministicEvaluator, evaluate_round

    db = store()
    for saved in evaluate_round(db, args.ronda, DeterministicEvaluator(), stage=args.etapa,
                                at=utc_now()):
        print(f"{saved['proposal_id']}  {saved['result']}  {saved['reasons']}")
    db.close()
    return 0


def cmd_llamar(args) -> int:
    """Call one MCP tool over HTTP, the same way a remote client would.

    The full body of every request and answer is appended to ``llamadas.jsonl``, with the
    secrets redacted. That file, and not the console, is what lets anyone check afterwards what
    each answer actually contained.
    """
    import httpx

    arguments = json.loads(args.argumentos)
    request = {"jsonrpc": "2.0", "id": 1, "method": "tools/call",
               "params": {"name": args.herramienta, "arguments": arguments}}
    response = httpx.post(f"{args.base.rstrip('/')}{access.mcp_path(capability())}", json=request,
                          headers={"Accept": "application/json, text/event-stream",
                                   "Content-Type": "application/json"}, timeout=30)
    try:
        body = response.json()
    except ValueError:
        body = {"texto": response.text}
    record = {"at": datetime.now(timezone.utc).isoformat(), "herramienta": args.herramienta,
              "argumentos": arguments, "status": response.status_code, "respuesta": body}
    destination = calls_file()
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("a", encoding="utf-8") as handle:
        handle.write(redact(json.dumps(record, ensure_ascii=False)) + "\n")
    print(response.status_code)
    print(json.dumps(body, ensure_ascii=False, indent=2))
    return 0 if response.status_code == 200 else 1


def cmd_capturar(args) -> int:
    """Save the exact bytes a surface answered to a GET, with the secrets redacted."""
    import httpx

    if args.nombre and len(args.ruta) != 1:
        raise SystemExit("--nombre solo se usa cuando se captura una sola ruta")
    base = args.base.rstrip("/")
    cookies = _session(args.sesion)
    for path in args.ruta:
        name = args.nombre or path.strip("/").replace("/", "-") or "guia"
        response = httpx.get(base + path, cookies=cookies, timeout=30)
        cookies.update(dict(response.cookies))
        _preserve(name, response)
    _save_session(args.sesion, cookies)
    return 0


def cmd_enviar(args) -> int:
    """Send a form the way a participant would, and preserve the answer, refusals included.

    The session keeps the cookies between calls, which is what makes a sequence of votes by the
    same participant reproducible instead of a new participant each time.
    """
    import httpx

    base = args.base.rstrip("/")
    cookies = _session(args.sesion)
    form = dict(pair.split("=", 1) for pair in args.dato)
    response = httpx.post(base + args.ruta, data=form, cookies=cookies, timeout=30)
    cookies.update(dict(response.cookies))
    _save_session(args.sesion, cookies)
    _preserve(args.nombre, response)
    return 0


def cmd_exportar(args) -> int:
    """Write everything a later reader needs to judge the run without repeating it."""
    db = store()
    channels = db.all_channels()
    evidence = {
        "exportado_en": datetime.now(timezone.utc).isoformat(),
        "campos_declarados": {
            "publicables": [f.name for f in domain.PUBLISHABLE_FIELDS],
            "privados": [f.name for f in domain.PRIVATE_FIELDS],
        },
        "canales": channels,
        "calibraciones": _calibrations(db, channels),
        "propuestas": {c["id"]: db.list_proposals(c["id"], limit=100)["items"] for c in channels},
        "rondas": [{**r, "propuestas": [p["id"] for p in db.round_proposals(r["id"])],
                    "autorizaciones": {kind: db.is_authorized(r["id"], kind)
                                       for kind in ("invitar", "publicar")}}
                   for c in channels for r in db.rounds_of(c["id"])],
        "evaluaciones": db.all_evaluations(),
        "invitaciones": db.all_invitations(),
        "registros_vinculados": db.all_records(),
        "votos": db.all_votes(),
        "llamadas": db.all_calls(),
        "solicitudes": db.all_requests(),
        "artefactos": _inventory(),
    }
    for round_id in db.published_rounds():
        evidence.setdefault("publicado", {})[round_id] = {
            "finalistas": db.finalists(round_id), "senales": db.signals(round_id)}
    db.close()
    destination = Path(args.destino)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(evidence, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Evidencia escrita en {destination}")
    return 0


def _calibrations(db, channels: list[dict]) -> dict:
    from circuit.store import NotFoundError

    saved = {}
    for channel in channels:
        try:
            saved[channel["id"]] = db.get_calibration(channel["id"])
        except NotFoundError:
            saved[channel["id"]] = None
    return saved


def _inventory() -> list[dict]:
    """Name and fingerprint every artefact of the run, so nothing rests on a later account."""
    entries = []
    for path in sorted([calls_file(), *captures_dir().glob("*.html")]):
        if not path.exists():
            continue
        raw = path.read_bytes()
        entries.append({"archivo": str(path.relative_to(DATA)), "bytes": len(raw),
                        "sha256": hashlib.sha256(raw).hexdigest()})
    return entries


def cmd_marcar(args) -> int:
    db = store()
    db.log_marker(utc_now(), args.nota)
    db.close()
    print(f"Marcador: {args.nota}")
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Circuito mínimo de propuestas de audiencia")
    parser.add_argument("--base", default="http://127.0.0.1:8000",
                        help="URL base con la que se arman los enlaces")
    sub = parser.add_subparsers(dest="comando", required=True)

    init = sub.add_parser("init", help="crear la base con una convocatoria y el canal permanente")
    init.add_argument("--cierra", default="2099-01-01T00:00:00+00:00")
    init.add_argument("--seleccionadas", type=int, default=4,
                      help="cuántas propuestas preselecciona la convocatoria")
    init.add_argument("--votos", type=int, default=3,
                      help="máximo de votos por participante y por ronda")
    init.set_defaults(func=cmd_init)

    seed = sub.add_parser("sembrar", help="cargar participaciones sintéticas")
    seed.add_argument("--canal", default=CONVOCATORIA)
    seed.add_argument("--cantidad", type=int, default=12)
    seed.add_argument("--desde", type=int, default=1,
                      help="número inicial, para que dos tandas no repitan el mismo texto")
    seed.set_defaults(func=cmd_seed)

    links = sub.add_parser("enlaces", help="mostrar los enlaces de las tres superficies")
    links.set_defaults(func=cmd_enlaces)

    serve = sub.add_parser("servir", help="levantar el sistema")
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--puerto", type=int, default=8000)
    serve.add_argument("--expuesto", action="store_true",
                       help="detrás de un servicio de reenvío: no rechaza Host ni Origin ajenos")
    serve.set_defaults(func=cmd_serve)

    evaluate = sub.add_parser("evaluar", help="evaluar una ronda con el ejecutor determinista local")
    evaluate.add_argument("--ronda", required=True)
    evaluate.add_argument("--etapa", type=int, default=1, choices=(1, 2))
    evaluate.set_defaults(func=cmd_evaluar)

    call = sub.add_parser("llamar", help="llamar una herramienta MCP por HTTP")
    call.add_argument("herramienta")
    call.add_argument("--argumentos", default="{}")
    call.set_defaults(func=cmd_llamar)

    capture = sub.add_parser("capturar", help="guardar el HTML exacto que devolvió una superficie")
    capture.add_argument("--ruta", action="append", required=True)
    capture.add_argument("--nombre", help="nombre del archivo, para capturar la misma ruta "
                                          "en dos momentos distintos")
    capture.add_argument("--sesion", default="anonima")
    capture.set_defaults(func=cmd_capturar)

    send = sub.add_parser("enviar", help="enviar un formulario y preservar la respuesta")
    send.add_argument("--ruta", required=True)
    send.add_argument("--dato", action="append", default=[], metavar="campo=valor")
    send.add_argument("--nombre", required=True)
    send.add_argument("--sesion", default="anonima")
    send.set_defaults(func=cmd_enviar)

    export = sub.add_parser("exportar", help="escribir la evidencia de la corrida")
    export.add_argument("--destino", default=str(DATA / "evidencia.json"))
    export.set_defaults(func=cmd_exportar)

    mark = sub.add_parser("marcar", help="dejar un marcador con nota en la evidencia")
    mark.add_argument("nota")
    mark.set_defaults(func=cmd_marcar)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
