import random
# import subprocess
from multiprocessing import Process
from typing import Any

import aioredis
import rq
from attrs import define

redis_conn = aioredis.from_url("redis://localhost:6379")
redis_queue = rq.Queue(connection=redis_conn)


@define(init=False)
class Worker(rq.Worker):
    """A worker that runs in a separate process. Subclass of Worker provided by the Redis Queue module."""

    def __init__(
        self,
        queues: list[rq.Queue],
        name: str,
        process: Process,
        conn: aioredis.Redis = None,
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
