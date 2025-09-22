from __future__ import annotations

from storage.database import init_db
from storage.repository import storage_repo


def test_storage_roundtrip(tmp_path, monkeypatch):
    init_db()
    geometry = {
        "geometry_id": "abc123",
        "name": "geom",
        "hash": "hash",
        "artifact_path": "path",
        "bbox": [0, 0, 0, 1, 1, 1],
        "volume": 10.0,
        "waterplane_area": 5.0,
        "created_at": "2023-01-01T00:00:00",
    }
    storage_repo.create_geometry(geometry)
    fetched = storage_repo.get_geometry("abc123")
    assert fetched["name"] == "geom"
