import pytest

from probe.store import (
    IN_SCOPE_CALL,
    OUT_OF_SCOPE_CALL,
    SYNTHETIC_MARK,
    NotInScopeError,
    Store,
    generate_dataset,
)


def test_dataset_is_deterministic_and_marked_synthetic():
    first = generate_dataset()
    second = generate_dataset()
    assert first == second
    assert all(p["synthetic"] == SYNTHETIC_MARK for p in first["proposals"])
    assert all(SYNTHETIC_MARK.lower() in c["email"] for c in first["contacts"])


def test_dataset_has_initial_volume_and_out_of_scope_records():
    data = generate_dataset()
    calls = [p["call_id"] for p in data["proposals"]]
    assert calls.count(IN_SCOPE_CALL) == 100
    assert calls.count(OUT_OF_SCOPE_CALL) == 3


def test_contacts_are_kept_apart_from_proposals():
    data = generate_dataset()
    for p in data["proposals"]:
        assert "email" not in p
        assert "@" not in " ".join(str(v) for v in p.values())


def test_seed_is_idempotent(tmp_path):
    s = Store(tmp_path / "db.sqlite")
    s.seed(generate_dataset())
    s.seed(generate_dataset())
    page = s.list_proposals(IN_SCOPE_CALL, cursor=None, limit=500)
    assert len(page["items"]) == 100
    s.close()


def test_list_paginates_in_scope_only_without_duplicates(store):
    seen, cursor = [], None
    while True:
        page = store.list_proposals(IN_SCOPE_CALL, cursor=cursor, limit=40)
        seen += [i["id"] for i in page["items"]]
        cursor = page["next_cursor"]
        if cursor is None:
            break
    assert len(seen) == 100
    assert len(set(seen)) == 100
    assert all(i.startswith("P-") for i in seen)


def test_get_proposal_returns_original_without_contact(store):
    p = store.get_proposal(IN_SCOPE_CALL, "P-001")
    assert set(p) == {"id", "call_id", "what", "why", "example", "received_at", "synthetic"}


def test_out_of_scope_proposal_is_rejected(store):
    with pytest.raises(NotInScopeError):
        store.get_proposal(IN_SCOPE_CALL, "X-001")
    with pytest.raises(NotInScopeError):
        store.get_proposal(IN_SCOPE_CALL, "P-999")


def test_saved_evaluation_is_returned_and_survives_reopen(tmp_path):
    path = tmp_path / "db.sqlite"
    s = Store(path)
    s.seed(generate_dataset())
    saved = s.save_evaluation(IN_SCOPE_CALL, "P-002", "preseleccionada", "Aporta un ejemplo claro.", "")
    s.close()
    reopened = Store(path)
    got = reopened.get_evaluations(IN_SCOPE_CALL, "P-002")
    assert got == [saved]
    reopened.close()


def test_evaluation_rejects_unknown_result_and_out_of_scope(store):
    with pytest.raises(ValueError):
        store.save_evaluation(IN_SCOPE_CALL, "P-003", "excelente", "r", "")
    with pytest.raises(NotInScopeError):
        store.save_evaluation(IN_SCOPE_CALL, "X-002", "duda", "r", "")
    assert store.get_evaluations(IN_SCOPE_CALL, "P-003") == []


def test_call_log_records_each_tool_call_in_order(store):
    store.log_call("get_proposal", {"proposal_id": "P-001"}, ok=True)
    store.log_call("get_proposal", {"proposal_id": "X-001"}, ok=False)
    calls = store.all_calls()
    assert [(c["tool"], c["arguments"], c["ok"]) for c in calls] == [
        ("get_proposal", {"proposal_id": "P-001"}, True),
        ("get_proposal", {"proposal_id": "X-001"}, False),
    ]
