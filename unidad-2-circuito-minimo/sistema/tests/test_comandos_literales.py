"""Every literal command of the C-U2-5 contract and checkpoint parses with the real parser.

C-U2-4 stopped at P10 because the written command put an option where the parser refused it,
and nobody had checked the text against the parser before running it. These tests make that
check part of the candidate and step P0 of the procedure. They parse; they never run a command.
"""

import re
import shlex
from pathlib import Path

import pytest

from circuit import launch

UNIT = Path(__file__).resolve().parents[2]
DOCUMENTS = [UNIT / "CONTRATO-C-U2-5.md", UNIT / "CHECKPOINT_HUMANO-C-U2-5.md"]
BASE = "https://ejemplo.invalid"
PLACEHOLDERS = {"<BASE>": BASE, "<corrida>-<repetición>": "R5-1", "<nombre>": "R5-1"}
# A command starts with an option or a subcommand; "python -m circuit.launch …" in prose is not one.
COMMAND = re.compile(r"python -m circuit\.launch (?=[a-z-])[^`\n|]+")


def literal_commands(text: str) -> list[str]:
    return [match.group(0).strip().rstrip(";,.") for match in COMMAND.finditer(text)]


def parse(command: str):
    """Parse one literal command exactly as written, placeholders substituted. Never runs it."""
    for placeholder, value in PLACEHOLDERS.items():
        command = command.replace(placeholder, value)
    if "<" in command:
        raise ValueError(f"Marcador sin sustituir en: {command}")
    return launch.build_parser().parse_args(shlex.split(command)[3:])


@pytest.mark.parametrize("document", DOCUMENTS, ids=lambda p: p.name)
def test_every_literal_command_parses(document):
    commands = literal_commands(document.read_text(encoding="utf-8"))
    assert commands, f"{document.name} no tiene comandos literales"
    for command in commands:
        try:
            parse(command)
        except SystemExit as refused:
            pytest.fail(f"{document.name}: el parser rechaza «{command}» (rc={refused.code})")


@pytest.mark.parametrize("document", DOCUMENTS, ids=lambda p: p.name)
def test_the_exposed_server_step_carries_the_base_and_the_exposure(document):
    exposed = [parse(c) for c in literal_commands(document.read_text(encoding="utf-8"))
               if " servir" in c and "--expuesto" in c]
    assert exposed, f"{document.name} no tiene el paso del servidor expuesto"
    for args in exposed:
        assert args.func is launch.cmd_serve
        assert args.expuesto is True
        assert args.base == BASE


@pytest.mark.parametrize("document", DOCUMENTS, ids=lambda p: p.name)
def test_the_preparation_commands_are_all_present(document):
    parsed = [parse(c) for c in literal_commands(document.read_text(encoding="utf-8"))]
    names = {args.comando for args in parsed}
    assert {"init", "calibrar", "servir", "sembrar", "marcar", "exportar"} <= names


def test_the_check_refuses_a_command_the_parser_does_not_accept():
    """Negative control: without it a check that never fails would prove nothing."""
    with pytest.raises(SystemExit):
        parse("python -m circuit.launch servir --expuesto --bse <BASE>")
    with pytest.raises(ValueError):
        parse("python -m circuit.launch marcar <sin-sustituir>")
