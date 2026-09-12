"""The creator's panel.

U1 measured that a write executes without any confirmation from ChatGPT, so the authorization
of a consequential action cannot live in the conversation. It lives here: the creator reviews
the calibration of their criteria and grants publication and invitation on a surface of the
system itself. The AI can ask, and can read the answer, but it cannot grant.

The panel is gated by the same capability as the MCP endpoint: its path comes from ``access``,
so a request without the capability matches no route at all.
"""

from starlette.responses import HTMLResponse, RedirectResponse

from circuit import access, auth as auth_module, domain, evaluation
from circuit.store import ClosedChannelError, NotAuthorizedError, NotFoundError, Store
from circuit.web import esc, field, notice, page


def panel_routes(store: Store, capability: str, clock, authorization=None) -> list[tuple]:
    base = access.panel_path(capability)

    async def _form(request) -> dict:
        from circuit.public import _form as parse
        return await parse(request)

    async def panel(request):
        body = ("<h1>Panel del creador</h1>"
                + notice("Publicar e invitar se autorizan acá, en el sistema. La IA puede "
                         "pedirlo; darlo es tuyo.")
                + _connections_block(store, base))
        for channel in store.all_channels():
            body += _channel_block(store, base, channel)
            for round_ in store.rounds_of(channel["id"]):
                body += _round_block(store, base, round_)
        return HTMLResponse(page("Panel del creador", body))

    async def approve_calibration(request):
        """Approving the interpretation is what opens the channel to participation."""
        form = await _form(request)
        try:
            store.approve_calibration(form.get("channel_id", ""), at=clock())
        except (NotFoundError, ClosedChannelError) as exc:
            return HTMLResponse(page("No se pudo aprobar", "<h1>No se pudo aprobar</h1>"
                                     + notice(str(exc), "aviso error")), status_code=400)
        return RedirectResponse(base, status_code=303)

    async def return_calibration(request):
        form = await _form(request)
        try:
            store.return_calibration(form.get("channel_id", ""), at=clock(),
                                     correction=form.get("correction", ""))
        except (NotFoundError, ValueError) as exc:
            return HTMLResponse(page("No se pudo devolver", "<h1>No se pudo devolver</h1>"
                                     + notice(str(exc), "aviso error")), status_code=400)
        return RedirectResponse(base, status_code=303)

    async def authorize(request):
        form = await _form(request)
        try:
            store.authorize(form.get("round_id", ""), form.get("kind", ""), at=clock())
        except (NotFoundError, ValueError) as exc:
            return HTMLResponse(page("No se pudo autorizar", "<h1>No se pudo autorizar</h1>"
                                     + notice(str(exc), "aviso error")), status_code=400)
        return RedirectResponse(base, status_code=303)

    async def choice(request):
        form = await _form(request)
        chosen = [pid.strip() for pid in form.get("proposal_ids", "").split(",") if pid.strip()]
        try:
            store.set_creator_choice(form.get("round_id", ""), chosen, at=clock())
        except NotFoundError as exc:
            return HTMLResponse(page("No se pudo registrar", "<h1>No se pudo registrar</h1>"
                                     + notice(str(exc), "aviso error")), status_code=400)
        return RedirectResponse(base, status_code=303)

    async def connect(request):
        """The consent surface of the authorization flow.

        A client that wants to operate the circuit lands here, and the creator is whoever can
        reach this page. Approving is what issues the code the client then exchanges for a
        token; until that happens the client holds nothing.
        """
        request_id = request.query_params.get("solicitud", "")
        if request.method == "GET":
            try:
                pending = auth_module.pending_request_view(store, request_id)
            except NotFoundError as exc:
                return HTMLResponse(page("Solicitud no encontrada", "<h1>Solicitud no encontrada</h1>"
                                         + notice(str(exc), "aviso error")), status_code=404)
            if pending["approved_at"]:
                return HTMLResponse(page("Ya aprobada", "<h1>Ya aprobada</h1>" + notice(
                    "Esta solicitud de conexión ya fue aprobada.")))
            body = (f"<h1>Conectar «{esc(pending['client_name'])}»</h1>"
                    f"<p>Una aplicación pide operar tu circuito en tu nombre.</p>"
                    f"<p><strong>Qué podrá hacer:</strong> leer propuestas, guardar evaluaciones y "
                    f"pedirte autorización para invitar y publicar. Autorizar esas dos acciones "
                    f"sigue siendo tuyo, acá en el panel.</p>"
                    f"<p><strong>Alcance:</strong> {esc(', '.join(pending['scopes']))}</p>"
                    f"<p><strong>Volverá a:</strong> {esc(pending['redirect_uri'])}</p>"
                    f"<p><strong>Pedida el:</strong> {esc(pending['created_at'])}</p>"
                    + notice("Si no reconocés esta solicitud, cerrá esta página: sin tu "
                             "aprobación la aplicación no obtiene ningún acceso.")
                    + f'<form method="post" action="{esc(base)}/conectar">'
                      f'<input type="hidden" name="solicitud" value="{esc(request_id)}">'
                      '<button type="submit">Autorizar esta conexión</button></form>')
            return HTMLResponse(page("Conectar una aplicación", body))

        form = await _form(request)
        try:
            destination = authorization.approve(form.get("solicitud", ""), at=clock())
        except (NotFoundError, NotAuthorizedError) as exc:
            return HTMLResponse(page("No se pudo autorizar", "<h1>No se pudo autorizar</h1>"
                                     + notice(str(exc), "aviso error")), status_code=400)
        return RedirectResponse(destination, status_code=303)

    return [
        (base, ["GET"], panel),
        (f"{base}/conectar", ["GET", "POST"], connect),
        (f"{base}/calibracion/aprobar", ["POST"], approve_calibration),
        (f"{base}/calibracion/devolver", ["POST"], return_calibration),
        (f"{base}/autorizar", ["POST"], authorize),
        (f"{base}/eleccion", ["POST"], choice),
    ]


def _connections_block(store: Store, base: str) -> str:
    """What the creator authorized to connect, and what is still waiting for them."""
    connections = store.connections()
    if not connections:
        return ""
    body = "<h2>Aplicaciones conectadas</h2><ul>"
    for connection in connections:
        estado = (f"autorizada el {esc(connection['approved_at'])}" if connection["approved_at"]
                  else "esperando tu decisión")
        body += f"<li>{esc(connection['client_name'])}: {estado}</li>"
    body += "</ul>"
    pendientes = [c for c in connections if not c["approved_at"]]
    for pendiente in pendientes:
        body += (f'<p><a href="{esc(base)}/conectar?solicitud={esc(pendiente["id"])}">'
                 f'Revisar la solicitud de {esc(pendiente["client_name"])}</a></p>')
    return body


def _channel_block(store: Store, base: str, channel: dict) -> str:
    body = (f"<h2>{esc(channel['title'])}</h2>"
            f"<p>Canal <strong>{esc(channel['kind'])}</strong> ({esc(channel['id'])}), "
            f"{esc(channel['status'])}. Se seleccionan {esc(channel['selected_count'])}.</p>"
            f"<p><strong>Criterios vigentes:</strong> {esc(channel['criteria'])}</p>")
    if channel["status"] == "preparacion":
        body += notice("Este canal todavía no recibe propuestas. Se abre cuando aprobás la "
                       "interpretación de tus criterios.")
    try:
        calibration = store.get_calibration(channel["id"])
    except NotFoundError:
        return body + notice("Todavía no hay una interpretación de tus criterios para revisar. "
                             "Pedísela a tu IA: sin eso el canal no se abre.")
    body += ("<h3>Interpretación de tus criterios</h3>"
             f"<p>{esc(calibration['interpretation'])}</p><h3>Ejemplos explicados</h3><ul>")
    for example in calibration["examples"]:
        body += (f"<li><strong>{esc(example.get('resultado', ''))}</strong>: "
                 f"{esc(example.get('propuesta', ''))} — {esc(example.get('explicacion', ''))}</li>")
    body += "</ul>"
    if calibration["correction"]:
        body += notice(f"Discrepancia que registraste: {esc(calibration['correction'])}")
    if calibration["reviewed_at"]:
        body += notice(f"Aprobada el {esc(calibration['reviewed_at'])}: con eso se abrió el canal.")
    else:
        body += (f'<form method="post" action="{esc(base)}/calibracion/aprobar">'
                 f'<input type="hidden" name="channel_id" value="{esc(channel["id"])}">'
                 '<button type="submit">Aprobar la interpretación y abrir el canal</button></form>'
                 f'<form method="post" action="{esc(base)}/calibracion/devolver">'
                 f'<input type="hidden" name="channel_id" value="{esc(channel["id"])}">'
                 + field("O devolvela con la discrepancia", "correction", "", "textarea",
                         "queda registrada y el canal sigue sin abrirse", 600, False)
                 + '<button type="submit">Devolver sin abrir</button></form>')
    return body


def _round_block(store: Store, base: str, round_: dict) -> str:
    proposals = store.round_proposals(round_["id"])
    signals = store.signals(round_["id"])
    body = (f"<h3>Ronda {esc(round_['id'])}</h3>"
            f"<p>Corte: {esc(round_['cut_at'])}. Propuestas: {esc(len(proposals))}. "
            f"Criterios congelados: {esc(round_['criteria']['criteria'])}</p>")
    body += notice(evaluation.result_notice())
    for kind in ("invitar", "publicar"):
        if store.is_authorized(round_["id"], kind):
            body += f"<p>Autorizado: <strong>{esc(kind)}</strong>.</p>"
        else:
            body += (f'<form method="post" action="{esc(base)}/autorizar">'
                     f'<input type="hidden" name="round_id" value="{esc(round_["id"])}">'
                     f'<input type="hidden" name="kind" value="{esc(kind)}">'
                     f'<button type="submit">Autorizar {esc(kind)} en esta ronda</button></form>')
    body += (f"<p><strong>Recomendación de la IA:</strong> "
             f"{esc(', '.join(signals['ia']) or 'sin preselección')}</p>"
             f'<form method="post" action="{esc(base)}/eleccion">'
             f'<input type="hidden" name="round_id" value="{esc(round_["id"])}">'
             + field("Tu elección (identificadores separados por coma)", "proposal_ids",
                     ", ".join(signals["creador"]), "text",
                     "es una señal propia y no se suma a las otras", 200, False)
             + '<button type="submit">Registrar mi elección</button></form>')
    finalists = store.finalists(round_["id"])
    if finalists:
        body += (f"<p>Publicadas: {esc(', '.join(f['id'] for f in finalists))}. "
                 f"{esc(domain.reception_label(finalists[0]['received_at']))} para la primera.</p>")
    return body
