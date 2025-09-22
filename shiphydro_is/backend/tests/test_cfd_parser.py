from __future__ import annotations

import json
from pathlib import Path

from adapters.cfd.parsers import CFDResultParser


def test_parse_metrics(tmp_path: Path) -> None:
    data = {"Rt": 120.0, "Ct": 0.002, "residuals": []}
    path = tmp_path / "metrics.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    parser = CFDResultParser()
    parsed = parser.parse_metrics(path)
    assert parsed["Rt"] == 120.0
