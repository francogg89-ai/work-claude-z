"""Gate G2: certify the public exposure before anything is configured in ChatGPT.

    python -m probe.check https://<host publico>

Uses the token in .data/token, never prints it, and only when every check passes writes the
two URLs to configure in ChatGPT into .data/chatgpt-url.txt and .data/chatgpt-url-invalida.txt.
Exit code 0 means the exposure is ready; any other code means it is not.
"""

import asyncio
import json
import sys
from pathlib import Path

import httpx
from mcp import Client

from probe.store import Store

DATA_DIR = Path(".data")
_INIT = {"jsonrpc": "2.0", "id": 1, "method": "initialize",
         "params": {"protocolVersion": "2025-06-18", "capabilities": {},
                    "clientInfo": {"name": "sonda-check", "version": "1"}}}
_HEADERS = {"Accept": "application/json, text/event-stream", "Content-Type": "application/json",
            "User-Agent": "sonda-check"}
EXPECTED_TOOLS = ["get_evaluations", "get_proposal", "list_proposals", "save_evaluation"]


def invalid_variant(token: str) -> str:
    return token[:-1] + ("A" if token[-1] != "A" else "B")


async def _list_tools(url: str) -> list[str]:
    async with Client(url, read_timeout_seconds=20) as client:
        return sorted(t.name for t in (await client.list_tools()).tools)


def check_public(base_url: str, token: str, store: Store, data_dir: Path) -> dict:
    base = base_url.rstrip("/")
    bad = invalid_variant(token)
    store.log_marker("check-publico-inicio")
    report = {"ok": False, "tools": [], "without_token": None, "invalid_token": None, "error": ""}
    try:
        report["tools"] = asyncio.run(_list_tools(f"{base}/mcp/{token}"))
        with httpx.Client(timeout=20) as http:
            report["without_token"] = http.post(f"{base}/mcp", json=_INIT, headers=_HEADERS).status_code
            report["invalid_token"] = http.post(f"{base}/mcp/{bad}", json=_INIT, headers=_HEADERS).status_code
        report["ok"] = (report["tools"] == EXPECTED_TOOLS
                        and report["without_token"] == 404 and report["invalid_token"] == 404)
    except Exception as exc:  # any failure means the exposure is not ready
        report["error"] = type(exc).__name__
    if report["ok"]:
        (data_dir / "chatgpt-url.txt").write_text(f"{base}/mcp/{token}")
        (data_dir / "chatgpt-url-invalida.txt").write_text(f"{base}/mcp/{bad}")
    store.log_marker("check-publico-ok" if report["ok"] else "check-publico-fallo")
    return report


def main() -> None:
    if len(sys.argv) != 2 or not sys.argv[1].startswith("https://"):
        raise SystemExit("Uso: python -m probe.check https://<host publico>")
    token = (DATA_DIR / "token").read_text().strip()
    store = Store(DATA_DIR / "probe.sqlite")
    report = check_public(sys.argv[1], token, store, DATA_DIR)
    store.close()
    print(json.dumps(report, indent=2))
    print("EXPOSICION LISTA" if report["ok"] else "EXPOSICION NO LISTA: no configurar ChatGPT")
    sys.exit(0 if report["ok"] else 1)


if __name__ == "__main__":
    main()
