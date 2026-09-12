import pytest

from circuit import domain
from circuit.store import Store

CONVOCATORIA = "conv-piloto"
PERMANENTE = "permanente"


@pytest.fixture()
def store(tmp_path):
    store = Store(tmp_path / "circuito.sqlite")
    yield store
    store.close()


@pytest.fixture()
def circuito(store):
    """A store with the two reception channels open, which is the shape U2 has to close."""
    store.create_channel(
        CONVOCATORIA, kind="convocatoria", title="Ideas para el próximo ciclo",
        question="¿Qué tema querés que tratemos en profundidad?",
        restrictions="Una propuesta por persona.",
        criteria="Se valoran temas conectados con el canal y realizables con pocos recursos.",
        selected_count=2, opens_at="2026-09-01T00:00:00+00:00", closes_at="2026-09-30T00:00:00+00:00")
    store.create_channel(
        PERMANENTE, kind="permanente", title="Buzón permanente",
        question="¿Qué te gustaría escuchar en el canal?",
        restrictions="Sin restricciones de fecha.",
        criteria="Se valoran propuestas concretas y realizables.",
        selected_count=1, opens_at="2026-09-01T00:00:00+00:00", closes_at=None)
    return store


def submission(n: int, channel_id: str = CONVOCATORIA, **overrides) -> dict:
    base = {
        "what": f"[{domain.SYNTHETIC_MARK}] Propongo un episodio sobre el tema número {n}.",
        "why": f"Aporta porque responde una duda frecuente del chat, caso {n}.",
        "example": "",
        "author": f"Participante {n}",
        "contact": f"participante{n}.sintetico@example.invalid",
    }
    base.update(overrides)
    return {"channel_id": channel_id, **base}


CAPABILITY = "c" * 43


@pytest.fixture()
def anyio_backend():
    return "asyncio"


@pytest.fixture()
def clock():
    """A clock that advances one minute per call, so evidence keeps a stable order."""
    state = {"n": 0}

    def tick() -> str:
        state["n"] += 1
        return f"2026-09-12T10:{state['n']:02d}:00+00:00"

    return tick


@pytest.fixture()
def serve(circuito, clock):
    """Run the real application on a free local port."""
    import socket
    import threading
    import time

    import uvicorn

    from circuit.app import build_app

    servers = []

    def start(exposed: bool = False) -> str:
        with socket.socket() as probe:
            probe.bind(("127.0.0.1", 0))
            port = probe.getsockname()[1]
        app = build_app(circuito, CAPABILITY, public_base=f"http://127.0.0.1:{port}",
                        exposed=exposed, clock=clock)
        server = uvicorn.Server(uvicorn.Config(app, host="127.0.0.1", port=port,
                                               log_level="warning"))
        thread = threading.Thread(target=server.run, daemon=True)
        thread.start()
        deadline = time.time() + 10
        while not server.started and time.time() < deadline:
            time.sleep(0.05)
        assert server.started
        servers.append((server, thread))
        return f"http://127.0.0.1:{port}"

    yield start
    for server, thread in servers:
        server.should_exit = True
        thread.join(timeout=10)
