import socket
import threading
import time

import pytest
import uvicorn

from probe.server import build_app
from probe.store import Store, generate_dataset

TOKEN = "t" * 43


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
def store(tmp_path):
    s = Store(tmp_path / "probe.sqlite")
    s.seed(generate_dataset())
    yield s
    s.close()


def _free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture
def serve(store):
    """Start the real ASGI app on a free local port; yields a factory taking public=True/False."""
    servers = []

    def start(public: bool) -> str:
        port = _free_port()
        server = uvicorn.Server(uvicorn.Config(build_app(store, TOKEN, public=public),
                                               host="127.0.0.1", port=port, log_level="warning"))
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
