from __future__ import annotations

import logging
import shutil
import subprocess
from pathlib import Path
from typing import Iterable

from app.schemas.common import CaseSpec, GeometryHandle

from .mock_solver import CFDSolverMock

logger = logging.getLogger(__name__)


ALLOWED_COMMANDS = {"blockMesh", "snappyHexMesh", "simpleFoam"}


class OpenFOAMRunner:
    def __init__(self, use_mock: bool = True) -> None:
        self.use_mock = use_mock

    def run(self, case_dir: Path, geometry: GeometryHandle, case: CaseSpec) -> Path:
        if self.use_mock or not self._check_commands():
            logger.warning("OpenFOAM commands missing - falling back to mock solver")
            solver = CFDSolverMock()
            solver.run(geometry, case, case_dir / "postProcessing")
            return case_dir
        commands = [
            ["blockMesh"],
            ["snappyHexMesh", "-overwrite"],
            ["simpleFoam"],
        ]
        for command in commands:
            self._run_command(command, cwd=case_dir)
        return case_dir

    def dry_run(self) -> list[str]:
        return [" ".join(cmd) for cmd in (["blockMesh"], ["snappyHexMesh", "-overwrite"], ["simpleFoam"])]

    def _check_commands(self) -> bool:
        for cmd in ALLOWED_COMMANDS:
            if shutil.which(cmd) is None:
                return False
        return True

    def _run_command(self, command: Iterable[str], cwd: Path) -> None:
        if command[0] not in ALLOWED_COMMANDS:
            raise ValueError(f"Command {command[0]} not allowed")
        attempts = 0
        while attempts < 3:
            result = subprocess.run(command, cwd=cwd, check=False, capture_output=True, text=True)
            if result.returncode == 0:
                logger.info(result.stdout)
                return
            attempts += 1
            logger.error("Command %s failed (attempt %s): %s", command, attempts, result.stderr)
        raise RuntimeError(f"Command {command} failed after retries")
