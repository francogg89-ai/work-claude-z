"""The authorization server of the system, so the connector stops depending on a URL secret.

U1 closed with the capability in the URL and recorded that a bearer secret in a URL is not fit
for the product. The product admits exactly two ways of connecting an app of one's own —a public
URL with no authentication, or OAuth— so «authentication without a secret in the URL» is the MCP
authorization flow and nothing else. This module is that flow.

The shape is deliberate in one respect. The resource owner here is the creator, and the creator
already has one private surface: their panel. So consent is not a new login screen with new
credentials to keep; it is one more decision on the panel, next to the ones that authorize
publishing and inviting. The AI asks, the creator grants, and the token is what the connector
carries from then on.

Nothing here validates the creator's identity beyond reaching the panel. That is the same
boundary the panel already had, and it does not travel to the connector: whoever holds a token
can operate the circuit, and whoever does not holds nothing.
"""

import secrets
import time
from dataclasses import dataclass

from mcp.server.auth.provider import (
    AccessToken,
    AuthorizationCode,
    AuthorizationParams,
    OAuthAuthorizationServerProvider,
    RefreshToken,
    construct_redirect_uri,
)
from mcp.server.auth.settings import AuthSettings, ClientRegistrationOptions, RevocationOptions
from mcp.shared.auth import OAuthClientInformationFull, OAuthToken

from circuit import access
from circuit.store import Store

SCOPE = "circuito"
CODE_TTL_SECONDS = 300
TOKEN_TTL_SECONDS = 60 * 60 * 8
REFRESH_TTL_SECONDS = 60 * 60 * 24 * 30


def auth_settings(public_base: str) -> AuthSettings:
    """How the server describes itself to a client that has to authorize against it."""
    return AuthSettings(
        issuer_url=public_base,
        resource_server_url=f"{public_base}{access.MCP_PATH}",
        # The authorization server and the resource server are the same process here, so a token
        # cannot have been issued for another resource. Checking the indicator would only reject
        # clients that do not send one.
        validate_token_resource=False,
        required_scopes=[SCOPE],
        client_registration_options=ClientRegistrationOptions(
            enabled=True, valid_scopes=[SCOPE], default_scopes=[SCOPE]),
        revocation_options=RevocationOptions(enabled=True),
    )


@dataclass
class CreatorAuthorization(OAuthAuthorizationServerProvider[AuthorizationCode, RefreshToken,
                                                            AccessToken]):
    """Authorization server backed by the store, with the creator's panel as the consent surface."""

    store: Store
    capability: str
    public_base: str

    # ------------------------------------------------------------------------------- clients

    async def get_client(self, client_id: str) -> OAuthClientInformationFull | None:
        raw = self.store.get_oauth_client(client_id)
        return OAuthClientInformationFull.model_validate(raw) if raw else None

    async def register_client(self, client_info: OAuthClientInformationFull) -> None:
        """Accept a client the host registers by itself, which is how the product connects.

        Registering is not authorizing: a registered client holds nothing until the creator
        approves it on the panel.
        """
        self.store.save_oauth_client(client_info.client_id,
                                     client_info.model_dump(mode="json", exclude_none=True))

    # ------------------------------------------------------------------- authorization request

    async def authorize(self, client: OAuthClientInformationFull,
                        params: AuthorizationParams) -> str:
        """Park the request and send the client to the creator's panel to decide."""
        request_id = f"SOL-{secrets.token_hex(8)}"
        self.store.save_authorization_request(request_id, client.client_id, {
            "state": params.state,
            "scopes": params.scopes or [SCOPE],
            "code_challenge": params.code_challenge,
            "redirect_uri": str(params.redirect_uri),
            "redirect_uri_provided_explicitly": params.redirect_uri_provided_explicitly,
            "resource": params.resource,
            "client_name": client.client_name or client.client_id,
        })
        return f"{self.public_base}{access.panel_path(self.capability)}/conectar?solicitud={request_id}"

    def approve(self, request_id: str, at: str) -> str:
        """The creator approves on the panel: issue the code and build the redirect back.

        Not a coroutine: it is called from the panel, which is ordinary request handling, and it
        is the only place where an authorization code is born.
        """
        pending = self.store.take_authorization_request(request_id, at)
        code = secrets.token_urlsafe(32)
        self.store.save_authorization_code(code, pending["client_id"], {
            "code": code,
            "scopes": pending["params"]["scopes"],
            "expires_at": time.time() + CODE_TTL_SECONDS,
            "client_id": pending["client_id"],
            "code_challenge": pending["params"]["code_challenge"],
            "redirect_uri": pending["params"]["redirect_uri"],
            "redirect_uri_provided_explicitly":
                pending["params"]["redirect_uri_provided_explicitly"],
            "resource": pending["params"]["resource"],
            "subject": "creador",
        })
        return construct_redirect_uri(pending["params"]["redirect_uri"], code=code,
                                      state=pending["params"]["state"])

    # ------------------------------------------------------------------------- code and tokens

    async def load_authorization_code(self, client: OAuthClientInformationFull,
                                      authorization_code: str) -> AuthorizationCode | None:
        raw = self.store.get_authorization_code(authorization_code)
        if raw is None or raw["client_id"] != client.client_id:
            return None
        if raw["data"]["expires_at"] < time.time():
            return None
        return AuthorizationCode.model_validate(raw["data"])

    async def exchange_authorization_code(self, client: OAuthClientInformationFull,
                                          authorization_code: AuthorizationCode) -> OAuthToken:
        """Spend the code once and issue the pair of tokens."""
        self.store.spend_authorization_code(authorization_code.code)
        access_token = secrets.token_urlsafe(32)
        refresh_token = secrets.token_urlsafe(32)
        self.store.save_oauth_token(access_token, "acceso", client.client_id,
                                    authorization_code.scopes,
                                    int(time.time()) + TOKEN_TTL_SECONDS,
                                    authorization_code.resource)
        self.store.save_oauth_token(refresh_token, "refresco", client.client_id,
                                    authorization_code.scopes,
                                    int(time.time()) + REFRESH_TTL_SECONDS,
                                    authorization_code.resource)
        return OAuthToken(access_token=access_token, token_type="Bearer",
                          expires_in=TOKEN_TTL_SECONDS,
                          scope=" ".join(authorization_code.scopes),
                          refresh_token=refresh_token)

    async def load_refresh_token(self, client: OAuthClientInformationFull,
                                 refresh_token: str) -> RefreshToken | None:
        raw = self._live_token(refresh_token, "refresco")
        if raw is None or raw["client_id"] != client.client_id:
            return None
        return RefreshToken(token=refresh_token, client_id=raw["client_id"],
                            scopes=raw["scopes"], expires_at=raw["expires_at"])

    async def exchange_refresh_token(self, client: OAuthClientInformationFull,
                                     refresh_token: RefreshToken,
                                     scopes: list[str]) -> OAuthToken:
        self.store.revoke_oauth_token(refresh_token.token)
        granted = scopes or refresh_token.scopes
        access_token = secrets.token_urlsafe(32)
        rotated = secrets.token_urlsafe(32)
        self.store.save_oauth_token(access_token, "acceso", client.client_id, granted,
                                    int(time.time()) + TOKEN_TTL_SECONDS, None)
        self.store.save_oauth_token(rotated, "refresco", client.client_id, granted,
                                    int(time.time()) + REFRESH_TTL_SECONDS, None)
        return OAuthToken(access_token=access_token, token_type="Bearer",
                          expires_in=TOKEN_TTL_SECONDS, scope=" ".join(granted),
                          refresh_token=rotated)

    async def load_access_token(self, token: str) -> AccessToken | None:
        raw = self._live_token(token, "acceso")
        if raw is None:
            return None
        return AccessToken(token=token, client_id=raw["client_id"], scopes=raw["scopes"],
                           expires_at=raw["expires_at"], resource=raw["resource"],
                           subject="creador")

    async def revoke_token(self, token: AccessToken | RefreshToken) -> None:
        self.store.revoke_oauth_token(token.token)

    def _live_token(self, token: str, kind: str) -> dict | None:
        raw = self.store.get_oauth_token(token)
        if raw is None or raw["kind"] != kind or raw["revoked_at"]:
            return None
        if raw["expires_at"] is not None and raw["expires_at"] < time.time():
            return None
        return raw


def pending_request_view(store: Store, request_id: str) -> dict:
    """What the creator has to see before deciding: who is asking and for what."""
    pending = store.get_authorization_request(request_id)
    return {"id": request_id, "client_name": pending["params"]["client_name"],
            "redirect_uri": pending["params"]["redirect_uri"],
            "scopes": pending["params"]["scopes"], "created_at": pending["created_at"],
            "approved_at": pending["approved_at"]}
