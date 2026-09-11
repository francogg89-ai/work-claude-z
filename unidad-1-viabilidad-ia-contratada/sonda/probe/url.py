"""Move the URLs certified by gate G2 to the clipboard without ever displaying them.

    python -m probe.url copiar            valid URL, to paste only into ChatGPT
    python -m probe.url copiar-invalida   invalid-capability URL, for the negative control
    python -m probe.url limpiar           overwrite the clipboard right after pasting

The URL carries the token. It is never printed, so it cannot end up in a screenshot, a
transcript or another conversation by being read off the screen.
"""

import subprocess
import sys
from pathlib import Path

DATA_DIR = Path(".data")


def _windows_clipboard(value: str) -> None:
    subprocess.run(["clip"], input=value.encode("utf-16-le"), check=True)


def copy_url(data_dir: Path, invalid: bool, copier=_windows_clipboard) -> None:
    source = data_dir / ("chatgpt-url-invalida.txt" if invalid else "chatgpt-url.txt")
    if not source.exists():
        raise SystemExit("No hay URL certificada: ejecutar primero la puerta G2 (probe.check).")
    copier(source.read_text().strip())


def clear(copier=_windows_clipboard) -> None:
    copier("")


def main() -> None:
    command = sys.argv[1] if len(sys.argv) == 2 else ""
    if command == "copiar":
        copy_url(DATA_DIR, invalid=False)
        print("URL copiada al portapapeles. Pegarla solo en el campo URL de la app en ChatGPT, y limpiar enseguida.")
    elif command == "copiar-invalida":
        copy_url(DATA_DIR, invalid=True)
        print("URL invalida copiada al portapapeles. Pegarla solo en ChatGPT, y limpiar enseguida.")
    elif command == "limpiar":
        clear()
        print("Portapapeles limpio.")
    else:
        raise SystemExit("Uso: python -m probe.url <copiar|copiar-invalida|limpiar>")


if __name__ == "__main__":
    main()
