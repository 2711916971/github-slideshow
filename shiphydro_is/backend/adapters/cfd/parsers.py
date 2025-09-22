from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


class CFDResultParser:
    def parse_metrics(self, metrics_path: str | Path) -> Dict[str, Any]:
        path = Path(metrics_path)
        if not path.exists():
            raise FileNotFoundError(f"Metrics file {metrics_path} not found")
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        if "Rt" not in data or "Ct" not in data:
            raise ValueError("Metrics missing required keys")
        return data

    def parse_forces(self, forces_path: str | Path) -> Dict[str, float]:
        path = Path(forces_path)
        if not path.exists():
            raise FileNotFoundError(f"Forces file {forces_path} not found")
        columns: List[str] = []
        values: List[float] = []
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                if line.startswith("#"):
                    columns = line.strip("# \n").split()
                    continue
                if not line.strip():
                    continue
                parts = [float(x) for x in line.split()]
                values = parts
        return {col: val for col, val in zip(columns, values)}
