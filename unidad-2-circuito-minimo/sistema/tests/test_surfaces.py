"""Construction tests for the HTTP surfaces, run against the real application.

They exercise mechanisms of the candidate, not the cases of PLAN.md.
"""

import httpx
import pytest

from circuit import access, domain
from tests.conftest import CAPABILITY, CONVOCATORIA, PERMANENTE, submission

INIT = {"jsonrpc": "2.0", "id": 1, "method": "initialize",
        "params": {"protocolVersion": "2025-06-18", "capabilities": {},
                   "clientInfo": {"name": "test", "version": "0"}}}
MCP_HEADERS = {"Accept": "application/json, text/event-stream", "Content-Type": "application/json"}

FORM = {"channel_id": CONVOCATORIA,
        "what": "[SINTETICO] Propongo un episodio sobre divulgación responsable.",
        "why": "Aporta porque responde dudas que aparecen seguido en el chat del canal.",
        "example": "", "author": "Participante sintético",
        "contact": "participante.sintetico@example.invalid"}


def test_the_guide_shows_objective_criteria_conditions_deadlines_and_how_to_take_part(serve):
    page = httpx.get(serve() + "/").text
    assert "Objetivo" in page and "Criterios de selección" in page
    assert "Condiciones" in page and "Plazos" in page
    assert "Participar sin IA es" in page
    assert "Buzón permanente" in page


def test_the_guide_announces_every_publishable_field_and_the_private_one(serve):
    page = httpx.get(serve() + "/").text
    for declared in domain.PUBLISHABLE_FIELDS:
        assert declared.label in page
    for declared in domain.PRIVATE_FIELDS:
        assert declared.label in page
        assert declared.notice in page


def test_a_submission_is_received_and_answered_with_the_reception_wording(serve):
    base = serve()
    response = httpx.post(base + "/propuestas", data=FORM)
    assert response.status_code == 200
    assert "P-001" in response.text
    assert "Recibida en el sistema" in response.text
    assert "no demuestra autoría" in response.text


def test_a_submission_over_the_limit_is_refused_and_says_the_limit(serve):
    response = httpx.post(serve() + "/propuestas", data={**FORM, "what": "x" * 401})
    assert response.status_code == 400
    assert str(domain.LIMITS["what"][1]) in response.text


def test_a_submission_to_a_closed_call_is_refused_and_points_at_the_permanent_channel(circuito, serve):
    base = serve()
    circuito.close_channel(CONVOCATORIA, at="2026-09-30T00:00:00+00:00")
    response = httpx.post(base + "/propuestas", data=FORM)
    assert response.status_code == 400
    assert PERMANENTE in response.text
    assert circuito.list_proposals(PERMANENTE)["items"] == []


def test_the_portal_publishes_only_the_declared_fields_and_never_the_contact(circuito, serve):
    base = serve()
    circuito.receive_proposal(submission(1), at="2026-09-02T10:00:00+00:00")
    round_ = circuito.open_round(CONVOCATORIA, cut_at="2026-09-30T00:00:00+00:00")
    circuito.authorize(round_["id"], "publicar", at="2026-09-30T01:00:00+00:00")
    circuito.publish(round_["id"], ["P-001"], operation_id="pub-1", at="2026-09-30T02:00:00+00:00")

    page = httpx.get(base + "/finalistas").text
    assert "P-001" in page
    assert "example.invalid" not in page
    assert "Recibida en el sistema" in page
    assert "no las suma en un único orden" in page


def test_nothing_is_public_before_the_creator_authorizes_the_publication(circuito, serve):
    base = serve()
    circuito.receive_proposal(submission(1), at="2026-09-02T10:00:00+00:00")
    circuito.open_round(CONVOCATORIA, cut_at="2026-09-30T00:00:00+00:00")
    page = httpx.get(base + "/finalistas").text
    assert "Todavía no hay finalistas" in page
    assert "P-001" not in page


def test_a_voter_is_marked_once_and_cannot_vote_the_same_proposal_twice(circuito, serve):
    base = serve()
    circuito.receive_proposal(submission(1), at="2026-09-02T10:00:00+00:00")
    round_ = circuito.open_round(CONVOCATORIA, cut_at="2026-09-30T00:00:00+00:00")
    circuito.authorize(round_["id"], "publicar", at="2026-09-30T01:00:00+00:00")
    circuito.publish(round_["id"], ["P-001"], operation_id="pub-1", at="2026-09-30T02:00:00+00:00")

    with httpx.Client(base_url=base, follow_redirects=True) as client:
        client.get("/finalistas")
        assert client.cookies.get("votante")
        first = client.post("/votos", data={"round_id": round_["id"], "proposal_id": "P-001"})
        assert first.status_code == 200
        second = client.post("/votos", data={"round_id": round_["id"], "proposal_id": "P-001"})
    assert second.status_code == 400
    assert circuito.audience_preference(round_["id"]) == {"P-001": 1}


def test_voting_without_having_opened_the_list_is_refused(serve):
    response = httpx.post(serve() + "/votos", data={"round_id": "x", "proposal_id": "P-001"})
    assert response.status_code == 400


def test_the_witness_link_identifies_the_author_without_any_code_to_copy(circuito, serve):
    base = serve()
    circuito.receive_proposal(submission(1), at="2026-09-02T10:00:00+00:00")
    round_ = circuito.open_round(CONVOCATORIA, cut_at="2026-09-30T00:00:00+00:00")
    circuito.authorize(round_["id"], "invitar", at="2026-09-30T01:00:00+00:00")
    invitation = circuito.prepare_invitation(round_["id"], "P-001", "¿Con qué ejemplo?",
                                             operation_id="inv-1", at="2026-09-30T02:00:00+00:00")

    page = httpx.get(f"{base}/ampliar/{invitation['witness']}")
    assert page.status_code == 200
    assert "No tenés que copiar ningún código" in page.text

    sent = httpx.post(f"{base}/ampliar/{invitation['witness']}",
                      data={"body": "Con dos invitados del propio canal."})
    assert sent.status_code == 200
    records = circuito.records_of("P-001")
    assert [r["kind"] for r in records] == ["ampliacion_autor"]
    assert circuito.get_proposal("P-001")["example"] == ""


def test_an_unknown_witness_is_not_a_door(serve):
    assert httpx.get(serve() + "/ampliar/inventado").status_code == 404


def test_the_creator_entry_link_carries_no_secret_and_demands_confirming_access(serve):
    page = httpx.get(serve() + "/entrada-creador")
    assert page.status_code == 200
    assert "estado_del_sistema" in page.text
    assert "no tenés acceso al sistema" in page.text
    assert CAPABILITY not in page.text


def test_the_panel_needs_the_capability(serve):
    base = serve()
    assert httpx.get(base + "/creador/otra-cosa").status_code == 404
    assert httpx.get(base + access.panel_path(CAPABILITY)).status_code == 200


def test_the_creator_grants_the_authorization_on_the_panel(circuito, serve):
    base = serve()
    circuito.receive_proposal(submission(1), at="2026-09-02T10:00:00+00:00")
    round_ = circuito.open_round(CONVOCATORIA, cut_at="2026-09-30T00:00:00+00:00")
    assert circuito.is_authorized(round_["id"], "publicar") is False

    response = httpx.post(f"{base}{access.panel_path(CAPABILITY)}/autorizar",
                          data={"round_id": round_["id"], "kind": "publicar"},
                          follow_redirects=True)
    assert response.status_code == 200
    assert circuito.is_authorized(round_["id"], "publicar") is True


def test_a_channel_in_preparation_offers_no_form_and_refuses_a_submission(serve_preparacion):
    base = serve_preparacion()
    guide = httpx.get(base + "/")
    assert "Participación cerrada" in guide.text
    assert "<form" not in guide.text
    assert httpx.post(base + "/propuestas", data=FORM).status_code == 400


def test_approving_the_interpretation_on_the_panel_is_what_opens_the_channel(
        preparacion, serve_preparacion):
    base = serve_preparacion()
    preparacion.save_calibration(CONVOCATORIA, "Priorizo lo realizable.",
                                 [{"propuesta": "Un taller", "resultado": "preseleccionada",
                                   "explicacion": "Realizable con pocos recursos."}])
    panel = httpx.get(base + access.panel_path(CAPABILITY)).text
    assert "Priorizo lo realizable." in panel
    assert "Realizable con pocos recursos." in panel
    assert httpx.post(base + "/propuestas", data=FORM).status_code == 400

    httpx.post(f"{base}{access.panel_path(CAPABILITY)}/calibracion/aprobar",
               data={"channel_id": CONVOCATORIA}, follow_redirects=True)
    assert preparacion.get_channel(CONVOCATORIA)["status"] == "abierta"
    assert httpx.post(base + "/propuestas", data=FORM).status_code == 200


def test_returning_the_interpretation_keeps_the_channel_shut_and_records_the_discrepancy(
        preparacion, serve_preparacion):
    base = serve_preparacion()
    preparacion.save_calibration(CONVOCATORIA, "Priorizo lo realizable.", [])
    httpx.post(f"{base}{access.panel_path(CAPABILITY)}/calibracion/devolver",
               data={"channel_id": CONVOCATORIA, "correction": "Falta el peso de la audiencia."},
               follow_redirects=True)

    calibration = preparacion.get_calibration(CONVOCATORIA)
    assert calibration["reviewed_at"] is None
    assert calibration["correction"] == "Falta el peso de la audiencia."
    assert preparacion.get_channel(CONVOCATORIA)["status"] == "preparacion"
    assert httpx.post(base + "/propuestas", data=FORM).status_code == 400
    assert "Falta el peso de la audiencia." in httpx.get(base + access.panel_path(CAPABILITY)).text


@pytest.mark.parametrize("path", ["/mcp", "/mcp/", "/mcp/" + "x" * 43])
def test_the_mcp_endpoint_does_not_exist_without_the_capability(serve, path):
    assert httpx.post(serve() + path, json=INIT, headers=MCP_HEADERS).status_code == 404


def test_the_mcp_endpoint_answers_plain_json_and_offers_no_event_stream(serve):
    base = serve()
    posted = httpx.post(base + access.mcp_path(CAPABILITY), json=INIT, headers=MCP_HEADERS)
    assert posted.status_code == 200
    assert posted.headers["content-type"].startswith("application/json")
    got = httpx.get(base + access.mcp_path(CAPABILITY), headers={"Accept": "text/event-stream"})
    assert got.status_code == 405


def test_every_request_is_logged_by_surface_and_never_with_its_path(circuito, serve):
    base = serve()
    httpx.get(base + "/")
    httpx.get(base + access.panel_path(CAPABILITY))
    httpx.post(base + access.mcp_path(CAPABILITY), json=INIT, headers=MCP_HEADERS)
    surfaces = [r["surface"] for r in circuito.all_requests()]
    assert surfaces == ["publica", "panel", "mcp"]
    assert all(CAPABILITY not in str(r) for r in circuito.all_requests())


def test_the_live_view_shows_the_same_published_list_in_a_readable_layout(circuito, serve):
    base = serve()
    circuito.receive_proposal(submission(1), at="2026-09-02T10:00:00+00:00")
    round_ = circuito.open_round(CONVOCATORIA, cut_at="2026-09-30T00:00:00+00:00")
    circuito.authorize(round_["id"], "publicar", at="2026-09-30T01:00:00+00:00")
    circuito.publish(round_["id"], ["P-001"], operation_id="pub-1", at="2026-09-30T02:00:00+00:00")

    page = httpx.get(base + "/finalistas/vivo").text
    assert "P-001" in page
    assert "example.invalid" not in page
    assert "font-size: 1.6rem" in page
    assert "no las suma en un único orden" in page


@pytest.mark.parametrize("path", ["/mcp", "/mcp/" + "x" * 43])
def test_a_get_without_the_capability_is_not_found_rather_than_method_not_allowed(serve, path):
    response = httpx.get(serve() + path, headers={"Accept": "text/event-stream"})
    assert response.status_code == 404


def _publish_one(circuito):
    circuito.receive_proposal(submission(1, example=""), at="2026-09-02T10:00:00+00:00")
    round_ = circuito.open_round(CONVOCATORIA, cut_at="2026-09-30T00:00:00+00:00")
    circuito.authorize(round_["id"], "publicar", at="2026-09-30T01:00:00+00:00")
    circuito.publish(round_["id"], ["P-001"], operation_id="pub-1", at="2026-09-30T02:00:00+00:00")
    return round_


@pytest.mark.parametrize("path", ["/finalistas", "/finalistas/vivo"])
def test_both_public_surfaces_show_every_declared_publishable_field(circuito, serve, path):
    base = serve()
    _publish_one(circuito)
    page = httpx.get(base + path).text
    for declared in domain.PUBLISHABLE_FIELDS:
        assert f"{declared.label}:" in page
    for declared in domain.PRIVATE_FIELDS:
        assert f"{declared.label}:" not in page
    assert "example.invalid" not in page


@pytest.mark.parametrize("path", ["/finalistas", "/finalistas/vivo"])
def test_an_empty_field_is_shown_as_empty_and_never_omitted(circuito, serve, path):
    base = serve()
    _publish_one(circuito)
    page = httpx.get(base + path).text
    assert "Ejemplo o detalle:" in page
    assert "(sin dato)" in page


def test_a_refused_submission_never_writes_the_contact_back_into_the_page(serve):
    response = httpx.post(serve() + "/propuestas", data={**FORM, "what": "x" * 401})
    assert response.status_code == 400
    assert FORM["contact"] not in response.text
    assert FORM["why"] in response.text
    assert "se te devuelve escrito" in response.text


def test_no_declared_private_field_is_written_back_into_a_refused_page(serve):
    response = httpx.post(serve() + "/propuestas", data={**FORM, "why": "corto"})
    for declared in domain.PRIVATE_FIELDS:
        assert f'name="{declared.name}" id="{declared.name}"' in response.text
        assert f'value="{FORM[declared.name]}"' not in response.text
