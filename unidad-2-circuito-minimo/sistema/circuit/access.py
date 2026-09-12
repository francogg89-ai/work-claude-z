"""The access boundary of the creator's surfaces.

U1 demonstrated the connection with a capability in the URL and recorded, as a limit, that a
bearer secret in a URL is not fit for the product. This module is the single place that decides
how the creator's two private surfaces — the MCP endpoint and the authorization panel — are
gated, so replacing it with a real authorization flow does not touch the circuit.

The capability is not the answer to that: it is what the local verification runs on. The
mechanism that replaces it is the MCP authorization flow, and it arrives with the contract that
covers the real conversational operation, because only a real run shows the host completing it.
Every other module talks to this one, so that replacement does not touch the circuit.
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
