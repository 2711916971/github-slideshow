from __future__ import annotations

from pathlib import Path

from adapters.geometry.dsl import GeometryParameters
from adapters.geometry.generators import GeometryGenerator


def test_geometry_generator_outputs(tmp_path: Path) -> None:
    params = GeometryParameters(
        name="test",
        lpp=10.0,
        beam=2.0,
        depth=2.0,
        draft=1.0,
        cb=0.6,
    )
    generator = GeometryGenerator(tmp_path)
    meta = generator.generate(params)
    assert Path(meta["artifact_path"]).exists()
    assert meta["volume"] > 0
