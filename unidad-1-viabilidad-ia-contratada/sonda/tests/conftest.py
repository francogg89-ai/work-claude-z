import pytest

from probe.store import Store, generate_dataset


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
def store(tmp_path):
    s = Store(tmp_path / "probe.sqlite")
    s.seed(generate_dataset())
    yield s
    s.close()
