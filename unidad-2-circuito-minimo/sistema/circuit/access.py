"""The access boundary of the creator's surfaces.

U1 demonstrated the connection with a capability in the URL and recorded, as a limit, that a
bearer secret in a URL is not fit for the product. This module is the single place that decides
how the creator's two private surfaces — the MCP endpoint and the authorization panel — are
gated, so replacing it with a real authorization flow does not touch the circuit.

What it deliberately does not do is decide that question. No case of U2 exercises the
authentication of the endpoint, and U1 did not demonstrate that OAuth works in the account that
was probed, so choosing it here would be freezing a mechanism without the evidence that decides
it. ARQUITECTURA.md records the decision and routes it.
"""

import re
import secrets

_CAPABILITY = re.compile(r"^[A-Za-z0-9_-]{32,}$")


class InvalidCapability(ValueError):
    """The capability does not have the expected shape."""


def new_capability() -> str:
    """Generate a capability locally. It is never written to Git nor to distributed material."""
    return secrets.token_urlsafe(32)


def check(capability: str) -> str:
    if not _CAPABILITY.match(capability or ""):
        raise InvalidCapability("La capacidad debe tener al menos 32 caracteres seguros para URL.")
    return capability


def mcp_path(capability: str) -> str:
    return f"/mcp/{check(capability)}"


def panel_path(capability: str) -> str:
    return f"/creador/{check(capability)}"
