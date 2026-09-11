import json
import socket
import threading
import time

import httpx
import pytest
import uvicorn
from mcp import Client

from probe.server import build_app
from probe.store import IN_SCOPE_CALL

TOKEN = "t" * 43
INIT = {
    "jsonrpc": "2.0", "id": 1, "method": "initialize",
    "params": {"protocolVersion": "2025-06-18", "capabilities": {},
               "clientInfo": {"name": "probe-test", "version": "0"}},
}
HEADERS = {"Accept": "application/json, text/event-stream", "Content-Type": "application/json"}


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture
def base_url(store):
    port = free_port()
    server = uvicorn.Server(uvicorn.Config(build_app(store, TOKEN, []), host="127.0.0.1", port=port, log_level="warning"))
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    deadline = time.time() + 10
    while not server.started and time.time() < deadline:
        time.sleep(0.05)
    assert server.started
    yield f"http://127.0.0.1:{port}"
    server.should_exit = True
    thread.join(timeout=10)


def test_build_app_refuses_a_weak_token(store):
    with pytest.raises(ValueError):
        build_app(store, "short", [])


@pytest.mark.parametrize("path", ["/mcp", "/mcp/", "/mcp/" + "x" * 43, "/"])
def test_requests_without_the_valid_token_get_no_mcp_endpoint(base_url, path):
    r = httpx.post(base_url + path, json=INIT, headers=HEADERS)
    assert r.status_code == 404


def test_foreign_host_header_is_rejected(base_url):
    r = httpx.post(f"{base_url}/mcp/{TOKEN}", json=INIT, headers={**HEADERS, "Host": "attacker.example"})
    assert r.status_code in (400, 403, 421)


@pytest.mark.anyio
async def test_valid_token_supports_the_read_and_write_round_trip(base_url):
    async with Client(f"{base_url}/mcp/{TOKEN}") as client:
        page = await client.call_tool("list_proposals", {})
        assert not page.is_error
        saved = await client.call_tool(
            "save_evaluation",
            {"proposal_id": "P-005", "result": "preseleccionada", "reasons": "r", "doubts": ""},
        )
        assert not saved.is_error
        got = await client.call_tool("get_evaluations", {"proposal_id": "P-005"})
    def body(r):
        return r.structured_content or json.loads(r.content[0].text)

    assert body(got)["evaluations"] == [body(saved)]
