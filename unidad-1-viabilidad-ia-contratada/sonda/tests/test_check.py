from probe.check import check_public, invalid_variant
from tests.conftest import TOKEN


def test_invalid_variant_differs_and_keeps_length():
    bad = invalid_variant(TOKEN)
    assert bad != TOKEN and len(bad) == len(TOKEN)


def test_check_passes_against_a_correctly_exposed_probe_and_writes_url_files(serve, store, tmp_path):
    report = check_public(serve(True), TOKEN, store, tmp_path)
    assert report["ok"] is True
    assert report["tools"] == ["get_evaluations", "get_proposal", "list_proposals", "save_evaluation"]
    assert report["without_token"] == 404 and report["invalid_token"] == 404
    assert (tmp_path / "chatgpt-url.txt").read_text().endswith(f"/mcp/{TOKEN}")
    assert (tmp_path / "chatgpt-url-invalida.txt").read_text().endswith(f"/mcp/{invalid_variant(TOKEN)}")
    assert TOKEN not in repr(report)
    notes = [r["note"] for r in store.all_requests() if r["kind"] == "marker"]
    assert notes == ["check-publico-inicio", "check-publico-ok"]


def test_check_fails_when_nothing_is_listening_and_writes_no_url(store, tmp_path):
    report = check_public("http://127.0.0.1:9", TOKEN, store, tmp_path)
    assert report["ok"] is False
    assert not (tmp_path / "chatgpt-url.txt").exists()
    assert [r["note"] for r in store.all_requests() if r["kind"] == "marker"][-1] == "check-publico-fallo"
