from typing import Any

from pydantic import BaseModel


class FilterMetadata(BaseModel):
    """Metadata for a filter."""

    filter_id: int
    name: str
    description: str
    inputs: int
    # the dict stored here is the result of calling `.to_dict()` on the parameter
    parameters: list[dict[str, Any]]
