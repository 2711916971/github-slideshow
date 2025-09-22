from __future__ import annotations

import time

from workers.task_queue import Task, task_queue


def test_task_queue_executes():
    results: list[int] = []

    def work() -> None:
        results.append(1)

    task_queue.submit(Task(job_id="1", func=work))
    task_queue.start()
    timeout = time.time() + 2
    while time.time() < timeout:
        if results:
            break
        time.sleep(0.1)
    assert results == [1]
