from typing import Any

from cv2 import Mat

from ..filters.image_filter import ImageFilter


class Job:
    """A single filter job"""

    def __init__(
        self, image: Mat, filters: list[ImageFilter], params: list[dict[str, Any]]
    ):
        self._image = image
        self._filters = filters
        self._params = params

    def execute(self) -> Mat:
        """Apply the filters to the image"""
        img = self._image.copy()

        for img_filter, param in zip(self._filters, self._params):
            img_filter.apply(img, param)

        return img
