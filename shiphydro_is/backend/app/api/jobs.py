from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.schemas.common import DriverDryRun, RunMetrics, RunRequest, RunStatus
from app.services import jobs as job_service
from adapters.isd.base import CaseSpec as DriverCaseSpec
from adapters.isd.fluent import FluentDriver
from adapters.isd.openfoam import OpenFOAMDriver
from adapters.isd.starccm import StarCCMDriver

router = APIRouter(prefix="/api/v1", tags=["jobs"])


driver_registry = {
    "openfoam": OpenFOAMDriver(),
    "fluent": FluentDriver(),
    "starccm": StarCCMDriver(),
}


@router.post("/jobs", response_model=RunStatus)
async def submit_job(request: RunRequest) -> RunStatus:
    try:
        return job_service.schedule_run(request).dict()
    except Exception as exc:  # pragma: no cover - FastAPI error path
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/results/{job_id}", response_model=RunMetrics)
async def get_result(job_id: str) -> RunMetrics:
    try:
        metrics = job_service.get_metrics(job_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    status = job_service.get_status(job_id)
    run_metrics = RunMetrics(
        job_id=job_id,
        resistance_total=metrics["Rt"],
        resistance_coefficient=metrics["Ct"],
        residuals=[
            {"timestamp": point["timestamp"], "residual": point["residual"]}
            for point in metrics.get("residuals", [])
        ],
        timestamps=[point["timestamp"] for point in metrics.get("residuals", [])],
    )
    return run_metrics.dict()


@router.get("/jobs/{job_id}", response_model=RunStatus)
async def get_status(job_id: str) -> RunStatus:
    try:
        return job_service.get_status(job_id).dict()
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/drivers/dryrun", response_model=DriverDryRun)
async def driver_dry_run(driver: str, command: list[str]) -> DriverDryRun:
    drv = driver_registry.get(driver)
    if not drv:
        raise HTTPException(status_code=404, detail="Driver not found")
    spec = DriverCaseSpec(name="dryrun", command=command, environment={})
    return drv.dry_run(spec).dict()
