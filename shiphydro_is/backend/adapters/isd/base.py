from __future__ import annotations

from dataclasses import dataclass
from typing import List

from app.schemas.common import DriverDryRun


@dataclass
class CaseSpec:
    name: str
    command: List[str]
    environment: dict[str, str]
    script: str | None = None


class BaseDriver:
    name: str = "base"

    def dry_run(self, spec: CaseSpec) -> DriverDryRun:
        return DriverDryRun(
            commands=[" ".join(spec.command)],
            scripts=[spec.script] if spec.script else [],
            env=[f"{k}={v}" for k, v in spec.environment.items()],
        )

    def run_case(self, spec: CaseSpec) -> str:
        raise NotImplementedError
