import json

from probe.export import export_evidence
from probe.store import IN_SCOPE_CALL


def test_export_contains_calls_and_evaluations_but_no_contacts(store):
    store.save_evaluation(IN_SCOPE_CALL, "P-006", "duda", "r", "d")
    store.log_call("save_evaluation", {"proposal_id": "P-006"}, ok=True)
    evidence = export_evidence(store)
    assert [e["proposal_id"] for e in evidence["evaluations"]] == ["P-006"]
    assert [c["tool"] for c in evidence["calls"]] == ["save_evaluation"]
    assert "@" not in json.dumps(evidence)
