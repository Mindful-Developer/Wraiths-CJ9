from abc import ABC, abstractmethod
from typing import Any

from cv2 import Mat
from json import dumps

from .parameter import Parameter

__all__ = ("ImageFilter",)


class ImageFilter(ABC):
    """Abstract class for image filters."""

    @staticmethod
    @abstractmethod
    def num_inputs() -> int:
        """Return the number of inputs this filter requires."""
        ...

    @staticmethod
    @abstractmethod
    def get_params() -> list[Parameter]:
        """Return the list of parameters for this filter."""
        ...

    @classmethod
    def to_json(cls) -> str:
        """Return the data for this filter."""
        param_dict = {param.name: param for param in cls.get_params()}
        param_dict["inputs"] = cls.num_inputs()
        return dumps(param_dict)

    @classmethod
    @abstractmethod
    def apply(self, images: list[Mat], params: dict[str, Any]) -> None:
        """Apply the filter to the image."""
        ...
