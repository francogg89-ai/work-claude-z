"""The MCP Apps view that shows one proposal exactly as it was received.

U1 demonstrated that the free text of the model is not literal: it retypes and normalises what
it shows. This view is the channel that does not pass through the model — server, host, iframe
— and it computes the fingerprint of what it actually rendered so the creator compares two
short codes instead of reading accents.

The text of a participant is untrusted: it is only ever assigned with textContent.
"""

VIEW_URI = "ui://circuito/propuesta.html"

_FNV_JS = """function fnv1a32(text) {
  let h = 0x811c9dc5;
  for (const byte of new TextEncoder().encode(text)) {
    h = Math.imul(h ^ byte, 0x01000193) >>> 0;
  }
  return h.toString(16).padStart(8, "0");
}"""

VIEW_HTML = """<!doctype html>
<html lang="es">
<head><meta charset="utf-8"><title>Propuesta tal como se recibió</title>
<style>
  body { font-family: system-ui, sans-serif; margin: 0; padding: 12px; }
  .campo { margin: 0 0 8px; white-space: pre-wrap; }
  .etiqueta { font-weight: 600; }
  .huellas { font-family: ui-monospace, monospace; margin-top: 12px; }
  .aviso { margin-top: 12px; font-size: 0.9em; }
</style></head>
<body>
  <div id="estado">Esperando la propuesta...</div>
  <div id="vista" hidden>
    <p class="campo"><span class="etiqueta">Id:</span> <span id="id"></span></p>
    <p class="campo"><span class="etiqueta">Qué propone:</span> <span id="what"></span></p>
    <p class="campo"><span class="etiqueta">Por qué aporta:</span> <span id="why"></span></p>
    <p class="campo"><span class="etiqueta">Ejemplo o detalle:</span> <span id="example"></span></p>
    <p class="campo"><span class="etiqueta">Autoría:</span> <span id="author"></span></p>
    <p class="campo"><span id="received"></span></p>
    <div class="huellas">
      <div>Huella de lo mostrado: <span id="huella-mostrada"></span></div>
      <div>Huella del servidor: <span id="huella-servidor"></span></div>
      <div>Coinciden: <span id="coinciden"></span></div>
    </div>
    <p class="aviso" id="aviso"></p>
  </div>
<script>
""" + _FNV_JS + """

const pending = new Map();
let nextId = 1;

function request(method, params) {
  const id = nextId++;
  window.parent.postMessage({ jsonrpc: "2.0", id, method, params }, "*");
  return new Promise((resolve, reject) => pending.set(id, { resolve, reject }));
}

function render(data) {
  if (!data || typeof data.what !== "string") return;
  for (const key of ["id", "what", "why", "example", "author"]) {
    document.getElementById(key).textContent = String(data[key] ?? "");
  }
  document.getElementById("received").textContent = String(data.received_label ?? "");
  document.getElementById("aviso").textContent = String(data.notice ?? "");
  const shown = ["what", "why", "example"].map((k) => document.getElementById(k).textContent).join("\\n");
  const mostrada = fnv1a32(shown);
  document.getElementById("huella-mostrada").textContent = mostrada;
  document.getElementById("huella-servidor").textContent = String(data.fingerprint ?? "");
  document.getElementById("coinciden").textContent = mostrada === data.fingerprint ? "SI" : "NO";
  document.getElementById("estado").hidden = true;
  document.getElementById("vista").hidden = false;
}

window.addEventListener("message", (event) => {
  if (event.source !== window.parent) return;
  const message = event.data;
  if (!message || message.jsonrpc !== "2.0") return;
  if (message.id !== undefined && pending.has(message.id)) {
    const p = pending.get(message.id);
    pending.delete(message.id);
    message.error ? p.reject(message.error) : p.resolve(message.result);
    return;
  }
  if (message.method === "ui/notifications/tool-result") {
    render(message.params && message.params.structuredContent);
  }
}, { passive: true });

request("ui/initialize", {
  protocolVersion: "2026-01-26",
  appInfo: { name: "circuito-vista-propuesta", version: "1" },
  appCapabilities: { availableDisplayModes: ["inline"] },
}).then(() => {
  window.parent.postMessage({ jsonrpc: "2.0", method: "ui/notifications/initialized", params: {} }, "*");
}).catch(() => {});

if (window.openai && window.openai.toolOutput) render(window.openai.toolOutput);
</script>
</body>
</html>
"""
