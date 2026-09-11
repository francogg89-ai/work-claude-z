import json

import pytest
from mcp import Client

from probe.server import build_server
from probe.store import EXPECTED_P042_FINGERPRINT, IN_SCOPE_CALL
from probe.widget import FNV_JS, WIDGET_URI

pytestmark = pytest.mark.anyio


def payload(result):
    assert not result.is_error, result
    return result.structured_content or json.loads(result.content[0].text)


async def test_exposes_only_the_five_probe_tools_with_read_write_hints(store):
    async with Client(build_server(store, IN_SCOPE_CALL)) as client:
        tools = {t.name: t for t in (await client.list_tools()).tools}
    assert set(tools) == {"list_proposals", "get_proposal", "show_proposal", "save_evaluation", "get_evaluations"}
    for name in ("list_proposals", "get_proposal", "show_proposal", "get_evaluations"):
        assert tools[name].annotations.read_only_hint is True
    assert tools["save_evaluation"].annotations.read_only_hint is False
    assert tools["save_evaluation"].annotations.destructive_hint is False


async def test_only_show_proposal_is_bound_to_the_ui_resource(store):
    async with Client(build_server(store, IN_SCOPE_CALL)) as client:
        tools = {t.name: t for t in (await client.list_tools()).tools}
        resources = (await client.list_resources()).resources
        html = (await client.read_resource(WIDGET_URI)).contents[0]
    assert tools["show_proposal"].meta == {"ui": {"resourceUri": WIDGET_URI}}
    assert all(not (tools[n].meta or {}).get("ui") for n in tools if n != "show_proposal")
    assert [(r.uri, r.mime_type) for r in resources] == [(WIDGET_URI, "text/html;profile=mcp-app")]
    assert html.mime_type == "text/html;profile=mcp-app"
    assert FNV_JS in html.text
    assert "innerHTML" not in html.text


async def test_show_proposal_returns_structured_original_with_server_fingerprint(store):
    async with Client(build_server(store, IN_SCOPE_CALL)) as client:
        result = await client.call_tool("show_proposal", {"proposal_id": "P-042"})
    assert not result.is_error
    shown = result.structured_content
    assert shown is not None
    assert shown["what"] == "[SINTETICO] Propongo un especial sobre música independiente."
    assert shown["fingerprint"] == EXPECTED_P042_FINGERPRINT
    assert "@" not in json.dumps(shown, ensure_ascii=False)


async def test_calls_returning_a_proposal_log_its_original_fingerprint(store):
    async with Client(build_server(store, IN_SCOPE_CALL)) as client:
        await client.call_tool("get_proposal", {"proposal_id": "P-042"})
        await client.call_tool("show_proposal", {"proposal_id": "P-042"})
        await client.call_tool("list_proposals", {})
        await client.call_tool("show_proposal", {"proposal_id": "X-001"})
    assert [(c["tool"], c["original_fp"]) for c in store.all_calls()] == [
        ("get_proposal", EXPECTED_P042_FINGERPRINT),
        ("show_proposal", EXPECTED_P042_FINGERPRINT),
        ("list_proposals", ""),
        ("show_proposal", ""),
    ]


async def test_listing_reaches_all_in_scope_proposals(store):
    ids, cursor = [], None
    async with Client(build_server(store, IN_SCOPE_CALL)) as client:
        while True:
            args = {"cursor": cursor} if cursor else {}
            page = payload(await client.call_tool("list_proposals", args))
            ids += [i["id"] for i in page["items"]]
            cursor = page["next_cursor"]
            if cursor is None:
                break
    assert len(ids) == len(set(ids)) == 100


async def test_proposal_detail_never_carries_contact_data(store):
    async with Client(build_server(store, IN_SCOPE_CALL)) as client:
        result = await client.call_tool("get_proposal", {"proposal_id": "P-010"})
    text = json.dumps(payload(result))
    assert "@" not in text and "email" not in text


async def test_out_of_scope_request_is_an_error_without_data(store):
    async with Client(build_server(store, IN_SCOPE_CALL)) as client:
        result = await client.call_tool("get_proposal", {"proposal_id": "X-001"})
    assert result.is_error
    assert "X-001" not in json.dumps(result.structured_content or {})


async def test_saved_evaluation_can_be_read_back(store):
    async with Client(build_server(store, IN_SCOPE_CALL)) as client:
        saved = payload(await client.call_tool(
            "save_evaluation",
            {"proposal_id": "P-004", "result": "duda", "reasons": "Idea clara.", "doubts": "Falta ejemplo."},
        ))
        got = payload(await client.call_tool("get_evaluations", {"proposal_id": "P-004"}))
    assert got["evaluations"] == [saved]


async def test_every_tool_call_is_logged_server_side(store):
    async with Client(build_server(store, IN_SCOPE_CALL)) as client:
        await client.call_tool("get_proposal", {"proposal_id": "P-001"})
        await client.call_tool("get_proposal", {"proposal_id": "X-001"})
    assert [(c["tool"], c["ok"]) for c in store.all_calls()] == [("get_proposal", True), ("get_proposal", False)]
