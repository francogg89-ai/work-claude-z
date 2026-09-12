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
    assert "no los pegues en material público" in printed


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
    assert "contact" not in json.dumps(evidence)


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
    assert launch.main(["--base", base, "llamar", "estado_del_sistema"]) == 0
    printed = capsys.readouterr().out
    assert "confirmado" in printed
