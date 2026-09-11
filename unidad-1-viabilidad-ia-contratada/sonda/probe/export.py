"""Write the probe's server-side evidence (requests, tool calls, evaluations) as UTF-8 JSON.

    python -m probe.export evidencia-servidor.json

The file is written directly, not through shell redirection, so its encoding does not depend
on the shell.
"""

import json
import sys
from pathlib import Path

from probe.store import Store


def export_evidence(store: Store) -> dict:
    return {"requests": store.all_requests(), "calls": store.all_calls(), "evaluations": store.all_evaluations()}


def write_evidence(store: Store, path: Path) -> None:
    Path(path).write_text(json.dumps(export_evidence(store), ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Uso: python -m probe.export <archivo.json>")
    s = Store(Path(".data") / "probe.sqlite")
    write_evidence(s, Path(sys.argv[1]))
    s.close()
    print(f"Evidencia escrita en {sys.argv[1]}")
