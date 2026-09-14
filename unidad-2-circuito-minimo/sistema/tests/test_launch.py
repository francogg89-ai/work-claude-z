"""Construction tests for the synthetic data and the local command line.

They exercise mechanisms of the candidate, not the cases of PLAN.md.
"""

import json

import pytest

from circuit import access, domain, launch, synthetic
from tests.conftest import CAPABILITY, CONVOCATORIA


@pytest.fixture()
def local(tmp_path, monkeypatch, circuito):
    monkeypatch.setattr(launch, "DATA", tmp_path)
    monkeypatch.setattr(launch, "CAPABILITY_FILE", tmp_path / "capacidad")
    monkeypatch.setattr(launch, "store", lambda: circuito)
    monkeypatch.setattr(circuito, "close", lambda: None)
    return tmp_path


def test_every_synthetic_proposal_carries_the_mark_inside_the_data():
    generated = synthetic.generate(CONVOCATORIA, 5)
    assert len(generated) == 5
    for submission in generated:
        assert domain.SYNTHETIC_MARK in submission["what"]
        assert domain.SYNTHETIC_MARK.lower() in submission["author"]
        domain.validate_submission(submission)


def test_the_synthetic_set_is_reproducible():
    assert synthetic.generate(CONVOCATORIA, 4) == synthetic.generate(CONVOCATORIA, 4)
    assert synthetic.generate(CONVOCATORIA, 4) != synthetic.generate(CONVOCATORIA, 4, seed=1)


def test_the_capability_is_generated_locally_and_kept_out_of_the_repository(local):
    first = launch.capability()
    assert access.check(first) == first
    assert launch.capability() == first
    assert (local / "capacidad").read_text(encoding="utf-8").strip() == first


def test_the_links_command_marks_which_surfaces_carry_the_capability(local, capsys):
    launch.main(["--base", "http://ejemplo.invalid", "enlaces"])
    printed = capsys.readouterr().out
    assert "http://ejemplo.invalid/entrada-creador" in printed
    assert launch.capability() in printed
    assert f"http://ejemplo.invalid{access.MCP_PATH}" in printed
    assert f"{access.MCP_PATH}/{launch.capability()}" not in printed


def test_seeding_stores_the_generated_participations(local, capsys):
    launch.main(["sembrar", "--canal", CONVOCATORIA, "--cantidad", "3"])
    assert "P-003" in capsys.readouterr().out


def test_the_export_preserves_the_run_without_leaking_the_capability(local, circuito, capsys):
    launch.main(["sembrar", "--canal", CONVOCATORIA, "--cantidad", "2"])
    launch.main(["marcar", "inicio"])
    destination = local / "evidencia.json"
    launch.main(["exportar", "--destino", str(destination)])
    evidence = json.loads(destination.read_text(encoding="utf-8"))
    assert [p["id"] for p in evidence["propuestas"][CONVOCATORIA]] == ["P-001", "P-002"]
    assert any(r["note"] == "inicio" for r in evidence["solicitudes"])
    assert launch.capability() not in destination.read_text(encoding="utf-8")
    assert "example.invalid" not in json.dumps(evidence)
    assert evidence["campos_declarados"]["publicables"] == [f.name for f in domain.PUBLISHABLE_FIELDS]


def test_the_export_keeps_the_whole_body_received_and_never_the_contact(local, circuito, capsys):
    """C-U2-5: the export listed only `what`, so the text sent in R5 and R6 had to be retyped."""
    from tests.conftest import submission

    sent = submission(1, why="Aporta porque responde una duda del chat.",
                      example="Un caso que me pasó la semana pasada.",
                      contact="uno.sintetico@example.invalid")
    circuito.receive_proposal(sent, at="2026-09-02T10:00:00+00:00")
    destination = local / "evidencia.json"
    launch.main(["exportar", "--destino", str(destination)])
    capsys.readouterr()

    raw = destination.read_text(encoding="utf-8")
    received = json.loads(raw)["propuestas"][CONVOCATORIA][0]
    assert received["id"] == "P-001"
    assert received["channel_id"] == CONVOCATORIA
    for field in ("what", "why", "example", "author"):
        assert received[field] == sent[field]
    assert received["received_at"] == "2026-09-02T10:00:00+00:00"
    assert received["synthetic"]
    assert "contact" not in received
    assert "uno.sintetico@example.invalid" not in raw


def test_the_export_keeps_when_each_authorization_was_granted(local, circuito, capsys):
    """C2.6 compares publicar_finalistas with granted_at; the rounds only said true or false."""
    from tests.conftest import submission

    circuito.receive_proposal(submission(1, contact="uno.sintetico@example.invalid"),
                              at="2026-09-02T10:00:00+00:00")
    round_ = circuito.open_round(CONVOCATORIA, cut_at="2026-09-30T00:00:00+00:00")
    circuito.authorize(round_["id"], "publicar", at="2026-09-30T01:30:00+00:00")
    destination = local / "evidencia.json"
    launch.main(["exportar", "--destino", str(destination)])
    capsys.readouterr()

    raw = destination.read_text(encoding="utf-8")
    assert json.loads(raw)["autorizaciones"] == [
        {"round_id": round_["id"], "kind": "publicar", "granted_at": "2026-09-30T01:30:00+00:00"}]
    assert "uno.sintetico@example.invalid" not in raw
    assert CAPABILITY not in raw and launch.capability() not in raw


def test_the_local_evaluator_can_be_run_from_the_command_line(local, circuito, capsys):
    launch.main(["sembrar", "--canal", CONVOCATORIA, "--cantidad", "2"])
    round_ = circuito.open_round(CONVOCATORIA, cut_at="2099-01-01T00:00:00+00:00")
    launch.main(["evaluar", "--ronda", round_["id"]])
    printed = capsys.readouterr().out
    assert "P-001" in printed
    assert {e["evaluator"] for e in circuito.evaluations_of(round_["id"])} == {"deterministico-local"}


def test_a_tool_can_be_called_over_http_the_way_a_remote_client_would(local, serve, capsys):
    base = serve()
    (local / "capacidad").write_text(CAPABILITY, encoding="utf-8")
    assert launch.main(["--base", base, "conectar"]) == 0
    assert launch.main(["--base", base, "llamar", "estado_del_sistema"]) == 0
    printed = capsys.readouterr().out
    assert "confirmado" in printed


def test_capturing_a_surface_keeps_the_exact_bytes_it_answered(local, serve, capsys):
    base = serve()
    launch.main(["--base", base, "capturar", "--ruta", "/", "--ruta", "/entrada-creador"])
    capsys.readouterr()
    guide = (local / "capturas" / "guia.html").read_text(encoding="utf-8")
    entry = (local / "capturas" / "entrada-creador.html").read_text(encoding="utf-8")
    assert "Criterios de selección" in guide
    assert "estado_del_sistema" in entry


def test_the_export_fingerprints_every_artefact_of_the_run(local, serve, capsys):
    base = serve()
    (local / "capacidad").write_text(CAPABILITY, encoding="utf-8")
    launch.main(["--base", base, "conectar"])
    launch.main(["--base", base, "llamar", "estado_del_sistema"])
    launch.main(["--base", base, "capturar", "--ruta", "/"])
    destination = local / "evidencia.json"
    launch.main(["exportar", "--destino", str(destination)])
    capsys.readouterr()

    evidence = json.loads(destination.read_text(encoding="utf-8"))
    files = {a["archivo"] for a in evidence["artefactos"]}
    assert "llamadas.jsonl" in files
    assert any(name.endswith("guia.html") for name in files)
    assert all(len(a["sha256"]) == 64 and a["bytes"] > 0 for a in evidence["artefactos"])

    logged = [json.loads(line) for line in
              (local / "llamadas.jsonl").read_text(encoding="utf-8").splitlines()]
    assert logged[0]["herramienta"] == "estado_del_sistema"
    assert "confirmado" in json.dumps(logged[0]["respuesta"], ensure_ascii=False)


def test_the_export_carries_the_bodies_needed_to_audit_the_chain(local, circuito, capsys):
    from tests.conftest import submission

    circuito.receive_proposal(submission(1), at="2026-09-02T10:00:00+00:00")
    round_ = circuito.open_round(CONVOCATORIA, cut_at="2026-09-30T00:00:00+00:00")
    circuito.save_evaluation(round_["id"], "P-001", stage=1, result="preseleccionada",
                             reasons="Coincide.", doubts="Falta ejemplo.",
                             evaluator="deterministico-local", at="2026-09-30T01:00:00+00:00")
    circuito.authorize(round_["id"], "invitar", at="2026-09-30T01:30:00+00:00")
    invitation = circuito.prepare_invitation(round_["id"], "P-001", "¿Con qué ejemplo?",
                                             operation_id="inv-1", at="2026-09-30T02:00:00+00:00")
    circuito.add_record_from_invitation(invitation["witness"], "Con dos invitados.",
                                        at="2026-10-01T10:00:00+00:00")
    circuito.authorize(round_["id"], "publicar", at="2026-10-01T11:00:00+00:00")
    circuito.publish(round_["id"], ["P-001"], operation_id="pub-1", at="2026-10-01T12:00:00+00:00")
    circuito.vote(round_["id"], "P-001", voter="votante-1", at="2026-10-02T10:00:00+00:00")

    destination = local / "evidencia.json"
    launch.main(["exportar", "--destino", str(destination)])
    capsys.readouterr()
    evidence = json.loads(destination.read_text(encoding="utf-8"))

    assert evidence["rondas"][0]["propuestas"] == ["P-001"]
    assert evidence["evaluaciones"][0]["doubts"] == "Falta ejemplo."
    assert evidence["registros_vinculados"][0]["body"] == "Con dos invitados."
    assert evidence["votos"][0]["proposal_id"] == "P-001"
    assert evidence["publicado"][round_["id"]]["finalistas"][0]["id"] == "P-001"
    assert evidence["invitaciones"][0]["proposal_id"] == "P-001"
    assert invitation["witness"] not in json.dumps(evidence)


def test_the_same_surface_can_be_captured_at_two_moments_under_different_names(local, serve, capsys):
    base = serve()
    launch.main(["--base", base, "capturar", "--ruta", "/", "--nombre", "guia-antes"])
    launch.main(["--base", base, "capturar", "--ruta", "/", "--nombre", "guia-despues"])
    capsys.readouterr()
    assert (local / "capturas" / "guia-antes.html").exists()
    assert (local / "capturas" / "guia-despues.html").exists()


def test_the_preserved_call_keeps_the_answer_but_not_the_capability(local, serve, capsys):
    base = serve()
    (local / "capacidad").write_text(CAPABILITY, encoding="utf-8")
    launch.main(["--base", base, "conectar"])
    launch.main(["--base", base, "llamar", "estado_del_sistema"])
    capsys.readouterr()
    logged = (local / "llamadas.jsonl").read_text(encoding="utf-8")
    assert CAPABILITY not in logged
    assert "<capacidad>" in logged
    assert "confirmado" in logged


def test_a_form_can_be_sent_and_its_refusal_is_preserved(local, serve, capsys):
    base = serve()
    launch.main(["--base", base, "enviar", "--ruta", "/propuestas", "--nombre", "envio-corto",
                 "--dato", "channel_id=" + CONVOCATORIA, "--dato", "what=muy corto",
                 "--dato", "why=tambien corto", "--dato", "example=",
                 "--dato", "author=Ana", "--dato", "contact=ana@example.invalid"])
    printed = capsys.readouterr().out
    assert "400" in printed
    saved = (local / "capturas" / "envio-corto.html").read_text(encoding="utf-8")
    assert "No se pudo enviar" in saved
    assert str(domain.LIMITS["what"][0]) in saved


def test_a_session_keeps_the_voter_mark_between_calls(local, circuito, serve, capsys):
    from tests.conftest import submission

    base = serve()
    circuito.receive_proposal(submission(1), at="2026-09-02T10:00:00+00:00")
    round_ = circuito.open_round(CONVOCATORIA, cut_at="2026-09-30T00:00:00+00:00")
    circuito.authorize(round_["id"], "publicar", at="2026-09-30T01:00:00+00:00")
    circuito.publish(round_["id"], ["P-001"], operation_id="pub-1", at="2026-09-30T02:00:00+00:00")

    launch.main(["--base", base, "capturar", "--ruta", "/finalistas", "--nombre", "lista",
                 "--sesion", "votante-1"])
    launch.main(["--base", base, "enviar", "--ruta", "/votos", "--nombre", "voto-1",
                 "--sesion", "votante-1", "--dato", "round_id=" + round_["id"],
                 "--dato", "proposal_id=P-001"])
    launch.main(["--base", base, "enviar", "--ruta", "/votos", "--nombre", "voto-repetido",
                 "--sesion", "votante-1", "--dato", "round_id=" + round_["id"],
                 "--dato", "proposal_id=P-001"])
    capsys.readouterr()

    assert circuito.audience_preference(round_["id"]) == {"P-001": 1}
    assert "Ya votaste" in (local / "capturas" / "voto-repetido.html").read_text(encoding="utf-8")


def test_a_captured_extension_page_does_not_carry_the_witness(local, circuito, serve, capsys):
    from tests.conftest import submission

    base = serve()
    circuito.receive_proposal(submission(1), at="2026-09-02T10:00:00+00:00")
    round_ = circuito.open_round(CONVOCATORIA, cut_at="2026-09-30T00:00:00+00:00")
    circuito.authorize(round_["id"], "invitar", at="2026-09-30T01:00:00+00:00")
    invitation = circuito.prepare_invitation(round_["id"], "P-001", "¿Con qué ejemplo?",
                                             operation_id="inv-1", at="2026-09-30T02:00:00+00:00")
    launch.main(["--base", base, "capturar", "--ruta", f"/ampliar/{invitation['witness']}",
                 "--nombre", "ampliar"])
    capsys.readouterr()
    saved = (local / "capturas" / "ampliar.html").read_text(encoding="utf-8")
    assert invitation["witness"] not in saved
    assert "/ampliar/<testigo>" in saved
    assert "No tenés que copiar ningún código" in saved


def test_the_preserved_call_substitutes_the_witness_by_value(local, circuito, serve, capsys):
    from tests.conftest import submission

    base = serve()
    (local / "capacidad").write_text(CAPABILITY, encoding="utf-8")
    circuito.receive_proposal(submission(1), at="2026-09-02T10:00:00+00:00")
    round_ = circuito.open_round(CONVOCATORIA, cut_at="2026-09-30T00:00:00+00:00")
    circuito.authorize(round_["id"], "invitar", at="2026-09-30T01:00:00+00:00")

    launch.main(["--base", base, "conectar"])
    launch.main(["--base", base, "llamar", "preparar_invitacion", "--argumentos", json.dumps(
        {"round_id": round_["id"], "proposal_id": "P-001", "pregunta": "¿Con qué ejemplo?",
         "id_operacion": "inv-1"})])
    capsys.readouterr()

    witness = circuito.invitations_of(round_["id"])[0]["witness"]
    logged = (local / "llamadas.jsonl").read_text(encoding="utf-8")
    assert witness not in logged
    assert "/ampliar/<testigo>" in logged
    assert "INV-" in logged


def test_the_export_shows_the_connection_going_from_pending_to_approved(local, circuito, serve,
                                                                       capsys):
    base = serve()
    (local / "capacidad").write_text(CAPABILITY, encoding="utf-8")
    launch.main(["--base", base, "conectar"])
    destination = local / "evidencia.json"
    launch.main(["exportar", "--destino", str(destination)])
    capsys.readouterr()

    evidence = json.loads(destination.read_text(encoding="utf-8"))
    conexiones = evidence["conexiones"]
    assert len(conexiones) == 1
    assert conexiones[0]["client_name"] == "circuito-local"
    assert conexiones[0]["created_at"] and conexiones[0]["approved_at"]

    tokens = evidence["tokens"]
    assert {t["kind"] for t in tokens} == {"acceso", "refresco"}
    assert all(len(t["huella"]) == 8 for t in tokens)
    assert all(issued not in json.dumps(evidence) for issued in circuito.issued_tokens())


def test_the_export_shows_a_revoked_token_as_revoked(local, circuito, serve, capsys):
    base = serve()
    (local / "capacidad").write_text(CAPABILITY, encoding="utf-8")
    launch.main(["--base", base, "conectar"])
    circuito.revoke_oauth_token((local / "token").read_text(encoding="utf-8").strip())
    destination = local / "evidencia.json"
    launch.main(["exportar", "--destino", str(destination)])
    capsys.readouterr()

    evidence = json.loads(destination.read_text(encoding="utf-8"))
    revocados = [t for t in evidence["tokens"] if t["revoked_at"]]
    assert [t["kind"] for t in revocados] == ["acceso"]


@pytest.mark.parametrize("argv", [
    ["--base", "https://ejemplo.invalid", "servir", "--expuesto"],
    ["servir", "--expuesto", "--base", "https://ejemplo.invalid"],
])
def test_the_base_is_accepted_before_or_after_the_command(argv):
    args = launch.build_parser().parse_args(argv)
    assert args.base == "https://ejemplo.invalid"
    assert args.expuesto is True
    assert args.func is launch.cmd_serve


def test_without_a_base_the_local_default_stays():
    args = launch.build_parser().parse_args(["servir"])
    assert args.base == "http://127.0.0.1:8000"
    assert args.expuesto is False


def test_an_unknown_argument_is_still_refused():
    with pytest.raises(SystemExit) as refused:
        launch.build_parser().parse_args(["servir", "--inexistente"])
    assert refused.value.code == 2


@pytest.fixture()
def fresh(tmp_path, monkeypatch):
    """A real base on disk, created by the command line the way a run creates it."""
    monkeypatch.setattr(launch, "DATA", tmp_path)
    monkeypatch.setattr(launch, "DB", tmp_path / "circuito.sqlite")
    monkeypatch.setattr(launch, "CAPABILITY_FILE", tmp_path / "capacidad")
    (tmp_path / "capacidad").write_text(CAPABILITY, encoding="utf-8")
    return tmp_path


@pytest.fixture()
def serve_fresh(fresh, clock):
    from circuit.store import Store
    from tests.conftest import _serving

    db = Store(fresh / "circuito.sqlite")
    yield from _serving(db, clock)
    db.close()


def _channel(fresh, channel_id):
    from circuit.store import Store

    db = Store(fresh / "circuito.sqlite")
    try:
        return db.get_channel(channel_id), db.list_proposals(channel_id)["items"]
    finally:
        db.close()


def test_seeding_right_after_init_is_refused_because_the_call_is_not_open_yet(fresh, capsys):
    from circuit.store import ClosedChannelError

    launch.main(["init", "--seleccionadas", "4", "--votos", "3"])
    with pytest.raises(ClosedChannelError):
        launch.main(["sembrar", "--canal", launch.CONVOCATORIA, "--cantidad", "8"])
    channel, proposals = _channel(fresh, launch.CONVOCATORIA)
    assert channel["status"] == "preparacion"
    assert proposals == []


def test_calibrating_from_the_command_line_proposes_without_opening(fresh, capsys):
    from circuit.store import ClosedChannelError, Store

    launch.main(["init", "--seleccionadas", "4", "--votos", "3"])
    assert launch.main(["calibrar", "--canal", launch.CONVOCATORIA]) == 0
    db = Store(fresh / "circuito.sqlite")
    try:
        calibration = db.get_calibration(launch.CONVOCATORIA)
        assert calibration["reviewed_at"] is None
        assert "ejecutor local" in calibration["interpretation"]
        assert calibration["examples"]
    finally:
        db.close()
    with pytest.raises(ClosedChannelError):
        launch.main(["sembrar", "--canal", launch.CONVOCATORIA, "--cantidad", "8"])


def test_the_preparation_sequence_of_c_u2_4_completes(fresh, serve_fresh, capsys):
    import httpx

    launch.main(["init", "--seleccionadas", "4", "--votos", "3"])
    launch.main(["calibrar", "--canal", launch.CONVOCATORIA])
    base = serve_fresh()
    panel = base + access.panel_path(CAPABILITY)
    assert httpx.get(panel).status_code == 200
    approved = httpx.post(panel + "/calibracion/aprobar", data={"channel_id": launch.CONVOCATORIA})
    assert approved.status_code == 303

    assert launch.main(["sembrar", "--canal", launch.CONVOCATORIA, "--cantidad", "8"]) == 0
    assert "P-008" in capsys.readouterr().out
    channel, proposals = _channel(fresh, launch.CONVOCATORIA)
    assert channel["status"] == "abierta"
    assert [p["id"] for p in proposals] == [f"P-{n:03d}" for n in range(1, 9)]
    assert _channel(fresh, launch.PERMANENTE)[0]["status"] == "preparacion"


def test_the_form_receives_only_while_the_call_is_open_so_assisted_runs_precede_the_cut(
        fresh, serve_fresh, capsys):
    import httpx

    from circuit.store import Store

    launch.main(["init", "--seleccionadas", "4", "--votos", "3"])
    launch.main(["calibrar", "--canal", launch.CONVOCATORIA])
    base = serve_fresh()
    httpx.post(base + access.panel_path(CAPABILITY) + "/calibracion/aprobar",
               data={"channel_id": launch.CONVOCATORIA})
    launch.main(["sembrar", "--canal", launch.CONVOCATORIA, "--cantidad", "8"])
    form = {"channel_id": launch.CONVOCATORIA,
            "what": "[SINTETICO] Propongo un episodio sobre cómo verificar noticias.",
            "why": "Aporta porque mucha gente comparte cosas falsas sin darse cuenta.",
            "example": "", "author": "Participante sintético",
            "contact": "participante.sintetico@example.invalid"}

    assert httpx.post(base + "/propuestas", data=form).status_code == 200
    db = Store(fresh / "circuito.sqlite")
    try:
        db.open_round(launch.CONVOCATORIA, cut_at="2099-01-01T00:00:00+00:00")
    finally:
        db.close()
    assert httpx.post(base + "/propuestas", data=form).status_code == 400
    assert "Participación cerrada" in httpx.get(base + "/").text
