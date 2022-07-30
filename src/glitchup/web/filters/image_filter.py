import json
from abc import ABC, abstractmethod
from typing import Any

from cv2 import Mat

from .parameter import Parameter

__all__ = ("ImageFilter",)


class ImageFilter(ABC):
    """Abstract class for image filters."""

    @classmethod
    def __init_subclass__(cls) -> None:
        required_class_attrs = ("filter_id",)

        for attr in required_class_attrs:
            if not hasattr(cls, attr):
                raise AttributeError(f"{cls.__name__} must define {attr}")

    @staticmethod
    @abstractmethod
    def metadata() -> tuple[int, list[Parameter]]:
        """Return a tuple containing the inputs and parameters of the filter."""
        ...

    @classmethod
    @abstractmethod
    def apply(cls, images: list[Mat], params: dict[str, Any]) -> None:
        """Apply the filter to the image."""
        ...

    @classmethod
    def to_json(cls) -> str:
        """Return a JSON representation of the filter."""
        param_dict = {param.name: param for param in cls.metadata()[1]}
        return json.dumps({"inputs": cls.metadata()[0], "parameters": param_dict})

    @classmethod
    def to_dict(cls) -> dict[str, Any]:
        """Return a dictionary representation of the filter."""
        return {
            "filter_id": cls.filter_id,  # type: ignore
            "name": cls.__name__,
            "description": cls.__doc__,
            "inputs": cls.metadata()[0],
            "parameters": [p.to_dict() for p in cls.metadata()[1]],
        }
