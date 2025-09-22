from __future__ import annotations

import json
from datetime import datetime
from typing import Optional

from .database import session_scope


class StorageRepository:
    def create_geometry(self, geometry: dict) -> None:
        with session_scope() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO geometries (geometry_id, name, hash, metadata_json, created_at) VALUES (?, ?, ?, ?, ?)",
                (
                    geometry["geometry_id"],
                    geometry["name"],
                    geometry["hash"],
                    json.dumps(geometry),
                    geometry.get("created_at", datetime.utcnow().isoformat()),
                ),
            )

    def get_geometry(self, geometry_id: str) -> Optional[dict]:
        with session_scope() as conn:
            cur = conn.execute(
                "SELECT metadata_json FROM geometries WHERE geometry_id = ?", (geometry_id,)
            )
            row = cur.fetchone()
            if not row:
                return None
            return json.loads(row[0])

    def create_case(self, case: dict) -> None:
        with session_scope() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO cases (case_id, geometry_id, case_hash, spec_json, created_at) VALUES (?, ?, ?, ?, ?)",
                (
                    case["case_id"],
                    case["geometry_id"],
                    case["case_hash"],
                    json.dumps(case["spec"]),
                    datetime.utcnow().isoformat(),
                ),
            )

    def get_case(self, case_id: str) -> Optional[dict]:
        with session_scope() as conn:
            cur = conn.execute("SELECT geometry_id, case_hash, spec_json FROM cases WHERE case_id = ?", (case_id,))
            row = cur.fetchone()
            if not row:
                return None
            spec = json.loads(row[2])
            return {"case_id": case_id, "geometry_id": row[0], "case_hash": row[1], "spec": spec}

    def upsert_run(self, run: dict) -> None:
        with session_scope() as conn:
            conn.execute(
                """
                INSERT INTO runs (job_id, geometry_id, case_id, status, progress, stage, solver_used, message, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(job_id) DO UPDATE SET
                    status=excluded.status,
                    progress=excluded.progress,
                    stage=excluded.stage,
                    solver_used=excluded.solver_used,
                    message=excluded.message,
                    updated_at=excluded.updated_at
                """,
                (
                    run["job_id"],
                    run["geometry_id"],
                    run["case_id"],
                    run["status"],
                    run.get("progress", 0.0),
                    run.get("stage"),
                    run.get("solver_used", "unknown"),
                    run.get("message"),
                    datetime.utcnow().isoformat(),
                    datetime.utcnow().isoformat(),
                ),
            )

    def get_run(self, job_id: str) -> Optional[dict]:
        with session_scope() as conn:
            cur = conn.execute(
                "SELECT geometry_id, case_id, status, progress, stage, solver_used, message, created_at, updated_at FROM runs WHERE job_id = ?",
                (job_id,),
            )
            row = cur.fetchone()
            if not row:
                return None
            return {
                "job_id": job_id,
                "geometry_id": row[0],
                "case_id": row[1],
                "status": row[2],
                "progress": row[3],
                "stage": row[4],
                "solver_used": row[5],
                "message": row[6],
                "created_at": datetime.fromisoformat(row[7]),
                "updated_at": datetime.fromisoformat(row[8]),
            }

    def store_metrics(self, job_id: str, metrics: dict) -> None:
        with session_scope() as conn:
            conn.execute(
                "INSERT INTO metrics (job_id, metrics_json, created_at) VALUES (?, ?, ?)",
                (job_id, json.dumps(metrics), datetime.utcnow().isoformat()),
            )

    def get_latest_metrics(self, job_id: str) -> Optional[dict]:
        with session_scope() as conn:
            cur = conn.execute(
                "SELECT metrics_json FROM metrics WHERE job_id = ? ORDER BY created_at DESC LIMIT 1",
                (job_id,),
            )
            row = cur.fetchone()
            return json.loads(row[0]) if row else None

    def log_event(self, job_id: str, action: str, detail: str) -> None:
        with session_scope() as conn:
            conn.execute(
                "INSERT INTO audit_logs (job_id, action, detail, created_at) VALUES (?, ?, ?, ?)",
                (job_id, action, detail, datetime.utcnow().isoformat()),
            )


storage_repo = StorageRepository()
