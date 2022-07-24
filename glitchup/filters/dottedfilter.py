"""Filter for a TV white noice affect with color"""
from random import randint as rnt
from typing import Any, List

import cv2 as cv
import numpy as np
from cv2 import Mat

from glitchup.filters.image_filter import ImageFilter
from glitchup.filters.parameter import Parameter


class DottedFilter(ImageFilter):
    """Add random dots on the image"""

    def num_inputs(self) -> int:
        """Return the number of inputs this filter requires."""
        return 1

    def get_params(self) -> list[Parameter]:
        """Return the list of parameters for this filter."""
        return [
            Parameter(
                Parameter.ParamType.INT,
                "number of dots",
                default=40000,
                param_range=(9000, 50000)
            ),
            Parameter(
                Parameter.ParamType.INT,
                "number of colors",
                default=3,
                param_range=(1, 10)
            )
        ]

    def apply(self, img: Mat, params: dict[str, Any]) -> None:
        """Apply the filter to the image."""
        # opacity = params["opacity"].default
        num_dots = params["number of dots"].default
        num_colors = params["number of colors"].default
        colors = self.get_rgb_colors(img, num_colors)
        for _ in range(num_dots):
            num = (rnt(0, img.shape[1]), rnt(0, img.shape[0]))
            cv.rectangle(img, num, (num[0], num[1]), (colors[rnt(0, len(colors)-1)]), cv.FILLED)

    def get_rgb_colors(self, theimg: Any, num: int) -> List[Any]:
        """Get colors"""
        img = theimg
        height, width, _ = np.shape(img)
        data = np.float32(np.reshape(img, (height * width, 3)))
        number_clusters = num
        criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        flags = cv.KMEANS_RANDOM_CENTERS
        _, _, centers = cv.kmeans(data, number_clusters, None, criteria, 10, flags)

        rgb_values = []

        for _, row in enumerate(centers):
            rgb = self.create_bar(row)
            rgb_values.append(rgb)

        colors = []
        for _, row in enumerate(rgb_values):
            colors.append(row)
        return colors

    def create_bar(self, color: Any) -> tuple[int, int, int]:
        "Create rgb color tuple"
        red, green, blue = int(color[0]), int(color[1]), int(color[2])
        return (red, green, blue)


if __name__ == "__main__":
    filter = DottedFilter()
    params = filter.get_params()
    param_dict = {param.name: param for param in params}
    img = cv.imread(r"cats.jpg")
    cv.imshow("Original", img)
    filter.apply(img, param_dict)
    cv.imshow("Dotted", img)
    cv.waitKey(0)
    cv.destroyAllWindows()
