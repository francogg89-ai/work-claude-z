import json
import shutil
import subprocess

import pytest

from probe.store import EXPECTED_P042_FINGERPRINT, fingerprint, generate_dataset, proposal_fingerprint
from probe.widget import FNV_JS


def p042():
    return next(p for p in generate_dataset()["proposals"] if p["id"] == "P-042")


def test_fnv1a_32_known_vectors():
    assert fingerprint("") == "811c9dc5"
    assert fingerprint("a") == "e40c292c"


def test_expected_p042_fingerprint_matches_the_candidate_data():
    assert proposal_fingerprint(p042()) == EXPECTED_P042_FINGERPRINT == "bac7f90c"


def test_the_alteration_observed_in_the_real_run_changes_the_fingerprint():
    altered = {**p042(), "what": p042()["what"].replace("SINTETICO", "SINTÉTICO")}
    assert proposal_fingerprint(altered) == "b60c8421"
    assert proposal_fingerprint(altered) != EXPECTED_P042_FINGERPRINT


@pytest.mark.skipif(shutil.which("node") is None, reason="node not available")
def test_widget_javascript_computes_the_same_fingerprint_as_python():
    samples = [p042()["what"], "SINTÉTICO", "música\nñandú\n", "", "emoji 🎤 y comillas \"x\""]
    script = FNV_JS + "\nconst s = JSON.parse(process.argv[1]);\nconsole.log(JSON.stringify(s.map(fnv1a32)));"
    out = subprocess.run(["node", "-e", script, json.dumps(samples)], capture_output=True, text=True,
                         timeout=30, check=True)
    assert json.loads(out.stdout) == [fingerprint(s) for s in samples]
