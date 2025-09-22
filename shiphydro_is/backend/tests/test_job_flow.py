from __future__ import annotations

import time

from app.schemas.common import CaseSpec, FluidProperties, GeometryParam, RunRequest
from app.services import jobs as job_service
from storage.database import init_db


def test_job_flow(tmp_path, monkeypatch):
    init_db()
    geometry = GeometryParam(
        name="demo",
        lpp=50.0,
        beam=8.0,
        depth=6.0,
        cb=0.55,
        bulbous_bow_length=0.05,
        bulbous_bow_radius=0.1,
        draft=4.0,
    )
    case = CaseSpec(
        geometry_id="temp",
        speed=6.0,
        draft=4.0,
        froude_number=0.2,
        reynolds_number=1e7,
        fluid=FluidProperties(density=1025.0, viscosity=0.0012),
        turbulence_model="k-omega-sst",
    )
    request = RunRequest(geometry=geometry, case=case, use_mock=True)
    status = job_service.schedule_run(request)
    assert status.state.value == "QUEUED"
    timeout = time.time() + 10
    while time.time() < timeout:
        current = job_service.get_status(status.job_id)
        if current.state.value == "SUCCEEDED":
            break
        time.sleep(0.2)
    assert job_service.get_status(status.job_id).state.value == "SUCCEEDED"
    metrics = job_service.get_metrics(status.job_id)
    assert "Rt" in metrics
