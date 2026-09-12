"""Rules of the circuit that do not depend on storage, transport or any model.

Two of them are load-bearing for the unit and live here so that there is exactly one place to
change them:

* the publishable fields are declared once and feed both the notice shown to the participant
  before sending and the projection that every public surface uses;
* membership of a proposal in a round is derived from its channel and the cut instant, never
  stored, so a round cannot silently disagree with the proposals it contains.
"""

from dataclasses import dataclass
from datetime import datetime

SYNTHETIC_MARK = "SINTETICO"
SIGNALS = ("ia", "audiencia", "creador")
DEFAULT_MAX_VOTES = 3
CHANNEL_KINDS = ("convocatoria", "permanente")
# A reception channel is born in `preparacion` and only reaches `abierta` when the creator has
# approved the interpretation of their criteria. The manifest puts that review *before* opening,
# so a channel that never went through it cannot receive anything.
CHANNEL_STATUSES = ("preparacion", "abierta", "cerrada")
EVALUATION_RESULTS = ("preseleccionada", "no_preseleccionada", "duda")
RECORD_KINDS = ("ampliacion_autor", "contribucion_tercero")


class SubmissionError(ValueError):
    """The participant's submission does not satisfy the declared limits of the form."""


@dataclass(frozen=True)
class Field:
    """One field of a proposal, with the exact wording the participant is shown about it."""

    name: str
    label: str
    notice: str


PUBLISHABLE_FIELDS = (
    Field("id", "Identificador", "Un código corto de la propuesta dentro del sistema."),
    Field("what", "Qué propone", "El texto que escribiste, tal como lo enviaste."),
    Field("why", "Por qué aporta", "El texto que escribiste, tal como lo enviaste."),
    Field("example", "Ejemplo o detalle", "El texto que escribiste, tal como lo enviaste."),
    Field("author", "Autoría", "El nombre que indiques acá es el que se muestra como autoría."),
    Field("received_at", "Fecha de recepción",
          "La fecha en que el sistema recibió la propuesta. No demuestra autoría ni prioridad."),
    Field("synthetic", "Marca de dato sintético",
          "Indica que la propuesta es un dato de prueba y no una participación real."),
)

PRIVATE_FIELDS = (
    Field("contact", "Contacto",
          "Se guarda separado y no se publica. Solo se usa para invitarte a ampliar tu propuesta."),
)

# Minimum and maximum characters per field. The minimums exist so that a proposal can be
# understood and evaluated at all; the maximums keep participation cheap, which the manifest
# requires. ARQUITECTURA.md justifies each number.
LIMITS = {
    "what": (20, 400),
    "why": (20, 400),
    "example": (0, 600),
    "author": (1, 80),
    "contact": (5, 120),
}


def fingerprint(text: str) -> str:
    """FNV-1a 32-bit over UTF-8, as 8 hex digits.

    Same function as the U1 probe, reimplemented here so this unit does not depend on the
    frozen candidate of another unit. It detects alteration, including the accent that the
    model normalises when it retypes a proposal; it is not a cryptographic guarantee.
    """
    h = 0x811C9DC5
    for byte in text.encode("utf-8"):
        h = ((h ^ byte) * 0x01000193) & 0xFFFFFFFF
    return f"{h:08x}"


def proposal_fingerprint(proposal: dict) -> str:
    """Fingerprint of the three fields that make up the original the participant wrote."""
    return fingerprint("\n".join([proposal["what"], proposal["why"], proposal["example"]]))


def public_projection(record: dict) -> dict:
    """Project a stored proposal onto exactly the declared publishable fields.

    Missing a declared field raises instead of returning a short record: a public surface that
    quietly drops a field would diverge from the notice the participant was shown.
    """
    return {field.name: record[field.name] for field in PUBLISHABLE_FIELDS}


def validate_submission(submission: dict) -> dict:
    """Validate and normalise one participant submission.

    Normalisation is only stripping the outer whitespace: what is stored as the original has to
    be what the participant sent, so no other rewriting happens here or anywhere else.
    """
    cleaned = {}
    for name in ("what", "why", "example", "author", "contact"):
        value = submission.get(name, "")
        if not isinstance(value, str):
            raise SubmissionError(f"El campo {name} debe ser texto.")
        cleaned[name] = value.strip()

    for name, (low, high) in LIMITS.items():
        size = len(cleaned[name])
        if size < low:
            raise SubmissionError(
                f"El campo {name} necesita al menos {low} caracteres y tiene {size}.")
        if size > high:
            raise SubmissionError(
                f"El campo {name} admite hasta {high} caracteres y tiene {size}.")

    contact = cleaned["contact"]
    if "@" not in contact or "." not in contact.split("@")[-1]:
        raise SubmissionError("El contacto debe ser una dirección de correo.")
    return cleaned


def round_membership(proposals: list[dict], channel_id: str, cut_at: str,
                     previous_cut_at: str | None) -> list[dict]:
    """Proposals of one channel that belong to the round closing at ``cut_at``.

    A proposal belongs to exactly one channel and to the first round of that channel whose cut
    is not before its reception, so a proposal received after a cut falls into the next one and
    is never re-assigned to another channel.
    """
    cut = _moment(cut_at)
    previous = _moment(previous_cut_at) if previous_cut_at else None
    inside = []
    for proposal in proposals:
        if proposal["channel_id"] != channel_id:
            continue
        received = _moment(proposal["received_at"])
        if received > cut:
            continue
        if previous is not None and received <= previous:
            continue
        inside.append(proposal)
    return sorted(inside, key=lambda p: (p["received_at"], p["id"]))


def signals_view(ia: list[str], audiencia: dict[str, int], creador: list[str]) -> dict:
    """The three signals, side by side and never added up.

    Composing them into a fourth ranking is excluded by the manifest, so this function returns
    them keyed exactly by SIGNALS and nothing else.
    """
    return {"ia": list(ia), "audiencia": dict(audiencia), "creador": list(creador)}


def reception_label(received_at: str) -> str:
    """Wording used by every surface that shows the date of a proposal."""
    moment = _moment(received_at)
    return f"Recibida en el sistema el {moment:%d/%m/%Y a las %H:%M} UTC"


def _moment(value: str) -> datetime:
    return datetime.fromisoformat(value)
