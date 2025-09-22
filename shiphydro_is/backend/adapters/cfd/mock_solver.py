from __future__ import annotations

import json
import math
import random
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict

from app.schemas.common import CaseSpec, GeometryHandle


@dataclass
class MockSolverResult:
    resistance_total: float
    resistance_coefficient: float
    residuals: list[dict]
    solver_used: str = "mock"


class CFDSolverMock:
    def __init__(self, seed: int | None = None) -> None:
        self.random = random.Random(seed)

    def run(self, geometry: GeometryHandle, case: CaseSpec, output_dir: str | Path) -> MockSolverResult:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        baseline = geometry.volume / (case.speed + 1)
        froude = case.froude_number
        reynolds = case.reynolds_number
        resistance_total = baseline * (0.5 + froude) * 1.2
        resistance_coefficient = 2.0 * resistance_total / (case.fluid.density * case.speed**2 + 1e-6)
        residuals: list[dict] = []
        now = datetime.utcnow()
        for i in range(20):
            residual = math.exp(-0.3 * i) + self.random.random() * 1e-3
            residuals.append({"timestamp": (now + timedelta(seconds=i)).isoformat(), "residual": residual})
        metrics = {
            "Rt": resistance_total,
            "Ct": resistance_coefficient,
            "solver": "mock",
            "residuals": residuals,
        }
        metrics_path = Path(output_dir) / "metrics.json"
        with metrics_path.open("w", encoding="utf-8") as handle:
            json.dump(metrics, handle, indent=2)
        return MockSolverResult(
            resistance_total=resistance_total,
            resistance_coefficient=resistance_coefficient,
            residuals=residuals,
        )
