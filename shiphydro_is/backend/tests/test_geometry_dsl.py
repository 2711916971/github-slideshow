from __future__ import annotations

from pathlib import Path

from adapters.geometry.dsl import load_geometry_from_yaml


def test_load_geometry(tmp_path: Path) -> None:
    yaml_path = tmp_path / "geom.yaml"
    yaml_path.write_text(
        """
name: hull
lpp: 100
beam: 15
depth: 10
draft: 6
cb: 0.6
""",
        encoding="utf-8",
    )
    params = load_geometry_from_yaml(yaml_path)
    assert params.name == "hull"
    assert params.hash
