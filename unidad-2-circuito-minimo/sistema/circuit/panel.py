"""The creator's panel.

U1 measured that a write executes without any confirmation from ChatGPT, so the authorization
of a consequential action cannot live in the conversation. It lives here: the creator reviews
the calibration of their criteria and grants publication and invitation on a surface of the
system itself. The AI can ask, and can read the answer, but it cannot grant.

The panel is gated by the same capability as the MCP endpoint: its path comes from ``access``,
so a request without the capability matches no route at all.
"""

from starlette.responses import HTMLResponse, RedirectResponse

from circuit import access, domain, evaluation
from circuit.store import NotFoundError, Store
from circuit.web import esc, field, notice, page


def panel_routes(store: Store, capability: str, clock) -> list[tuple]:
    base = access.panel_path(capability)

    async def _form(request) -> dict:
        from circuit.public import _form as parse
        return await parse(request)

    async def panel(request):
        body = ("<h1>Panel del creador</h1>"
                + notice("Publicar e invitar se autorizan acá, en el sistema. La IA puede "
                         "pedirlo; darlo es tuyo."))
        for channel in store.all_channels():
            body += _channel_block(store, base, channel)
            for round_ in store.rounds_of(channel["id"]):
                body += _round_block(store, base, round_)
        return HTMLResponse(page("Panel del creador", body))

    async def review_calibration(request):
        form = await _form(request)
        try:
            store.review_calibration(form.get("channel_id", ""), at=clock(),
                                     correction=form.get("correction", "").strip())
        except NotFoundError as exc:
            return HTMLResponse(page("No se pudo revisar", "<h1>No se pudo revisar</h1>"
                                     + notice(str(exc), "aviso error")), status_code=404)
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

    return [
        (base, ["GET"], panel),
        (f"{base}/calibracion", ["POST"], review_calibration),
        (f"{base}/autorizar", ["POST"], authorize),
        (f"{base}/eleccion", ["POST"], choice),
    ]


def _channel_block(store: Store, base: str, channel: dict) -> str:
    body = (f"<h2>{esc(channel['title'])}</h2>"
            f"<p>Canal <strong>{esc(channel['kind'])}</strong> ({esc(channel['id'])}), "
            f"{esc(channel['status'])}. Se seleccionan {esc(channel['selected_count'])}.</p>"
            f"<p><strong>Criterios vigentes:</strong> {esc(channel['criteria'])}</p>")
    try:
        calibration = store.get_calibration(channel["id"])
    except NotFoundError:
        return body + notice("Todavía no hay una interpretación de tus criterios para revisar. "
                             "Pedísela a tu IA antes de cortar la ronda.")
    body += ("<h3>Interpretación de tus criterios</h3>"
             f"<p>{esc(calibration['interpretation'])}</p><h3>Ejemplos explicados</h3><ul>")
    for example in calibration["examples"]:
        body += (f"<li><strong>{esc(example.get('resultado', ''))}</strong>: "
                 f"{esc(example.get('propuesta', ''))} — {esc(example.get('explicacion', ''))}</li>")
    body += "</ul>"
    if calibration["reviewed_at"]:
        body += notice(f"Revisada el {esc(calibration['reviewed_at'])}."
                       + (f" Corrección registrada: {calibration['correction']}"
                          if calibration["correction"] else ""))
    else:
        body += (f'<form method="post" action="{esc(base)}/calibracion">'
                 f'<input type="hidden" name="channel_id" value="{esc(channel["id"])}">'
                 + field("Discrepancia que quieras corregir (opcional)", "correction", "",
                         "textarea", "queda registrada junto a la interpretación", 600, False)
                 + '<button type="submit">Revisado: puedo cortar la ronda</button></form>')
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
