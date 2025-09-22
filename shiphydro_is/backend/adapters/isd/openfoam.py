from __future__ import annotations

import logging
import shutil
import subprocess
from pathlib import Path

from .base import BaseDriver, CaseSpec

logger = logging.getLogger(__name__)


class OpenFOAMDriver(BaseDriver):
    name = "openfoam"

    def run_case(self, spec: CaseSpec) -> str:
        command = spec.command
        if shutil.which(command[0]) is None:
            logger.warning("OpenFOAM binary %s missing, returning mock result", command[0])
            return "mock"
        result = subprocess.run(command, env=spec.environment, capture_output=True, text=True, check=False)
        if result.returncode != 0:
            logger.error("OpenFOAM run failed: %s", result.stderr)
            raise RuntimeError("OpenFOAM execution failed")
        logger.info(result.stdout)
        return "success"
