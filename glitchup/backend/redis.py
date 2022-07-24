from typing import Any

import aioredis


class Redis:
    """Class for Redis functionality."""

    url: str = "redis://redis:6379"

    @classmethod
    async def get_connection(cls) -> Any:
        """Get a Redis connection."""
        return await aioredis.from_url(cls.url)
