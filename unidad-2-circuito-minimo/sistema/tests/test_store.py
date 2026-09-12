"""Construction tests for the store.

They exercise mechanisms of the candidate, not the cases of PLAN.md.
"""

import pytest

from circuit import domain, store as store_module
from tests.conftest import CONVOCATORIA, PERMANENTE, submission


def test_a_received_proposal_keeps_its_text_and_gets_a_reception_date(circuito):
    sent = submission(1)
    proposal = circuito.receive_proposal(sent, at="2026-09-02T10:00:00+00:00")
    stored = circuito.get_proposal(proposal["id"])
    assert stored["what"] == sent["what"]
    assert stored["received_at"] == "2026-09-02T10:00:00+00:00"
    assert stored["synthetic"] == domain.SYNTHETIC_MARK


def test_contact_never_travels_with_the_proposal(circuito):
    proposal = circuito.receive_proposal(submission(1), at="2026-09-02T10:00:00+00:00")
    assert "contact" not in circuito.get_proposal(proposal["id"])
    assert "contact" not in circuito.list_proposals(CONVOCATORIA)["items"][0]
    assert circuito.contact_of(proposal["id"]) == submission(1)["contact"]


def test_a_closed_call_rejects_the_submission_and_never_reassigns_it(circuito):
    circuito.close_channel(CONVOCATORIA, at="2026-09-30T00:00:00+00:00")
    with pytest.raises(store_module.ClosedChannelError) as raised:
        circuito.receive_proposal(submission(2), at="2026-10-01T10:00:00+00:00")
    assert PERMANENTE in str(raised.value)
    assert circuito.list_proposals(PERMANENTE)["items"] == []


def test_a_round_freezes_the_criteria_it_was_cut_with(circuito):
    circuito.receive_proposal(submission(1), at="2026-09-02T10:00:00+00:00")
    round_ = circuito.open_round(CONVOCATORIA, cut_at="2026-09-30T00:00:00+00:00")
    circuito.update_channel_criteria(CONVOCATORIA, criteria="Otros criterios distintos.")
    assert circuito.get_round(round_["id"])["criteria"]["criteria"] != "Otros criterios distintos."


def test_a_round_contains_only_the_proposals_of_its_channel_and_window(circuito):
    circuito.receive_proposal(submission(1), at="2026-09-02T10:00:00+00:00")
    circuito.receive_proposal(submission(2, channel_id=PERMANENTE), at="2026-09-03T10:00:00+00:00")
    late = circuito.receive_proposal(submission(3, channel_id=PERMANENTE), at="2026-09-20T10:00:00+00:00")

    first = circuito.open_round(PERMANENTE, cut_at="2026-09-10T00:00:00+00:00")
    assert [p["id"] for p in circuito.round_proposals(first["id"])] == ["P-002"]

    second = circuito.open_round(PERMANENTE, cut_at="2026-09-30T00:00:00+00:00")
    assert [p["id"] for p in circuito.round_proposals(second["id"])] == [late["id"]]


def test_an_extension_is_a_new_linked_record_and_leaves_the_original_intact(circuito):
    proposal = circuito.receive_proposal(submission(1), at="2026-09-02T10:00:00+00:00")
    before = domain.proposal_fingerprint(circuito.get_proposal(proposal["id"]))
    round_ = circuito.open_round(CONVOCATORIA, cut_at="2026-09-30T00:00:00+00:00")
    circuito.authorize(round_["id"], "invitar", at="2026-09-30T01:00:00+00:00")
    invitation = circuito.prepare_invitation(
        round_["id"], proposal["id"], question="¿Con qué invitados lo harías?",
        operation_id="inv-1", at="2026-09-30T02:00:00+00:00")

    record = circuito.add_record_from_invitation(
        invitation["witness"], body="Con dos invitados del propio canal.",
        at="2026-10-01T10:00:00+00:00")

    assert record["kind"] == "ampliacion_autor"
    assert record["author"] == circuito.get_proposal(proposal["id"])["author"]
    assert domain.proposal_fingerprint(circuito.get_proposal(proposal["id"])) == before
    assert [r["id"] for r in circuito.records_of(proposal["id"])] == [record["id"]]


def test_the_witness_link_is_issued_by_the_system_and_an_unknown_one_is_refused(circuito):
    with pytest.raises(store_module.NotFoundError):
        circuito.add_record_from_invitation("testigo-inventado", body="hola",
                                            at="2026-10-01T10:00:00+00:00")


def test_inviting_without_authorization_is_refused(circuito):
    proposal = circuito.receive_proposal(submission(1), at="2026-09-02T10:00:00+00:00")
    round_ = circuito.open_round(CONVOCATORIA, cut_at="2026-09-30T00:00:00+00:00")
    with pytest.raises(store_module.NotAuthorizedError):
        circuito.prepare_invitation(round_["id"], proposal["id"], question="¿Y?",
                                    operation_id="inv-1", at="2026-09-30T02:00:00+00:00")
    assert circuito.invitations_of(round_["id"]) == []


def test_publishing_without_authorization_publishes_nothing(circuito):
    proposal = circuito.receive_proposal(submission(1), at="2026-09-02T10:00:00+00:00")
    round_ = circuito.open_round(CONVOCATORIA, cut_at="2026-09-30T00:00:00+00:00")
    with pytest.raises(store_module.NotAuthorizedError):
        circuito.publish(round_["id"], [proposal["id"]], operation_id="pub-1",
                         at="2026-09-30T03:00:00+00:00")
    assert circuito.finalists(round_["id"]) == []


def test_repeating_an_operation_id_does_not_duplicate_anything(circuito):
    proposal = circuito.receive_proposal(submission(1), at="2026-09-02T10:00:00+00:00")
    round_ = circuito.open_round(CONVOCATORIA, cut_at="2026-09-30T00:00:00+00:00")
    circuito.authorize(round_["id"], "invitar", at="2026-09-30T01:00:00+00:00")
    circuito.authorize(round_["id"], "publicar", at="2026-09-30T01:00:00+00:00")

    first = circuito.prepare_invitation(round_["id"], proposal["id"], question="¿Y?",
                                        operation_id="inv-1", at="2026-09-30T02:00:00+00:00")
    again = circuito.prepare_invitation(round_["id"], proposal["id"], question="¿Y?",
                                        operation_id="inv-1", at="2026-09-30T02:05:00+00:00")
    assert again == first
    assert len(circuito.invitations_of(round_["id"])) == 1

    circuito.publish(round_["id"], [proposal["id"]], operation_id="pub-1", at="2026-09-30T03:00:00+00:00")
    circuito.publish(round_["id"], [proposal["id"]], operation_id="pub-1", at="2026-09-30T03:05:00+00:00")
    assert [f["id"] for f in circuito.finalists(round_["id"])] == [proposal["id"]]


def test_the_published_list_has_no_duplicates_even_if_asked_twice_in_one_call(circuito):
    proposal = circuito.receive_proposal(submission(1), at="2026-09-02T10:00:00+00:00")
    round_ = circuito.open_round(CONVOCATORIA, cut_at="2026-09-30T00:00:00+00:00")
    circuito.authorize(round_["id"], "publicar", at="2026-09-30T01:00:00+00:00")
    circuito.publish(round_["id"], [proposal["id"], proposal["id"]], operation_id="pub-1",
                     at="2026-09-30T03:00:00+00:00")
    assert [f["id"] for f in circuito.finalists(round_["id"])] == [proposal["id"]]


def test_finalists_expose_only_publishable_fields(circuito):
    circuito.receive_proposal(submission(1), at="2026-09-02T10:00:00+00:00")
    round_ = circuito.open_round(CONVOCATORIA, cut_at="2026-09-30T00:00:00+00:00")
    circuito.authorize(round_["id"], "publicar", at="2026-09-30T01:00:00+00:00")
    circuito.publish(round_["id"], ["P-001"], operation_id="pub-1", at="2026-09-30T03:00:00+00:00")
    assert set(circuito.finalists(round_["id"])[0]) == {f.name for f in domain.PUBLISHABLE_FIELDS}


def test_a_voter_votes_once_per_proposal_and_up_to_the_configured_maximum(circuito):
    for n in (1, 2, 3, 4):
        circuito.receive_proposal(submission(n), at=f"2026-09-0{n}T10:00:00+00:00")
    round_ = circuito.open_round(CONVOCATORIA, cut_at="2026-09-30T00:00:00+00:00")
    circuito.authorize(round_["id"], "publicar", at="2026-09-30T01:00:00+00:00")
    circuito.publish(round_["id"], ["P-001", "P-002", "P-003", "P-004"], operation_id="pub-1",
                     at="2026-09-30T03:00:00+00:00")

    for pid in ("P-001", "P-002", "P-003"):
        circuito.vote(round_["id"], pid, voter="votante-1", at="2026-10-01T10:00:00+00:00")
    with pytest.raises(store_module.VoteRefused):
        circuito.vote(round_["id"], "P-001", voter="votante-1", at="2026-10-01T10:01:00+00:00")
    with pytest.raises(store_module.VoteRefused):
        circuito.vote(round_["id"], "P-004", voter="votante-1", at="2026-10-01T10:02:00+00:00")
    assert circuito.audience_preference(round_["id"]) == {"P-001": 1, "P-002": 1, "P-003": 1}


def test_voting_for_something_not_published_is_refused(circuito):
    circuito.receive_proposal(submission(1), at="2026-09-02T10:00:00+00:00")
    round_ = circuito.open_round(CONVOCATORIA, cut_at="2026-09-30T00:00:00+00:00")
    with pytest.raises(store_module.VoteRefused):
        circuito.vote(round_["id"], "P-001", voter="votante-1", at="2026-10-01T10:00:00+00:00")


def test_the_three_signals_are_stored_apart(circuito):
    circuito.receive_proposal(submission(1), at="2026-09-02T10:00:00+00:00")
    circuito.receive_proposal(submission(2), at="2026-09-03T10:00:00+00:00")
    round_ = circuito.open_round(CONVOCATORIA, cut_at="2026-09-30T00:00:00+00:00")
    circuito.save_evaluation(round_["id"], "P-001", stage=1, result="preseleccionada",
                             reasons="Coincide con los criterios.", doubts="",
                             evaluator="deterministico", at="2026-09-30T01:00:00+00:00")
    circuito.set_creator_choice(round_["id"], ["P-002"], at="2026-09-30T02:00:00+00:00")
    circuito.authorize(round_["id"], "publicar", at="2026-09-30T02:30:00+00:00")
    circuito.publish(round_["id"], ["P-001", "P-002"], operation_id="pub-1", at="2026-09-30T03:00:00+00:00")
    circuito.vote(round_["id"], "P-002", voter="votante-1", at="2026-10-01T10:00:00+00:00")

    signals = circuito.signals(round_["id"])
    assert signals == {"ia": ["P-001"], "audiencia": {"P-002": 1}, "creador": ["P-002"]}


def test_evaluations_record_who_evaluated(circuito):
    circuito.receive_proposal(submission(1), at="2026-09-02T10:00:00+00:00")
    round_ = circuito.open_round(CONVOCATORIA, cut_at="2026-09-30T00:00:00+00:00")
    circuito.save_evaluation(round_["id"], "P-001", stage=1, result="duda",
                             reasons="No queda claro el alcance.", doubts="¿Cuánto dura?",
                             evaluator="ia-del-creador", at="2026-09-30T01:00:00+00:00")
    saved = circuito.evaluations_of(round_["id"], "P-001")
    assert [e["evaluator"] for e in saved] == ["ia-del-creador"]
    assert saved[0]["stage"] == 1


def test_an_unknown_evaluation_result_is_refused(circuito):
    circuito.receive_proposal(submission(1), at="2026-09-02T10:00:00+00:00")
    round_ = circuito.open_round(CONVOCATORIA, cut_at="2026-09-30T00:00:00+00:00")
    with pytest.raises(ValueError):
        circuito.save_evaluation(round_["id"], "P-001", stage=1, result="excelente",
                                 reasons="x", doubts="", evaluator="deterministico",
                                 at="2026-09-30T01:00:00+00:00")


def test_the_second_evaluation_keeps_the_link_with_the_original(circuito):
    proposal = circuito.receive_proposal(submission(1), at="2026-09-02T10:00:00+00:00")
    round_ = circuito.open_round(CONVOCATORIA, cut_at="2026-09-30T00:00:00+00:00")
    circuito.authorize(round_["id"], "invitar", at="2026-09-30T01:00:00+00:00")
    invitation = circuito.prepare_invitation(round_["id"], proposal["id"], question="¿Y?",
                                             operation_id="inv-1", at="2026-09-30T02:00:00+00:00")
    circuito.add_record_from_invitation(invitation["witness"], body="Con dos invitados.",
                                        at="2026-10-01T10:00:00+00:00")
    material = circuito.evaluation_material(round_["id"], proposal["id"])
    assert material["original"]["what"] == circuito.get_proposal(proposal["id"])["what"]
    assert [r["body"] for r in material["records"]] == ["Con dos invitados."]
    assert "contact" not in material["original"]


def test_cutting_a_call_closes_it_and_leaves_the_permanent_channel_open(circuito):
    circuito.receive_proposal(submission(1), at="2026-09-02T10:00:00+00:00")
    circuito.open_round(CONVOCATORIA, cut_at="2026-09-30T00:00:00+00:00")
    assert circuito.get_channel(CONVOCATORIA)["status"] == "cerrada"
    assert [c["id"] for c in circuito.open_channels()] == [PERMANENTE]

    circuito.open_round(PERMANENTE, cut_at="2026-09-30T00:00:00+00:00")
    assert circuito.get_channel(PERMANENTE)["status"] == "abierta"


def test_a_closed_call_keeps_its_rounds_visible_to_the_creator(circuito):
    circuito.receive_proposal(submission(1), at="2026-09-02T10:00:00+00:00")
    round_ = circuito.open_round(CONVOCATORIA, cut_at="2026-09-30T00:00:00+00:00")
    assert [c["id"] for c in circuito.all_channels()] == [CONVOCATORIA, PERMANENTE]
    assert [r["id"] for r in circuito.rounds_of(CONVOCATORIA)] == [round_["id"]]


def test_a_late_submission_to_a_cut_call_is_refused_and_points_at_the_permanent_channel(circuito):
    circuito.receive_proposal(submission(1), at="2026-09-02T10:00:00+00:00")
    circuito.open_round(CONVOCATORIA, cut_at="2026-09-30T00:00:00+00:00")
    with pytest.raises(store_module.ClosedChannelError) as raised:
        circuito.receive_proposal(submission(9), at="2026-09-30T10:00:00+00:00")
    assert PERMANENTE in str(raised.value)
