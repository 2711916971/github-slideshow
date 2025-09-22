from __future__ import annotations

import logging

from .base import BaseDriver, CaseSpec

logger = logging.getLogger(__name__)


class StarCCMDriver(BaseDriver):
    name = "starccm"

    def run_case(self, spec: CaseSpec) -> str:
        logger.info("Star-CCM+ driver mock execution for %s", spec.name)
        return "mock"
