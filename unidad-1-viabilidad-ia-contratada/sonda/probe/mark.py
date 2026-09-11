"""Write a timestamped marker into the probe's request log.

    python -m probe.mark <etiqueta>
"""

import sys
from pathlib import Path

from probe.store import Store

ALLOWED = ("inicio-chatgpt", "inicio-intento-capacidad-invalida", "fin")


def main() -> None:
    if len(sys.argv) != 2 or sys.argv[1] not in ALLOWED:
        raise SystemExit(f"Uso: python -m probe.mark <{'|'.join(ALLOWED)}>")
    store = Store(Path(".data") / "probe.sqlite")
    store.log_marker(sys.argv[1])
    store.close()
    print(f"Marcador registrado: {sys.argv[1]}")


if __name__ == "__main__":
    main()
