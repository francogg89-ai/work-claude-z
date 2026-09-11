import json

from probe.export import export_evidence
from probe.store import IN_SCOPE_CALL


def test_export_contains_calls_and_evaluations_but_no_contacts(store):
    store.save_evaluation(IN_SCOPE_CALL, "P-006", "duda", "r", "d")
    store.log_call("save_evaluation", {"proposal_id": "P-006"}, ok=True)
    evidence = export_evidence(store)
    assert [e["proposal_id"] for e in evidence["evaluations"]] == ["P-006"]
    assert [c["tool"] for c in evidence["calls"]] == ["save_evaluation"]
    assert "requests" in evidence
    assert "@" not in json.dumps(evidence)


def test_evidence_file_is_written_as_utf8_json(store, tmp_path):
    from probe.export import write_evidence
    store.save_evaluation(IN_SCOPE_CALL, "P-008", "duda", "razón con acento", "")
    out = tmp_path / "evidencia-servidor.json"
    write_evidence(store, out)
    raw = out.read_bytes()
    assert not raw.startswith(b"\xff\xfe")
    assert json.loads(raw.decode("utf-8"))["evaluations"][0]["reasons"] == "razón con acento"
