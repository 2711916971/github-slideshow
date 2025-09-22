from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np


@dataclass
class ValidationIssue:
    message: str
    severity: str = "warning"


class GeometryValidator:
    def validate_vertices(self, vertices: Iterable[tuple[float, float, float]]) -> list[ValidationIssue]:
        arr = np.array(list(vertices))
        if arr.size == 0:
            return [ValidationIssue("Geometry has no vertices", "error")]
        extent = arr.max(axis=0) - arr.min(axis=0)
        issues: list[ValidationIssue] = []
        if np.any(extent <= 0):
            issues.append(ValidationIssue("Degenerate bounding box", "error"))
        if extent[0] < extent[1]:
            issues.append(ValidationIssue("Length smaller than beam", "warning"))
        return issues
