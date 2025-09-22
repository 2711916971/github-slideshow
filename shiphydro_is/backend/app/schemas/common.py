from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Sequence


def parse_datetime(value: str) -> datetime:
    if isinstance(value, datetime):
        return value
    return datetime.fromisoformat(value)


@dataclass
class BaseModel:
    def dict(self) -> Dict[str, object]:
        def convert(value):
            if isinstance(value, Enum):
                return value.value
            if isinstance(value, datetime):
                return value.isoformat()
            if hasattr(value, "dict") and callable(value.dict):
                return value.dict()
            if isinstance(value, list):
                return [convert(item) for item in value]
            if isinstance(value, tuple):
                return [convert(item) for item in value]
            if isinstance(value, dict):
                return {k: convert(v) for k, v in value.items()}
            return value

        return convert(asdict(self))


@dataclass
class GeometryParam(BaseModel):
    name: str
    lpp: float
    beam: float
    depth: float
    cb: float
    bulbous_bow_length: float = 0.0
    bulbous_bow_radius: float = 0.0
    draft: float = 0.0
    sections: List[List[float]] = field(default_factory=list)


@dataclass
class GeometryHandle(BaseModel):
    geometry_id: str
    name: str
    hash: str
    artifact_path: str
    bbox: List[float]
    volume: float
    waterplane_area: float
    created_at: datetime


class TurbulenceModel(str, Enum):
    K_OMEGA_SST = "k-omega-sst"
    K_EPSILON = "k-epsilon"


@dataclass
class FluidProperties(BaseModel):
    density: float
    viscosity: float


@dataclass
class CaseSpec(BaseModel):
    geometry_id: str
    speed: float
    draft: float
    froude_number: float
    reynolds_number: float
    fluid: FluidProperties
    turbulence_model: TurbulenceModel = TurbulenceModel.K_OMEGA_SST
    solver_options: Dict[str, object] = field(default_factory=dict)
    def __post_init__(self) -> None:
        if isinstance(self.turbulence_model, str):
            self.turbulence_model = TurbulenceModel(self.turbulence_model)
        if isinstance(self.fluid, dict):
            self.fluid = FluidProperties(**self.fluid)



@dataclass
class RunRequest(BaseModel):
    geometry: GeometryParam
    case: CaseSpec
    use_mock: bool = False

    def __post_init__(self) -> None:
        if isinstance(self.geometry, dict):
            self.geometry = GeometryParam(**self.geometry)
        if isinstance(self.case, dict):
            self.case = CaseSpec(**self.case)


class RunState(str, Enum):
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    CANCELED = "CANCELED"


@dataclass
class RunStatus(BaseModel):
    job_id: str
    state: RunState
    progress: float
    stage: Optional[str]
    created_at: datetime
    updated_at: datetime
    solver_used: str
    message: Optional[str] = None

    def __post_init__(self) -> None:
        if isinstance(self.state, str):
            self.state = RunState(self.state)
        if not isinstance(self.created_at, datetime):
            self.created_at = parse_datetime(self.created_at)
        if not isinstance(self.updated_at, datetime):
            self.updated_at = parse_datetime(self.updated_at)


@dataclass
class MetricPoint(BaseModel):
    timestamp: datetime
    residual: float

    def __post_init__(self) -> None:
        if not isinstance(self.timestamp, datetime):
            self.timestamp = parse_datetime(self.timestamp)


@dataclass
class RunMetrics(BaseModel):
    job_id: str
    resistance_total: float
    resistance_coefficient: float
    residuals: Sequence[MetricPoint]
    timestamps: Sequence[datetime]
    def __post_init__(self) -> None:
        converted = []
        for item in self.residuals:
            if isinstance(item, MetricPoint):
                converted.append(item)
            else:
                converted.append(MetricPoint(timestamp=parse_datetime(item['timestamp']), residual=item['residual']))
        self.residuals = tuple(converted)
        if not self.timestamps:
            self.timestamps = tuple(point.timestamp for point in self.residuals)



@dataclass
class SurrogateSpec(BaseModel):
    name: str
    algorithm: str
    target: str
    features: List[str]


@dataclass
class SurrogatePrediction(BaseModel):
    mean: float
    std: float
    ci95: List[float]


@dataclass
class OptConfig(BaseModel):
    budget: int
    objectives: List[str]
    constraints: List[str]


@dataclass
class CandidatePoint(BaseModel):
    variables: Dict[str, float]
    objectives: Dict[str, float]


@dataclass
class OptResult(BaseModel):
    pareto: List[CandidatePoint]
    candidates: List[CandidatePoint]


@dataclass
class DriverDryRun(BaseModel):
    commands: List[str]
    scripts: List[str] = field(default_factory=list)
    env: List[str] = field(default_factory=list)
