"""Construction tests for the authorization of the connector.

They exercise mechanisms of the candidate, not the cases of PLAN.md: whether a real host
completes this flow is what the contract of the real run has to show.
"""

import base64
import hashlib
import secrets
from urllib.parse import parse_qs, urlparse

import httpx
import pytest

from circuit import access, auth
from tests.conftest import CAPABILITY

INIT = {"jsonrpc": "2.0", "id": 1, "method": "initialize",
        "params": {"protocolVersion": "2025-06-18", "capabilities": {},
                   "clientInfo": {"name": "test", "version": "0"}}}
MCP_HEADERS = {"Accept": "application/json, text/event-stream", "Content-Type": "application/json"}


@pytest.fixture()
def creador(serve):
    """A browser that already reached the panel, which is what opens the creator's session."""
    base = serve()
    with httpx.Client(base_url=base, timeout=30, follow_redirects=False) as client:
        assert client.get(access.panel_path(CAPABILITY)).status_code == 200
        client.base = base
        yield client


def _register(base: str, name: str = "app-de-prueba") -> tuple[str, str]:
    redirect = f"{base}{access.panel_path(CAPABILITY)}/listo"
    answer = httpx.post(f"{base}/register", json={
        "client_name": name, "redirect_uris": [redirect],
        "grant_types": ["authorization_code", "refresh_token"], "response_types": ["code"],
        "token_endpoint_auth_method": "none", "scope": auth.SCOPE}, timeout=30)
    assert answer.status_code < 400, answer.text
    return answer.json()["client_id"], redirect


def _ask(base: str, client_id: str, redirect: str) -> tuple[str, str]:
    verifier = secrets.token_urlsafe(43)
    challenge = base64.urlsafe_b64encode(
        hashlib.sha256(verifier.encode()).digest()).decode().rstrip("=")
    asked = httpx.get(f"{base}/authorize", params={
        "response_type": "code", "client_id": client_id, "redirect_uri": redirect,
        "code_challenge": challenge, "code_challenge_method": "S256", "state": "xyz",
        "scope": auth.SCOPE}, follow_redirects=False, timeout=30)
    assert asked.status_code == 302, asked.text
    request_id = parse_qs(urlparse(asked.headers["location"]).query)["solicitud"][0]
    return request_id, verifier


def _approve(client: httpx.Client, request_id: str) -> httpx.Response:
    return client.post(auth.CONSENT_PATH, data={"solicitud": request_id})


def _exchange(base: str, client_id: str, redirect: str, code: str, verifier: str) -> httpx.Response:
    return httpx.post(f"{base}/token", data={
        "grant_type": "authorization_code", "code": code, "redirect_uri": redirect,
        "client_id": client_id, "code_verifier": verifier}, timeout=30)


def _code_of(response: httpx.Response) -> str:
    return parse_qs(urlparse(response.headers["location"]).query)["code"][0]


def test_registering_a_client_grants_nothing(circuito, serve):
    base = serve()
    client_id, _ = _register(base)
    assert circuito.get_oauth_client(client_id) is not None
    assert circuito.issued_tokens() == []
    assert httpx.post(base + access.MCP_PATH, json=INIT, headers=MCP_HEADERS).status_code == 401


def test_a_connection_request_waits_for_the_creator(circuito, serve):
    base = serve()
    client_id, redirect = _register(base)
    request_id, _ = _ask(base, client_id, redirect)
    pending = circuito.pending_authorization_requests()
    assert [p["id"] for p in pending] == [request_id]
    assert circuito.issued_tokens() == []


def test_the_consent_page_says_who_is_asking_and_what_it_would_get(circuito, creador):
    base = creador.base
    client_id, redirect = _register(base, name="ChatGPT de prueba")
    request_id, _ = _ask(base, client_id, redirect)
    page = creador.get(auth.CONSENT_PATH, params={"solicitud": request_id}).text
    assert "ChatGPT de prueba" in page
    assert auth.SCOPE in page
    assert "sin tu aprobación" in page
    assert "sigue siendo tuyo" in page


def test_the_creators_approval_is_what_issues_the_code(circuito, creador):
    base = creador.base
    client_id, redirect = _register(base)
    request_id, _ = _ask(base, client_id, redirect)
    approved = _approve(creador, request_id)
    assert approved.status_code == 303
    assert _code_of(approved)
    assert parse_qs(urlparse(approved.headers["location"]).query)["state"] == ["xyz"]


def test_a_request_cannot_be_approved_twice(circuito, creador):
    base = creador.base
    client_id, redirect = _register(base)
    request_id, _ = _ask(base, client_id, redirect)
    assert _approve(creador, request_id).status_code == 303
    again = _approve(creador, request_id)
    assert again.status_code == 400
    assert "ya fue aprobada" in again.text


def test_the_authorization_code_is_spent_once(circuito, creador):
    base = creador.base
    client_id, redirect = _register(base)
    request_id, verifier = _ask(base, client_id, redirect)
    code = _code_of(_approve(creador, request_id))
    assert _exchange(base, client_id, redirect, code, verifier).status_code == 200
    assert _exchange(base, client_id, redirect, code, verifier).status_code >= 400


def test_a_wrong_verifier_does_not_get_a_token(circuito, creador):
    base = creador.base
    client_id, redirect = _register(base)
    request_id, _ = _ask(base, client_id, redirect)
    code = _code_of(_approve(creador, request_id))
    assert _exchange(base, client_id, redirect, code,
                     secrets.token_urlsafe(43)).status_code >= 400


def test_the_token_is_what_opens_the_connector(circuito, creador):
    base = creador.base
    client_id, redirect = _register(base)
    request_id, verifier = _ask(base, client_id, redirect)
    code = _code_of(_approve(creador, request_id))
    token = _exchange(base, client_id, redirect, code, verifier).json()["access_token"]

    call = {"jsonrpc": "2.0", "id": 2, "method": "tools/call",
            "params": {"name": "estado_del_sistema", "arguments": {}}}
    opened = httpx.post(base + access.MCP_PATH, json=call,
                        headers={**MCP_HEADERS, "Authorization": f"Bearer {token}"}, timeout=30)
    assert opened.status_code == 200
    assert "confirmado" in opened.text


def test_a_revoked_token_stops_opening_the_connector(circuito, creador):
    base = creador.base
    client_id, redirect = _register(base)
    request_id, verifier = _ask(base, client_id, redirect)
    code = _code_of(_approve(creador, request_id))
    token = _exchange(base, client_id, redirect, code, verifier).json()["access_token"]
    circuito.revoke_oauth_token(token)

    refused = httpx.post(base + access.MCP_PATH, json=INIT,
                         headers={**MCP_HEADERS, "Authorization": f"Bearer {token}"}, timeout=30)
    assert refused.status_code == 401


def test_the_creator_sees_the_connections_on_the_panel(circuito, creador):
    base = creador.base
    client_id, redirect = _register(base, name="app-listada")
    request_id, _ = _ask(base, client_id, redirect)
    _approve(creador, request_id)
    panel = httpx.get(base + access.panel_path(CAPABILITY), timeout=30).text
    assert "app-listada" in panel


def test_the_consent_url_handed_to_the_agent_carries_no_secret(circuito, serve):
    base = serve()
    client_id, redirect = _register(base)
    asked = httpx.get(f"{base}/authorize", params={
        "response_type": "code", "client_id": client_id, "redirect_uri": redirect,
        "code_challenge": "x" * 43, "code_challenge_method": "S256", "state": "xyz",
        "scope": auth.SCOPE}, follow_redirects=False, timeout=30)
    destination = asked.headers["location"]
    assert CAPABILITY not in destination
    assert destination.startswith(f"{base}{auth.CONSENT_PATH}?")


def test_without_the_creators_session_the_consent_page_shows_nothing(circuito, serve):
    base = serve()
    client_id, redirect = _register(base, name="app-que-espia")
    request_id, _ = _ask(base, client_id, redirect)

    blind = httpx.get(f"{base}{auth.CONSENT_PATH}", params={"solicitud": request_id}, timeout=30)
    assert blind.status_code == 403
    assert "app-que-espia" not in blind.text
    assert CAPABILITY not in blind.text


def test_without_the_creators_session_nobody_can_approve(circuito, serve):
    base = serve()
    client_id, redirect = _register(base)
    request_id, _ = _ask(base, client_id, redirect)

    refused = httpx.post(f"{base}{auth.CONSENT_PATH}", data={"solicitud": request_id},
                         follow_redirects=False, timeout=30)
    assert refused.status_code == 403
    assert circuito.issued_tokens() == []
    assert [p["id"] for p in circuito.pending_authorization_requests()] == [request_id]


def test_the_creator_can_cut_off_a_connection_from_the_panel(circuito, creador):
    base = creador.base
    client_id, redirect = _register(base, name="app-a-revocar")
    request_id, verifier = _ask(base, client_id, redirect)
    code = _code_of(_approve(creador, request_id))
    token = _exchange(base, client_id, redirect, code, verifier).json()["access_token"]

    panel = creador.get(access.panel_path(CAPABILITY)).text
    assert "Revocar esta conexión" in panel

    creador.post(f"{access.panel_path(CAPABILITY)}/revocar", data={"client_id": client_id})
    refused = httpx.post(base + access.MCP_PATH, json=INIT,
                         headers={**MCP_HEADERS, "Authorization": f"Bearer {token}"}, timeout=30)
    assert refused.status_code == 401
    assert all(t["revoked_at"] for t in circuito.token_ledger())
