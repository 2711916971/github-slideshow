from __future__ import annotations

from pathlib import Path

from adapters.cfd.parsers import CFDResultParser


def test_parse_forces(tmp_path: Path) -> None:
    path = tmp_path / "forces.dat"
    path.write_text("# time fx fy fz\n0.5 10 0 0\n", encoding="utf-8")
    parser = CFDResultParser()
    values = parser.parse_forces(path)
    assert values["time"] == 0.5
