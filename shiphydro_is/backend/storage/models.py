from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Geometry:
    geometry_id: str
    name: str
    hash: str
    metadata_json: str
    created_at: datetime


@dataclass
class Case:
    case_id: str
    geometry_id: str
    case_hash: str
    spec: dict
    created_at: datetime


@dataclass
class Run:
    job_id: str
    geometry_id: str
    case_id: str
    status: str
    progress: float
    stage: Optional[str]
    solver_used: str
    message: Optional[str]
    created_at: datetime
    updated_at: datetime


@dataclass
class Metric:
    job_id: str
    metrics: dict
    created_at: datetime


@dataclass
class AuditLog:
    job_id: str
    action: str
    detail: str
    created_at: datetime
