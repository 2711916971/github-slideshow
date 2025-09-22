from __future__ import annotations

from adapters.geometry.dsl import GeometryParameters


def test_geometry_hash_changes():
    base = GeometryParameters(name="a", lpp=10, beam=2, depth=2, draft=1, cb=0.6)
    modified = GeometryParameters(name="a", lpp=11, beam=2, depth=2, draft=1, cb=0.6)
    assert base.hash != modified.hash
