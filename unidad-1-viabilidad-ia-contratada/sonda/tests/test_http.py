import json

import httpx
import pytest
from mcp import Client

from probe.server import build_app
from tests.conftest import TOKEN

INIT = {
    "jsonrpc": "2.0", "id": 1, "method": "initialize",
    "params": {"protocolVersion": "2025-06-18", "capabilities": {},
               "clientInfo": {"name": "probe-test", "version": "0"}},
}
HEADERS = {"Accept": "application/json, text/event-stream", "Content-Type": "application/json"}


def body(result):
    return result.structured_content or json.loads(result.content[0].text)


def test_build_app_refuses_a_weak_token(store):
    with pytest.raises(ValueError):
        build_app(store, "short", public=False)


@pytest.mark.parametrize("public", [False, True])
@pytest.mark.parametrize("path", ["/mcp", "/mcp/", "/mcp/" + "x" * 43, "/"])
def test_requests_without_the_valid_token_get_no_mcp_endpoint(serve, public, path):
    r = httpx.post(serve(public) + path, json=INIT, headers=HEADERS)
    assert r.status_code == 404


@pytest.mark.parametrize("public", [False, True])
def test_responses_are_plain_json_never_server_sent_events(serve, public):
    r = httpx.post(f"{serve(public)}/mcp/{TOKEN}", json=INIT, headers=HEADERS)
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("application/json")


@pytest.mark.parametrize("public", [False, True])
def test_no_standalone_event_stream_is_offered(serve, public):
    r = httpx.get(f"{serve(public)}/mcp/{TOKEN}", headers={"Accept": "text/event-stream"})
    assert r.status_code == 405


@pytest.mark.parametrize("path", ["/mcp", "/mcp/" + "x" * 43, "/"])
def test_get_without_the_valid_token_is_404_not_405(serve, path):
    r = httpx.get(serve(True) + path, headers={"Accept": "text/event-stream"})
    assert r.status_code == 404


def test_local_mode_rejects_a_foreign_host_header(serve):
    r = httpx.post(f"{serve(False)}/mcp/{TOKEN}", json=INIT, headers={**HEADERS, "Host": "attacker.example"})
    assert r.status_code == 421


def test_public_mode_accepts_forwarded_host_and_origin_but_still_requires_the_token(serve):
    base = serve(True)
    forwarded = {**HEADERS, "Host": "abc.trycloudflare.com", "Origin": "https://chatgpt.com"}
    assert httpx.post(f"{base}/mcp/{TOKEN}", json=INIT, headers=forwarded).status_code == 200
    assert httpx.post(f"{base}/mcp", json=INIT, headers=forwarded).status_code == 404


@pytest.mark.anyio
@pytest.mark.parametrize("public", [False, True])
async def test_valid_token_supports_the_read_and_write_round_trip(serve, public):
    async with Client(f"{serve(public)}/mcp/{TOKEN}") as client:
        assert not (await client.call_tool("list_proposals", {})).is_error
        saved = await client.call_tool(
            "save_evaluation",
            {"proposal_id": "P-005", "result": "preseleccionada", "reasons": "r", "doubts": ""},
        )
        assert not saved.is_error
        got = await client.call_tool("get_evaluations", {"proposal_id": "P-005"})
    assert body(got)["evaluations"] == [body(saved)]
