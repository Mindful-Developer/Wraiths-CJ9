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
        pass

    @abstractmethod
    def get_params(self) -> list[Parameter]:
        """Return the list of parameters for this filter."""
        pass

    @abstractmethod
    def apply(self, image: Mat, params: dict[str, Any]):
        """Apply the filter to the image."""
        pass
