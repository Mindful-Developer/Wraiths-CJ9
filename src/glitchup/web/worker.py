import multiprocessing

import aioredis

redis_conn = aioredis.from_url("redis://localhost:6379")


def _initialize_worker_process(db_connection: aioredis.Redis) -> None:
    ...


with multiprocessing.Pool(
    initializer=_initialize_worker_process, initargs=(redis_conn,)
) as pool:
    ...
