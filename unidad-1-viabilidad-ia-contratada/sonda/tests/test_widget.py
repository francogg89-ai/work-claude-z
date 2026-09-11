"""Run the view's real script in Node with a minimal DOM and a simulated MCP Apps host."""

import json
import re
import shutil
import subprocess

import pytest

from probe.store import EXPECTED_P042_FINGERPRINT, generate_dataset, proposal_fingerprint
from probe.widget import WIDGET_HTML

pytestmark = pytest.mark.skipif(shutil.which("node") is None, reason="node not available")

HARNESS = r"""
const script = process.argv[1];
const data = JSON.parse(process.argv[2]);
const els = {};
const document = { getElementById: (id) => (els[id] ??= { textContent: "", hidden: false }) };
const sent = [];
let handler = null;
const parent = { postMessage: (m) => sent.push(m) };
const window = { parent, addEventListener: (type, fn) => { if (type === "message") handler = fn; } };
new Function("window", "document", script)(window, document);
const init = sent.find((m) => m.method === "ui/initialize");
handler({ source: parent, data: { jsonrpc: "2.0", id: init.id, result: {} } });
setTimeout(() => {
  handler({ source: parent, data: { jsonrpc: "2.0", method: "ui/notifications/tool-result",
                                    params: { structuredContent: data } } });
  console.log(JSON.stringify({
    methods: sent.map((m) => m.method),
    init: init.params,
    what: els["what"].textContent,
    shown: els["huella-mostrada"].textContent,
    match: els["coinciden"].textContent,
    visible: els["vista"].hidden === false,
  }));
}, 0);
"""


def run_view(structured: dict) -> dict:
    script = re.search(r"<script>(.*)</script>", WIDGET_HTML, re.S).group(1)
    out = subprocess.run(["node", "-e", HARNESS, script, json.dumps(structured, ensure_ascii=False)],
                         capture_output=True, text=True, encoding="utf-8", timeout=30, check=True)
    return json.loads(out.stdout)


def shown_p042(**override) -> dict:
    p = next(x for x in generate_dataset()["proposals"] if x["id"] == "P-042")
    return {**p, "fingerprint": proposal_fingerprint(p), **override}


def test_view_completes_the_handshake_and_renders_the_exact_original():
    result = run_view(shown_p042())
    assert result["methods"] == ["ui/initialize", "ui/notifications/initialized"]
    assert result["init"]["protocolVersion"] == "2026-01-26"
    assert result["what"] == "[SINTETICO] Propongo un especial sobre música independiente."
    assert result["shown"] == EXPECTED_P042_FINGERPRINT
    assert result["match"] == "SI"
    assert result["visible"] is True


def test_view_detects_an_alteration_between_server_and_display():
    altered = shown_p042(what="[SINTÉTICO] Propongo un especial sobre música independiente.")
    result = run_view(altered)
    assert result["shown"] == "b60c8421"
    assert result["match"] == "NO"


def test_view_renders_hostile_markup_as_plain_text():
    hostile = shown_p042(what='<img src=x onerror="alert(1)">')
    assert run_view(hostile)["what"] == '<img src=x onerror="alert(1)">'
