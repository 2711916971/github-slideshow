from __future__ import annotations

import logging
import queue as queue_module
import threading
import time
from dataclasses import dataclass
from typing import Callable, Optional

logger = logging.getLogger(__name__)


@dataclass
class Task:
    job_id: str
    func: Callable[[], None]
    retries: int = 0
    max_retries: int = 3
    timeout: float = 600.0


class LocalTaskQueue:
    def __init__(self) -> None:
        self._queue: queue_module.Queue[Task] = queue_module.Queue()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._running = False

    def start(self) -> None:
        if not self._running:
            self._running = True
            self._thread.start()

    def submit(self, task: Task) -> None:
        logger.info("Task %s submitted", task.job_id)
        self._queue.put(task)

    def _run(self) -> None:
        while self._running:
            try:
                task = self._queue.get(timeout=0.5)
            except queue_module.Empty:
                continue
            start = time.time()
            try:
                task.func()
            except Exception as exc:  # pragma: no cover - safety net
                logger.exception("Task %s failed: %s", task.job_id, exc)
                if task.retries < task.max_retries:
                    task.retries += 1
                    self._queue.put(task)
            finally:
                elapsed = time.time() - start
                logger.info("Task %s finished in %.2fs", task.job_id, elapsed)


task_queue = LocalTaskQueue()
