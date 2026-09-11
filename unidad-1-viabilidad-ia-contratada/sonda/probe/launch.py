"""Start the probe for the real connection, in public mode, on 127.0.0.1.

    python -m probe.launch --fresh      new token and empty database
    python -m probe.launch              resume: same token and database

The token is written to .data/token and never printed.
"""

import argparse
import secrets
from pathlib import Path

from probe.server import build_app
from probe.store import Store, generate_dataset

DATA_DIR = Path(".data")


def prepare(data_dir: Path, fresh: bool) -> str:
    data_dir.mkdir(parents=True, exist_ok=True)
    token_file = data_dir / "token"
    if fresh:
        for name in ("probe.sqlite", "chatgpt-url.txt", "chatgpt-url-invalida.txt"):
            (data_dir / name).unlink(missing_ok=True)
        token_file.write_text(secrets.token_urlsafe(32))
    elif not token_file.exists():
        raise SystemExit("No hay token previo: arrancar con --fresh.")
    return token_file.read_text().strip()


def main() -> None:
    import uvicorn

    parser = argparse.ArgumentParser(prog="python -m probe.launch")
    parser.add_argument("--fresh", action="store_true", help="new token and empty database")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    token = prepare(DATA_DIR, args.fresh)
    store = Store(DATA_DIR / "probe.sqlite")
    store.seed(generate_dataset())
    print(f"Sonda escuchando en http://127.0.0.1:{args.port} (modo publico). Token en {DATA_DIR / 'token'}; no compartirlo.")
    print("Dejar esta ventana abierta. Ctrl+C para detener.")
    uvicorn.run(build_app(store, token, public=True), host="127.0.0.1", port=args.port,
                access_log=False, log_level="warning")


if __name__ == "__main__":
    main()
