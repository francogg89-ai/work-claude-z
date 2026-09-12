"""Shared pieces of the HTML surfaces.

Everything a participant or a creator wrote is escaped before it reaches a page: the content of
a participant is untrusted in every direction, not only towards a model.
"""

from html import escape

_STYLE = """
  :root { color-scheme: light dark; }
  body { font-family: system-ui, sans-serif; margin: 0 auto; max-width: 44rem; padding: 1.5rem 1rem;
         line-height: 1.5; }
  h1, h2 { line-height: 1.2; }
  label { display: block; margin: 0.75rem 0 0.25rem; font-weight: 600; }
  input, textarea, select { width: 100%; box-sizing: border-box; padding: 0.4rem; font: inherit; }
  textarea { min-height: 4.5rem; }
  button { margin-top: 1rem; padding: 0.5rem 1rem; font: inherit; }
  .aviso { border-left: 3px solid currentColor; padding: 0.25rem 0 0.25rem 0.75rem; margin: 1rem 0; }
  .error { border-left-width: 5px; }
  .propuesta { border-top: 1px solid; padding-top: 0.75rem; margin-top: 1.25rem; }
  .senal { margin: 0.25rem 0; }
  .original { white-space: pre-wrap; }
  footer { margin-top: 2.5rem; font-size: 0.9em; }
"""


def page(title: str, body: str) -> str:
    return (f"<!doctype html><html lang=\"es\"><head><meta charset=\"utf-8\">"
            f"<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
            f"<title>{escape(title)}</title><style>{_STYLE}</style></head><body>{body}"
            f"<footer>Datos de prueba sintéticos. Este sistema es una implementación de "
            f"referencia.</footer></body></html>")


def field(label: str, name: str, value: str = "", kind: str = "text", hint: str = "",
          limit: int | None = None, required: bool = True) -> str:
    """One form control. The limit is shown to the participant, not only enforced on the server."""
    attrs = f' name="{escape(name)}" id="{escape(name)}"'
    if required:
        attrs += " required"
    if limit:
        attrs += f' maxlength="{limit}"'
    note = f" <small>{escape(hint)}</small>" if hint else ""
    if kind == "textarea":
        control = f"<textarea{attrs}>{escape(value)}</textarea>"
    else:
        control = f'<input type="{escape(kind)}" value="{escape(value)}"{attrs}>'
    return f'<label for="{escape(name)}">{escape(label)}{note}</label>{control}'


def notice(text: str, css: str = "aviso") -> str:
    return f'<p class="{escape(css)}">{escape(text)}</p>'


def esc(value) -> str:
    return escape(str(value))
