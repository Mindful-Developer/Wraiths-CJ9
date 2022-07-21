from cv2 import Mat

from ..filters.image_filter import ImageFilter


class Job:
    """A single filter job"""

    def __init__(self, image: Mat, filters: list[ImageFilter]):
        self._image = image
        self._filters = filters

    def execute(self) -> Mat:
        """Apply the filters to the image"""
        img = self._image.copy()

        for img_filter in self._filters:
            img_filter.apply(img)

        return img
