"""Construction tests for the domain rules.

These exercise mechanisms of the candidate. They are not the cases of PLAN.md: those are
discriminating verifications and run only under a contract frozen by the auditor.
"""

import pytest

from circuit import domain


def test_publishable_and_private_fields_do_not_overlap():
    publishable = {f.name for f in domain.PUBLISHABLE_FIELDS}
    private = {f.name for f in domain.PRIVATE_FIELDS}
    assert publishable and private
    assert publishable.isdisjoint(private)


def test_contact_is_declared_private():
    assert "contact" in {f.name for f in domain.PRIVATE_FIELDS}
    assert "contact" not in {f.name for f in domain.PUBLISHABLE_FIELDS}


def test_public_projection_returns_exactly_the_declared_publishable_fields():
    record = {
        "id": "P-001", "what": "a" * 40, "why": "b" * 40, "example": "", "author": "Ana",
        "received_at": "2026-09-12T10:00:00+00:00", "synthetic": domain.SYNTHETIC_MARK,
        "contact": "ana@example.invalid", "channel_id": "conv-1",
    }
    public = domain.public_projection(record)
    assert set(public) == {f.name for f in domain.PUBLISHABLE_FIELDS}
    assert "contact" not in public


def test_public_projection_fails_loudly_when_a_declared_field_is_missing():
    with pytest.raises(KeyError):
        domain.public_projection({"id": "P-001"})


def test_fingerprint_is_stable_and_sensitive_to_the_accent_the_model_normalises():
    assert domain.fingerprint("[SINTETICO] hola") == domain.fingerprint("[SINTETICO] hola")
    assert domain.fingerprint("[SINTETICO] hola") != domain.fingerprint("[SINTÉTICO] hola")


def test_proposal_fingerprint_covers_the_three_original_fields():
    base = {"what": "uno", "why": "dos", "example": "tres"}
    assert domain.proposal_fingerprint(base) == domain.fingerprint("uno\ndos\ntres")
    assert domain.proposal_fingerprint({**base, "example": "otro"}) != domain.proposal_fingerprint(base)


@pytest.mark.parametrize(
    "field, value",
    [("what", ""), ("what", "corto"), ("what", "x" * 401), ("why", ""), ("why", "x" * 401),
     ("example", "x" * 601), ("author", ""), ("author", "x" * 81), ("contact", "sin-arroba")],
)
def test_submission_rejects_values_outside_the_declared_limits(field, value):
    submission = {"what": "w" * 40, "why": "y" * 40, "example": "", "author": "Ana",
                  "contact": "ana@example.invalid"}
    submission[field] = value
    with pytest.raises(domain.SubmissionError):
        domain.validate_submission(submission)


def test_submission_accepts_an_empty_example_because_participating_must_stay_cheap():
    submission = {"what": "w" * 40, "why": "y" * 40, "example": "", "author": "Ana",
                  "contact": "ana@example.invalid"}
    assert domain.validate_submission(submission)["example"] == ""


def test_submission_keeps_the_participant_text_verbatim():
    text = "  Propongo [SINTÉTICO] algo con acentos y  dobles espacios.  " + "x" * 20
    submission = {"what": text, "why": "y" * 40, "example": "", "author": "Ana",
                  "contact": "ana@example.invalid"}
    assert domain.validate_submission(submission)["what"] == text.strip()


def test_round_membership_is_derived_from_the_channel_and_the_cut():
    proposals = [
        {"id": "P-1", "channel_id": "perm", "received_at": "2026-09-01T00:00:00+00:00"},
        {"id": "P-2", "channel_id": "perm", "received_at": "2026-09-05T00:00:00+00:00"},
        {"id": "P-3", "channel_id": "conv", "received_at": "2026-09-02T00:00:00+00:00"},
        {"id": "P-4", "channel_id": "perm", "received_at": "2026-09-20T00:00:00+00:00"},
    ]
    first_cut = domain.round_membership(proposals, channel_id="perm",
                                        cut_at="2026-09-10T00:00:00+00:00", previous_cut_at=None)
    assert [p["id"] for p in first_cut] == ["P-1", "P-2"]


def test_a_permanent_proposal_received_after_a_cut_belongs_to_the_next_one():
    proposals = [
        {"id": "P-1", "channel_id": "perm", "received_at": "2026-09-05T00:00:00+00:00"},
        {"id": "P-4", "channel_id": "perm", "received_at": "2026-09-20T00:00:00+00:00"},
    ]
    second_cut = domain.round_membership(proposals, channel_id="perm",
                                         cut_at="2026-09-30T00:00:00+00:00",
                                         previous_cut_at="2026-09-10T00:00:00+00:00")
    assert [p["id"] for p in second_cut] == ["P-4"]


def test_signals_stay_three_and_are_never_composed():
    assert domain.SIGNALS == ("ia", "audiencia", "creador")
    combined = domain.signals_view(
        ia=["P-1", "P-2"], audiencia={"P-2": 5, "P-1": 1}, creador=["P-1"])
    assert set(combined) == {"ia", "audiencia", "creador"}
    assert not any("total" in key or "ranking" in key for key in combined)


def test_reception_date_is_always_labelled_as_reception_in_the_system():
    label = domain.reception_label("2026-09-12T10:00:00+00:00")
    assert "recibida en el sistema" in label.lower()
    assert "autoría" not in label.lower()
