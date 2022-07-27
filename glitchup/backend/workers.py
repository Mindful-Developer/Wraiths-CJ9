import random
# import subprocess
from multiprocessing import Process
from typing import Any

import rq
from aioredis import Redis
from attrs import define

from .api import redis_conn, redis_queue


@define(init=False)
class Worker(rq.Worker):
    """A worker that runs in a separate process. Subclass of Worker provided by the Redis Queue module."""

    def __init__(
        self,
        queues: list[rq.Queue],
        name: str,
        process: Process,
        conn: Redis = None,
        **kwargs: Any,
    ) -> None:
        self.process = process
        super().__init__(queues, name=name, connection=conn, **kwargs)

    def __del__(self) -> None:
        self.process.close()


async def spawn_worker() -> Worker:
    """Spawn a new worker, inside a new process."""
    worker_id = random.getrandbits(10)
    worker_process = Process(name=f"worker-{worker_id}-process")
    worker = Worker(
        [redis_queue],
        name=f"worker-{worker_id}",
        process=worker_process,
        conn=redis_conn,
    )

    worker_process.start()

    return worker
