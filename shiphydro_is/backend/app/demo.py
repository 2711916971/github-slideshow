from __future__ import annotations

import json
import time
from pathlib import Path

from adapters.geometry.dsl import load_geometry_from_yaml, _simple_yaml_load
from adapters.geometry.generators import GeometryGenerator
from app.schemas.common import CaseSpec, FluidProperties, GeometryParam, RunRequest
from app.services import jobs as job_service
from app.services.jobs import ARTIFACT_ROOT

EXAMPLE_DIR = Path(__file__).resolve().parents[2] / "examples"


def run_demo() -> dict:
    dsl_path = EXAMPLE_DIR / "geometries" / "bulbous_bow.yaml"
    geometry_params = load_geometry_from_yaml(dsl_path)
    generator = GeometryGenerator(ARTIFACT_ROOT / "demo_geoms")
    geometry_meta = generator.generate(geometry_params)
    case_yaml = EXAMPLE_DIR / "cases" / "steady_rans.yaml"
    case_spec = _simple_yaml_load(case_yaml.read_text(encoding="utf-8"))
    request = RunRequest(
        geometry=GeometryParam(
            name=geometry_params.name,
            lpp=geometry_params.lpp,
            beam=geometry_params.beam,
            depth=geometry_params.depth,
            draft=geometry_params.draft,
            cb=geometry_params.cb,
            bulbous_bow_length=geometry_params.bulbous_bow_length,
            bulbous_bow_radius=geometry_params.bulbous_bow_radius,
            sections=geometry_params.sections or [],
        ),
        case=CaseSpec(
            geometry_id=geometry_meta["geometry_id"],
            speed=case_spec["speed"],
            draft=case_spec["draft"],
            froude_number=case_spec["froude_number"],
            reynolds_number=case_spec["reynolds_number"],
            fluid=FluidProperties(**case_spec["fluid"]),
            turbulence_model=case_spec["turbulence_model"],
            solver_options=case_spec.get("solver_options", {}),
        ),
        use_mock=True,
    )
    status = job_service.schedule_run(request)
    timeout = time.time() + 15
    while time.time() < timeout:
        current = job_service.get_status(status.job_id)
        if current.state.value == "SUCCEEDED":
            metrics = job_service.get_metrics(status.job_id)
            return {"job_id": status.job_id, "metrics": metrics}
        time.sleep(0.5)
    raise TimeoutError("Demo run did not finish in time")


if __name__ == "__main__":
    result = run_demo()
    print(json.dumps(result, indent=2))
