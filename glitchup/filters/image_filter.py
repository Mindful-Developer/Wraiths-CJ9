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

    @abstractmethod
    @staticmethod
    def metadata() -> tuple[int, list[Parameter]]:
        """Return a tuple containing the inputs and parameters of the filter."""
        ...

    @abstractmethod
    @classmethod
    def apply(cls, images: list[Mat], params: dict[str, Any]) -> None:
        """Apply the filter to the image."""
        ...
