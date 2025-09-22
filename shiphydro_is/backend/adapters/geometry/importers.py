from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np


class GeometryImporter:
    """Mock geometry importer supporting STL/STEP/IGES fallback."""

    def import_file(self, path: str | Path) -> dict[str, Any]:
        file_path = Path(path)
        if not file_path.exists():
            raise FileNotFoundError(f"Geometry file {path} not found")
        # For demo we simply compute bounding box assuming ascii STL
        with file_path.open("r", encoding="utf-8", errors="ignore") as handle:
            vertices = []
            for line in handle:
                if line.strip().startswith("vertex"):
                    parts = line.strip().split()
                    vertices.append(tuple(float(v) for v in parts[1:4]))
        if not vertices:
            raise ValueError("Unsupported geometry format or missing vertices")
        arr = np.array(vertices)
        mins = arr.min(axis=0)
        maxs = arr.max(axis=0)
        bbox = [float(v) for v in (*mins, *maxs)]
        return {
            "name": file_path.stem,
            "path": str(file_path),
            "bbox": bbox,
            "vertex_count": len(vertices),
        }
