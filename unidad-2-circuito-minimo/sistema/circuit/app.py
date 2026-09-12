"""Composition of the three surfaces into one application.

They share one process and one store because they are one circuit: what the audience sends on
the public surface is what the creator's AI reads through MCP and what the creator authorizes
on the panel.

The two wrappers around it are the ones U1 showed to be necessary: no server-initiated event
stream, because the forwarding service used for the real run does not support it, and a log of
every request, because when a real connection fails that log is what tells apart a request that
never arrived from one the system refused.
"""

import json
from datetime import datetime, timezone

from mcp.server.transport_security import TransportSecuritySettings

from circuit import access, auth, creator, panel, public
from circuit.store import Store


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def build_app(store: Store, capability: str, public_base: str = "", exposed: bool = False,
              clock=utc_now):
    """Build the ASGI application.

    ``exposed`` turns off DNS rebinding protection: behind a forwarding service the Host and
    Origin headers are set by third parties, and refusing them would make a refusal of ours look
    like an incompatibility of the account. What gates the connector is the access token; what
    gates the panel is the capability in its path.
    """
    access.check(capability)
    authorization = auth.CreatorAuthorization(store=store, capability=capability,
                                              public_base=public_base or "")
    server = creator.build_server(store, capability, public_base, clock,
                                  authorization=authorization)
    routes = (public.public_routes(store, clock)
              + panel.panel_routes(store, capability, clock, authorization))
    for path, methods, handler in routes:
        server.custom_route(path, methods=methods)(handler)

    security = TransportSecuritySettings(
        enable_dns_rebinding_protection=not exposed,
        allowed_hosts=["127.0.0.1:*", "localhost:*", "[::1]:*"],
        allowed_origins=[])
    mcp_path = access.MCP_PATH
    app = server.streamable_http_app(streamable_http_path=mcp_path, json_response=True,
                                     stateless_http=True, transport_security=security)
    return RequestLog(NoStandaloneStream(app, mcp_path), store, mcp_path, clock)


class NoStandaloneStream:
    """Answer 405 to GET on the MCP endpoint.

    The streamable HTTP transport allows a server with no server-initiated event stream to
    refuse that GET, and U1 measured that the tunnel used for the real run does not support
    SSE. Any other path falls through, so a wrong capability sees 404 and never a 405.
    """

    def __init__(self, app, mcp_path: str):
        self.app, self.mcp_path = app, mcp_path

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http" and scope["method"] == "GET" and scope["path"] == self.mcp_path:
            await send({"type": "http.response.start", "status": 405, "headers": [(b"allow", b"POST")]})
            await send({"type": "http.response.body", "body": b""})
            return
        await self.app(scope, receive, send)


class RequestLog:
    """Record every HTTP request that reaches the system, without ever storing the path.

    The path of the two private surfaces carries the capability, so what is stored is which
    surface answered, the method, the status and the headers that identify the client.
    """

    def __init__(self, app, store: Store, mcp_path: str, clock):
        self.app, self.store, self.mcp_path, self.clock = app, store, mcp_path, clock

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        headers = {k.decode("latin-1").lower(): v.decode("latin-1") for k, v in scope.get("headers", [])}
        path = scope["path"]
        is_mcp = path == self.mcp_path
        surface = "mcp" if is_mcp else ("panel" if path.startswith("/creador/") else "publica")
        rpc, inner_receive = "", receive
        if is_mcp and scope["method"] == "POST":
            messages, more = [], True
            while more:
                message = await receive()
                messages.append(message)
                more = message.get("more_body", False)
            rpc = _rpc_methods(b"".join(m.get("body", b"") for m in messages))
            replay = iter(messages)

            async def inner_receive():
                return next(replay, None) or await receive()

        logged = False

        async def logging_send(message):
            nonlocal logged
            if message["type"] == "http.response.start" and not logged:
                logged = True
                self._record(surface, scope["method"], is_mcp, message["status"], rpc, headers)
            await send(message)

        try:
            await self.app(scope, inner_receive, logging_send)
        finally:
            if not logged:
                self._record(surface, scope["method"], is_mcp, 500, rpc, headers)

    def _record(self, surface, method, path_ok, status, rpc, headers):
        self.store.log_request(self.clock(), surface, method, path_ok, status, rpc,
                               headers.get("host", ""), headers.get("origin", ""),
                               headers.get("user-agent", ""))


def _rpc_methods(raw: bytes) -> str:
    try:
        payload = json.loads(raw or b"null")
    except ValueError:
        return "invalid-json"
    items = payload if isinstance(payload, list) else [payload]
    return ",".join(i.get("method", "response") for i in items if isinstance(i, dict))
