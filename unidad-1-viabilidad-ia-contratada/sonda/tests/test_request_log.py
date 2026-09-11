import httpx

from tests.conftest import TOKEN
from tests.test_http import HEADERS, INIT


def test_every_http_request_is_logged_without_the_token(serve, store):
    base = serve(True)
    httpx.post(f"{base}/mcp/{TOKEN}", json=INIT, headers={**HEADERS, "Origin": "https://chatgpt.com"})
    httpx.post(f"{base}/mcp/{'y' * 43}", json=INIT, headers=HEADERS)
    rows = [r for r in store.all_requests() if r["kind"] == "http"]
    assert [(r["path_ok"], r["status"], r["rpc"]) for r in rows] == [(True, 200, "initialize"), (False, 404, "")]
    assert rows[0]["origin"] == "https://chatgpt.com"
    assert TOKEN not in repr(store.all_requests())


def test_markers_are_interleaved_in_order(serve, store):
    base = serve(True)
    store.log_marker("inicio-intento-capacidad-invalida")
    httpx.post(f"{base}/mcp/{'z' * 43}", json=INIT, headers=HEADERS)
    kinds = [(r["kind"], r["note"] if r["kind"] == "marker" else r["status"]) for r in store.all_requests()]
    assert kinds == [("marker", "inicio-intento-capacidad-invalida"), ("http", 404)]
