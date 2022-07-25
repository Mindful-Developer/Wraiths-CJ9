from abc import ABC, abstractmethod
from typing import Any

from cv2 import Mat

from .parameter import Parameter

__all__ = ("ImageFilter",)


class ImageFilter(ABC):
    """Abstract class for image filters."""

    @abstractmethod
    def num_inputs(self) -> int:
        """Return the number of inputs this filter requires."""
        ...

    @abstractmethod
    def get_params(self) -> list[Parameter]:
        """Return the list of parameters for this filter."""
        ...

    @abstractmethod
    def apply(self, images: list[Mat], params: dict[str, Any]) -> None:
        """Apply the filter to the image."""
        ...
