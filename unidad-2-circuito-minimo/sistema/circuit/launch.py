"""Local command line to prepare, run and preserve a run of the circuit.

The capability is generated here and written under ``.data``, which is ignored by Git: no
secret enters the repository, the documentation or any material that gets distributed.
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from circuit import access, synthetic
from circuit.app import build_app, utc_now
from circuit.store import Store

DATA = Path(__file__).resolve().parent.parent / ".data"
DB = DATA / "circuito.sqlite"
CAPABILITY_FILE = DATA / "capacidad"

CONVOCATORIA = "convocatoria-1"
PERMANENTE = "permanente"


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
        selected_count=3, opens_at=utc_now(), closes_at=args.cierra)
    db.create_channel(
        PERMANENTE, kind="permanente", title="Buzón permanente",
        question="¿Qué te gustaría escuchar en el canal?",
        restrictions="Se evalúa por cortes, no por fecha de cierre.",
        criteria="Se valoran propuestas concretas y realizables.",
        selected_count=2, opens_at=utc_now(), closes_at=None)
    db.close()
    print(f"Base creada en {DB}")
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
    """Call one MCP tool over HTTP, the same way a remote client would, and print the answer."""
    import httpx

    request = {"jsonrpc": "2.0", "id": 1, "method": "tools/call",
               "params": {"name": args.herramienta, "arguments": json.loads(args.argumentos)}}
    response = httpx.post(f"{args.base.rstrip('/')}{access.mcp_path(capability())}", json=request,
                          headers={"Accept": "application/json, text/event-stream",
                                   "Content-Type": "application/json"}, timeout=30)
    print(response.status_code)
    print(json.dumps(response.json(), ensure_ascii=False, indent=2))
    return 0 if response.status_code == 200 else 1


def cmd_exportar(args) -> int:
    db = store()
    evidence = {
        "exportado_en": datetime.now(timezone.utc).isoformat(),
        "canales": db.all_channels(),
        "propuestas": {c["id"]: db.list_proposals(c["id"], limit=100)["items"]
                       for c in db.all_channels()},
        "rondas": [r for c in db.all_channels() for r in db.rounds_of(c["id"])],
        "llamadas": db.all_calls(),
        "solicitudes": db.all_requests(),
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
