from __future__ import annotations

import json
import logging
import uuid
from datetime import datetime
from pathlib import Path

from adapters.cfd.openfoam_runner import OpenFOAMRunner
from adapters.cfd.openfoam_writer import OpenFOAMCaseWriter
from adapters.cfd.parsers import CFDResultParser
from adapters.geometry.dsl import GeometryParameters, geometry_to_dict
from adapters.geometry.generators import GeometryGenerator
from storage.repository import storage_repo
from workers.task_queue import Task, task_queue

from app.schemas.common import CaseSpec, GeometryHandle, GeometryParam, RunRequest, RunState, RunStatus

logger = logging.getLogger(__name__)


ARTIFACT_ROOT = Path(__file__).resolve().parents[2] / "artifacts"
ARTIFACT_ROOT.mkdir(parents=True, exist_ok=True)


def schedule_run(request: RunRequest) -> RunStatus:
    geometry_params = GeometryParameters(
        name=request.geometry.name,
        lpp=request.geometry.lpp,
        beam=request.geometry.beam,
        depth=request.geometry.depth,
        draft=request.geometry.draft,
        cb=request.geometry.cb,
        bulbous_bow_length=request.geometry.bulbous_bow_length,
        bulbous_bow_radius=request.geometry.bulbous_bow_radius,
        sections=request.geometry.sections,
    )
    generator = GeometryGenerator(ARTIFACT_ROOT / "geometries")
    geometry_meta = generator.generate(geometry_params)
    storage_repo.create_geometry(geometry_meta)
    geometry_meta_clean = geometry_meta.copy()
    geometry_meta_clean["created_at"] = datetime.fromisoformat(geometry_meta_clean["created_at"])
    geometry_handle = GeometryHandle(**geometry_meta_clean)
    case_id = uuid.uuid4().hex[:12]
    case_hash = uuid.uuid5(uuid.UUID(int=0), json.dumps(request.case.dict(), sort_keys=True)).hex
    storage_repo.create_case(
        {
            "case_id": case_id,
            "geometry_id": geometry_handle.geometry_id,
            "case_hash": case_hash,
            "spec": request.case.dict(),
        }
    )
    job_id = uuid.uuid4().hex
    storage_repo.upsert_run(
        {
            "job_id": job_id,
            "geometry_id": geometry_handle.geometry_id,
            "case_id": case_id,
            "status": RunState.QUEUED.value,
            "progress": 0.0,
            "stage": "queued",
            "solver_used": "pending",
            "message": None,
        }
    )

    def task_func() -> None:
        run_id = job_id
        storage_repo.upsert_run(
            {
                "job_id": run_id,
                "geometry_id": geometry_handle.geometry_id,
                "case_id": case_id,
                "status": RunState.RUNNING.value,
                "progress": 0.1,
                "stage": "meshing",
                "solver_used": "pending",
                "message": None,
            }
        )
        case_writer = OpenFOAMCaseWriter(ARTIFACT_ROOT / "cases")
        case_dir = case_writer.write_case(geometry_handle, request.case)
        storage_repo.upsert_run(
            {
                "job_id": run_id,
                "geometry_id": geometry_handle.geometry_id,
                "case_id": case_id,
                "status": RunState.RUNNING.value,
                "progress": 0.5,
                "stage": "solving",
                "solver_used": "pending",
                "message": None,
            }
        )
        runner = OpenFOAMRunner(use_mock=request.use_mock or True)
        runner.run(case_dir, geometry_handle, request.case)
        parser = CFDResultParser()
        metrics_path = case_dir / "postProcessing" / "metrics.json"
        metrics = parser.parse_metrics(metrics_path)
        storage_repo.store_metrics(run_id, metrics)
        storage_repo.upsert_run(
            {
                "job_id": run_id,
                "geometry_id": geometry_handle.geometry_id,
                "case_id": case_id,
                "status": RunState.SUCCEEDED.value,
                "progress": 1.0,
                "stage": "completed",
                "solver_used": metrics.get("solver", "mock"),
                "message": None,
            }
        )

    task_queue.submit(Task(job_id=job_id, func=task_func))
    task_queue.start()
    now = datetime.utcnow()
    return RunStatus(
        job_id=job_id,
        state=RunState.QUEUED,
        progress=0.0,
        stage="queued",
        created_at=now,
        updated_at=now,
        solver_used="pending",
    )


def get_status(job_id: str) -> RunStatus:
    record = storage_repo.get_run(job_id)
    if not record:
        raise ValueError(f"Job {job_id} not found")
    return RunStatus(
        job_id=record["job_id"],
        state=RunState(record["status"]),
        progress=record["progress"],
        stage=record["stage"],
        created_at=record["created_at"],
        updated_at=record["updated_at"],
        solver_used=record["solver_used"],
        message=record.get("message"),
    )


def get_metrics(job_id: str) -> dict:
    metrics = storage_repo.get_latest_metrics(job_id)
    if not metrics:
        raise ValueError("Metrics not available")
    return metrics
