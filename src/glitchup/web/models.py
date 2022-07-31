import uuid
from typing import Any

from pydantic import BaseModel


class UploadedImage(BaseModel):
    """Model for uploaded image."""

    id: int = uuid.uuid4().int
    path: str

    @classmethod
    def to_dict(cls) -> dict[str, Any]:
        """Return a dictionary representation of the model."""
        return {
            "id": cls.id,
            "path": cls.path,
        }
