"""The access boundary of the creator's own surface.

U1 demonstrated the connection with a capability in the URL and recorded, as a limit, that a
bearer secret in a URL is not fit for the product. That limit is now answered where it was
raised: the connector's endpoint is gated by the authorization flow in `circuit.auth`, not by
its path.

What stays here is the capability of the creator's panel, which is a local surface and was never
what U1 flagged. It is also the consent surface of the authorization flow: reaching the panel is
what identifies the creator when a client asks to connect.
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


# The connector's endpoint carries no secret in its path: what gates it is the token the host
# obtained through the authorization flow in `circuit.auth`.
MCP_PATH = "/mcp"


def panel_path(capability: str) -> str:
    return f"/creador/{check(capability)}"
