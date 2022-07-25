from typing import Any

from attrs import define
from cv2 import Mat

from glitchup.filters.image_filter import ImageFilter


@define
class Job:
    """A single filter job"""

    _image: Mat
    _filters: list[ImageFilter]
    _params: list[dict[str, Any]]

    def execute(self) -> Mat:
        """Apply the filters to the image"""
        img = self._image.copy()

        for img_filter, param in zip(self._filters, self._params):
            img_filter.apply(img, param)

        return img
