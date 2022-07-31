import multiprocessing as mp
from typing import Any

import redis
import rq
from cv2 import Mat
from rq.decorators import job

from .filters.image_filter import ImageFilter
from .job import Job

redis_conn = redis.Redis(decode_responses=True)
redis_queue = rq.Queue(connection=redis_conn)


class Worker(rq.Worker):
    """A worker that lives in its own process."""

    def __init__(self) -> None:
        self.process = mp.Process(
            target=super().__init__,
            args=([redis_queue],),
            kwargs={"connection": redis_conn},
        )
        self.process.start()

    def close(self) -> None:
        """Close the worker process."""
        self.process.terminate()
        self.process.join()

    @job(queue=redis_queue, connection=redis_conn)  # type: ignore
    def apply_filter(
        img: Mat, filters: list[ImageFilter], params: list[dict[str, Any]]
    ) -> None:
        """Start a filter job and apply filter to image."""
        filter_job = Job(img, filters, params)
        filter_job = redis_queue.enqueue(filter_job.execute)
