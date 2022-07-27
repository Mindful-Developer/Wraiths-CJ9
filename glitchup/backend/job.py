from typing import Any

from attrs import define
from cv2 import Mat

from ..filters.image_filter import ImageFilter


@define
class Job:
    """A single filter job"""

    _image: Mat
    _filters: list[ImageFilter]
    _params: list[dict[str, Any]]

    @property
    def image(self) -> Mat:
        """Get the image"""
        return self._image

    @property
    def filters(self) -> list[ImageFilter]:
        """Get the filters to be applied to the image"""
        return self._filters

    @property
    def params(self) -> list[dict[str, Any]]:
        """Get the parameters"""
        return self._params

    def execute(self) -> Mat:
        """Apply the filters to the image"""
        img = self.image.copy()

        for img_filter, param in zip(self.filters, self.params):
            img_filter.apply(img, param)

        return img
