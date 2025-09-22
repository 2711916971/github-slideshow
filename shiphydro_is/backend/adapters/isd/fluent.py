from __future__ import annotations

import logging

from .base import BaseDriver, CaseSpec

logger = logging.getLogger(__name__)


class FluentDriver(BaseDriver):
    name = "fluent"

    def run_case(self, spec: CaseSpec) -> str:
        logger.info("Fluent driver mock execution for %s", spec.name)
        return "mock"
