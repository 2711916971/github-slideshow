from __future__ import annotations

import json
from pathlib import Path

from app.schemas.common import CaseSpec, GeometryHandle


TEMPLATE_CONTROL = """application     simpleFoam;\nstartFrom       startTime;\nstopAt          endTime;\nendTime         1000;\nwriteInterval   100;\n"""


class OpenFOAMCaseWriter:
    def __init__(self, base_dir: str | Path) -> None:
        self.base_dir = Path(base_dir)

    def write_case(self, geometry: GeometryHandle, case: CaseSpec) -> Path:
        case_dir = self.base_dir / f"case_{geometry.geometry_id}"
        (case_dir / "system").mkdir(parents=True, exist_ok=True)
        (case_dir / "constant").mkdir(exist_ok=True)
        (case_dir / "0").mkdir(exist_ok=True)
        control_path = case_dir / "system" / "controlDict"
        control_path.write_text(TEMPLATE_CONTROL, encoding="utf-8")
        created_at = geometry.created_at.isoformat() if hasattr(geometry.created_at, "isoformat") else str(geometry.created_at)
        case_info = {
            "geometry": geometry.dict() | {"created_at": created_at},
            "case": case.dict(),
        }
        (case_dir / "case_info.json").write_text(json.dumps(case_info, indent=2, default=str), encoding="utf-8")
        return case_dir
