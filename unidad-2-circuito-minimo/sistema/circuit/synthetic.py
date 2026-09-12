"""Synthetic participations for local runs.

Every generated proposal carries the mark inside the data itself, not only in the documentation
around it, so a synthetic record cannot be mistaken for a real participation on any surface.
"""

import random

from circuit import domain

_TOPICS = [
    "un episodio sobre historia de la ciencia", "una serie de entrevistas a oyentes",
    "un taller en vivo de edición de audio", "un debate sobre hábitos de lectura",
    "una sección de preguntas de la audiencia", "un especial sobre música independiente",
    "una guía de herramientas gratuitas", "un recorrido por proyectos comunitarios",
    "una charla sobre divulgación responsable", "un reto semanal de escritura",
]
_REASONS = [
    "conecta con temas ya tratados en el canal", "suma voces que no suelen aparecer",
    "puede producirse con pocos recursos", "responde a dudas frecuentes del chat",
    "permite participación en directo",
]
_EXAMPLES = [
    "Un bloque de quince minutos con dos invitados del propio canal.",
    "Tres preguntas enviadas por el chat antes del vivo.",
    "Una demostración paso a paso con material libre.",
    "",
    "Una lista breve de fuentes para seguir el tema después.",
]


def generate(channel_id: str, count: int, seed: int = 20260912, start: int = 1) -> list[dict]:
    """Deterministic synthetic submissions, ready for ``Store.receive_proposal``."""
    rng = random.Random(seed + start)
    mark = domain.SYNTHETIC_MARK
    submissions = []
    for n in range(start, start + count):
        submissions.append({
            "channel_id": channel_id,
            "what": f"[{mark}] Propongo {rng.choice(_TOPICS)} para el canal.",
            "why": f"Aporta porque {rng.choice(_REASONS)}, y es abordable en una emisión.",
            "example": rng.choice(_EXAMPLES),
            "author": f"Participante {mark.lower()} {n:03d}",
            "contact": f"participante{n:03d}.{mark.lower()}@example.invalid",
        })
    return submissions
