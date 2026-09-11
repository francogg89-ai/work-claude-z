"""Print the probe's server-side evidence (tool calls and saved evaluations) as JSON."""

import json
import os
from pathlib import Path

from probe.store import Store


def export_evidence(store: Store) -> dict:
    return {"calls": store.all_calls(), "evaluations": store.all_evaluations()}


if __name__ == "__main__":
    s = Store(Path(os.environ.get("SONDA_DB", ".data/probe.sqlite")))
    print(json.dumps(export_evidence(s), ensure_ascii=False, indent=2))
    s.close()
