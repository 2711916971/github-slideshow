from __future__ import annotations

import json
import math
from datetime import datetime
from pathlib import Path
from typing import List, Tuple

from .dsl import GeometryParameters


class GeometryGenerationError(Exception):
    """Raised when geometry generation fails."""


def _cross(a: Tuple[float, float, float], b: Tuple[float, float, float]) -> Tuple[float, float, float]:
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def _normalize(vec: Tuple[float, float, float]) -> Tuple[float, float, float]:
    length = math.sqrt(sum(component * component for component in vec)) or 1.0
    return tuple(component / length for component in vec)


class GeometryGenerator:
    def __init__(self, output_dir: str | Path) -> None:
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate(self, params: GeometryParameters) -> dict:
        vertices, faces = self._create_parametric_hull(params)
        stl_path = self.output_dir / f"{params.name}.stl"
        self._write_ascii_stl(stl_path, params.name, vertices, faces)
        bbox = self._compute_bbox(vertices)
        volume = self._estimate_volume(params)
        waterplane = params.lpp * params.beam * 0.7
        metadata = {
            "geometry_id": params.hash[:12],
            "name": params.name,
            "hash": params.hash,
            "artifact_path": str(stl_path),
            "bbox": bbox,
            "volume": volume,
            "waterplane_area": waterplane,
            "created_at": datetime.utcnow().isoformat(),
        }
        meta_path = self.output_dir / f"{params.name}_metadata.json"
        with meta_path.open("w", encoding="utf-8") as handle:
            json.dump(metadata, handle, indent=2)
        return metadata

    def _create_parametric_hull(self, params: GeometryParameters) -> Tuple[List[Tuple[float, float, float]], List[Tuple[int, int, int]]]:
        length = params.lpp
        half_beam = params.beam / 2
        sections = 20
        ring = 12
        vertices: List[Tuple[float, float, float]] = []
        faces: List[Tuple[int, int, int]] = []
        for i in range(sections):
            xi = length * i / (sections - 1)
            fullness = math.sin(math.pi * (xi / length)) ** 0.5 if length else 0.0
            radius = fullness * half_beam
            for j in range(ring):
                theta = 2 * math.pi * j / ring
                y = radius * math.cos(theta)
                z = radius * 0.4 * math.sin(theta)
                vertices.append((xi, y, z))
            if i > 0:
                base_idx = i * ring
                prev_idx = (i - 1) * ring
                for j in range(ring):
                    a = prev_idx + j
                    b = prev_idx + (j + 1) % ring
                    c = base_idx + j
                    d = base_idx + (j + 1) % ring
                    faces.append((a, b, c))
                    faces.append((b, d, c))
        return vertices, faces

    def _write_ascii_stl(self, path: Path, name: str, vertices: List[Tuple[float, float, float]], faces: List[Tuple[int, int, int]]) -> None:
        with path.open("w", encoding="utf-8") as stl:
            stl.write(f"solid {name}\n")
            for face in faces:
                v1, v2, v3 = (vertices[idx] for idx in face)
                normal = _cross((v2[0] - v1[0], v2[1] - v1[1], v2[2] - v1[2]), (v3[0] - v1[0], v3[1] - v1[1], v3[2] - v1[2]))
                normal = _normalize(normal)
                stl.write(f" facet normal {normal[0]} {normal[1]} {normal[2]}\n  outer loop\n")
                for vertex in (v1, v2, v3):
                    stl.write(f"    vertex {vertex[0]} {vertex[1]} {vertex[2]}\n")
                stl.write("  endloop\n endfacet\n")
            stl.write(f"endsolid {name}\n")

    def _compute_bbox(self, vertices: List[Tuple[float, float, float]]) -> List[float]:
        xs = [v[0] for v in vertices]
        ys = [v[1] for v in vertices]
        zs = [v[2] for v in vertices]
        return [min(xs), min(ys), min(zs), max(xs), max(ys), max(zs)]

    def _estimate_volume(self, params: GeometryParameters) -> float:
        return params.cb * params.lpp * params.beam * params.draft


def cli_generate(dsl_path: str, output: str) -> dict:
    from .dsl import load_geometry_from_yaml

    params = load_geometry_from_yaml(dsl_path)
    generator = GeometryGenerator(output)
    return generator.generate(params)
