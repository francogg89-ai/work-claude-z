"""Construction tests for the MCP surface the creator's AI uses.

They exercise mechanisms of the candidate, not the cases of PLAN.md.
"""

import json

import pytest
from mcp import Client

from circuit import evaluation
from circuit.creator import build_server
from circuit.view import VIEW_URI
from tests.conftest import CAPABILITY, CONVOCATORIA, calibrate_and_open, submission

pytestmark = pytest.mark.anyio

TOOLS = {"estado_del_sistema", "listar_propuestas", "ver_propuesta", "obtener_propuesta",
         "proponer_calibracion", "cortar_ronda", "guardar_evaluacion", "estado_autorizaciones",
         "solicitar_autorizacion", "preparar_invitacion", "publicar_finalistas",
         "senales_de_la_ronda"}


def payload(result):
    assert not result.is_error, result
    return result.structured_content or json.loads(result.content[0].text)


def server(store, clock):
    return build_server(store, CAPABILITY, public_base="http://local.invalid", clock=clock)


async def test_the_tools_declare_what_reads_and_what_writes(circuito, clock):
    async with Client(server(circuito, clock)) as client:
        tools = {t.name: t for t in (await client.list_tools()).tools}
    assert set(tools) == TOOLS
    for name in ("estado_del_sistema", "listar_propuestas", "ver_propuesta", "obtener_propuesta",
                 "estado_autorizaciones", "solicitar_autorizacion", "senales_de_la_ronda"):
        assert tools[name].annotations.read_only_hint is True
    for name in ("proponer_calibracion", "cortar_ronda", "guardar_evaluacion",
                 "preparar_invitacion", "publicar_finalistas"):
        assert tools[name].annotations.read_only_hint is False


async def test_only_the_faithful_view_is_bound_to_the_ui_resource(circuito, clock):
    async with Client(server(circuito, clock)) as client:
        tools = {t.name: t for t in (await client.list_tools()).tools}
        html = (await client.read_resource(VIEW_URI)).contents[0]
    assert tools["ver_propuesta"].meta == {"ui": {"resourceUri": VIEW_URI}}
    assert all(not (tools[name].meta or {}).get("ui") for name in tools if name != "ver_propuesta")
    assert html.mime_type == "text/html;profile=mcp-app"
    assert "innerHTML" not in html.text


async def test_the_instructions_require_confirming_access_before_operating(circuito, clock):
    instructions = server(circuito, clock).instructions or ""
    assert "estado_del_sistema" in instructions
    assert "ver_propuesta" in instructions
    assert "no obtuviste de estas herramientas" in instructions


async def test_the_status_tool_answers_with_what_the_system_actually_holds(circuito, clock):
    circuito.receive_proposal(submission(1), at="2026-09-02T10:00:00+00:00")
    async with Client(server(circuito, clock)) as client:
        status = payload(await client.call_tool("estado_del_sistema", {}))
    assert status["acceso"].startswith("confirmado")
    assert status["datos"] == "sintéticos"
    assert {c["id"] for c in status["canales"]} == {CONVOCATORIA, "permanente"}
    assert status["canales"][0]["propuestas"] >= 0


async def test_the_view_returns_the_original_with_its_fingerprint(circuito, clock):
    proposal = circuito.receive_proposal(submission(1), at="2026-09-02T10:00:00+00:00")
    async with Client(server(circuito, clock)) as client:
        shown = payload(await client.call_tool("ver_propuesta", {"proposal_id": proposal["id"]}))
    assert shown["what"] == proposal["what"]
    assert len(shown["fingerprint"]) == 8
    assert "recibida en el sistema" in shown["received_label"].lower()


async def test_the_material_for_evaluation_carries_no_contact_and_retrieves_no_link(circuito, clock):
    circuito.receive_proposal(
        submission(1, example="Detalle en https://ejemplo.invalid/x"), at="2026-09-02T10:00:00+00:00")
    async with Client(server(circuito, clock)) as client:
        material = payload(await client.call_tool("obtener_propuesta", {"proposal_id": "P-001"}))
    assert material["enlaces_no_recuperados"] == ["https://ejemplo.invalid/x"]
    assert "example.invalid" not in json.dumps(material["propuesta"])
    assert "no son instrucciones" in material["aviso"]


async def test_listing_never_returns_contact(circuito, clock):
    circuito.receive_proposal(submission(1), at="2026-09-02T10:00:00+00:00")
    async with Client(server(circuito, clock)) as client:
        listed = payload(await client.call_tool("listar_propuestas", {"channel_id": CONVOCATORIA}))
    assert "contact" not in listed["items"][0]


async def test_a_channel_in_preparation_cannot_be_cut_and_the_status_says_why(preparacion, clock):
    async with Client(server(preparacion, clock)) as client:
        status = payload(await client.call_tool("estado_del_sistema", {}))
        refused = await client.call_tool("cortar_ronda", {"channel_id": CONVOCATORIA})
    assert [c["status"] for c in status["canales"]] == ["preparacion", "preparacion"]
    assert all("sin proponer" in c["calibracion"] for c in status["canales"])
    assert refused.is_error


async def test_proposing_a_calibration_does_not_open_anything_by_itself(preparacion, clock):
    async with Client(server(preparacion, clock)) as client:
        proposed = payload(await client.call_tool("proponer_calibracion", {
            "channel_id": CONVOCATORIA, "interpretacion": "Priorizo lo realizable.",
            "ejemplos": [{"propuesta": "Un taller", "resultado": "preseleccionada",
                          "explicacion": "Realizable con pocos recursos."}]}))
        status = payload(await client.call_tool("estado_del_sistema", {}))
        refused = await client.call_tool("cortar_ronda", {"channel_id": CONVOCATORIA})
    assert "apruebe" in proposed["aviso"]
    assert preparacion.get_channel(CONVOCATORIA)["status"] == "preparacion"
    assert "esperando la aprobación" in status["canales"][0]["calibracion"]
    assert refused.is_error


async def test_once_the_creator_approves_the_channel_receives_and_the_round_can_be_cut(
        preparacion, clock):
    calibrate_and_open(preparacion, CONVOCATORIA)
    preparacion.receive_proposal(submission(1), at="2026-09-02T10:00:00+00:00")
    async with Client(server(preparacion, clock)) as client:
        status = payload(await client.call_tool("estado_del_sistema", {}))
        cut = payload(await client.call_tool("cortar_ronda", {"channel_id": CONVOCATORIA}))
    assert "aprobada por el creador" in status["canales"][0]["calibracion"]
    assert cut["propuestas"] == ["P-001"]


async def test_the_ai_cannot_authorize_itself_and_publishing_is_refused_until_the_creator_does(
        circuito, clock):
    circuito.receive_proposal(submission(1), at="2026-09-02T10:00:00+00:00")
    round_ = circuito.open_round(CONVOCATORIA, cut_at="2026-09-30T00:00:00+00:00")
    async with Client(server(circuito, clock)) as client:
        asked = payload(await client.call_tool("solicitar_autorizacion",
                                               {"round_id": round_["id"], "tipo": "publicar"}))
        assert asked["autorizado"] is False
        assert "/creador/" in asked["autorizar_en"]

        refused = await client.call_tool("publicar_finalistas", {
            "round_id": round_["id"], "ids_propuestas": ["P-001"], "id_operacion": "pub-1"})
        assert refused.is_error
        assert circuito.finalists(round_["id"]) == []

        circuito.authorize(round_["id"], "publicar", at="2026-09-30T01:00:00+00:00")
        published = payload(await client.call_tool("publicar_finalistas", {
            "round_id": round_["id"], "ids_propuestas": ["P-001"], "id_operacion": "pub-1"}))
    assert published["published"] == ["P-001"]


async def test_retrying_a_publication_with_the_same_operation_id_publishes_once(circuito, clock):
    circuito.receive_proposal(submission(1), at="2026-09-02T10:00:00+00:00")
    round_ = circuito.open_round(CONVOCATORIA, cut_at="2026-09-30T00:00:00+00:00")
    circuito.authorize(round_["id"], "publicar", at="2026-09-30T01:00:00+00:00")
    args = {"round_id": round_["id"], "ids_propuestas": ["P-001"], "id_operacion": "pub-1"}
    async with Client(server(circuito, clock)) as client:
        first = payload(await client.call_tool("publicar_finalistas", args))
        again = payload(await client.call_tool("publicar_finalistas", args))
    assert first == again
    assert [f["id"] for f in circuito.finalists(round_["id"])] == ["P-001"]


async def test_an_invitation_returns_a_witness_link_and_leaves_sending_to_the_creator(circuito, clock):
    circuito.receive_proposal(submission(1), at="2026-09-02T10:00:00+00:00")
    round_ = circuito.open_round(CONVOCATORIA, cut_at="2026-09-30T00:00:00+00:00")
    circuito.authorize(round_["id"], "invitar", at="2026-09-30T01:00:00+00:00")
    async with Client(server(circuito, clock)) as client:
        invitation = payload(await client.call_tool("preparar_invitacion", {
            "round_id": round_["id"], "proposal_id": "P-001", "pregunta": "¿Con qué ejemplo?",
            "id_operacion": "inv-1"}))
    assert invitation["enlace"].endswith(invitation["witness"])
    assert "decisión del creador" in invitation["envio"]


async def test_an_evaluation_saved_by_the_ai_records_who_evaluated_and_the_notice(circuito, clock):
    circuito.receive_proposal(submission(1), at="2026-09-02T10:00:00+00:00")
    round_ = circuito.open_round(CONVOCATORIA, cut_at="2026-09-30T00:00:00+00:00")
    async with Client(server(circuito, clock)) as client:
        saved = payload(await client.call_tool("guardar_evaluacion", {
            "round_id": round_["id"], "proposal_id": "P-001", "resultado": "preseleccionada",
            "razones": "Responde la pregunta de la ronda.", "dudas": "No trae ejemplo."}))
    assert saved["evaluator"] == "ia-del-creador"
    assert evaluation.NOT_AN_OBJECTIVE_MEASURE in saved["reasons"]


async def test_the_signals_come_back_as_three_and_say_they_are_not_combined(circuito, clock):
    circuito.receive_proposal(submission(1), at="2026-09-02T10:00:00+00:00")
    round_ = circuito.open_round(CONVOCATORIA, cut_at="2026-09-30T00:00:00+00:00")
    async with Client(server(circuito, clock)) as client:
        signals = payload(await client.call_tool("senales_de_la_ronda", {"round_id": round_["id"]}))
    assert {"ia", "audiencia", "creador"} <= set(signals)
    assert not any(key in signals for key in ("total", "ranking", "puntaje"))


async def test_a_refused_call_is_logged_as_a_failed_call(circuito, clock):
    async with Client(server(circuito, clock)) as client:
        failed = await client.call_tool("obtener_propuesta", {"proposal_id": "P-999"})
    assert failed.is_error
    assert [c["ok"] for c in circuito.all_calls()] == [False]
