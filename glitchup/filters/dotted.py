from random import randint as rnt
from typing import Any

import cv2 as cv
import numpy as np

from .image_filter import ImageFilter
from .parameter import Parameter, ParamType

__all__ = ("Dotted",)


class Dotted(ImageFilter):
    """Add random dots on the image"""

    filter_id = 981

    @staticmethod
    def metadata() -> tuple[int, list[Parameter]]:
        """Return a tuple containing the inputs and parameters of the filter."""
        return 1, [
            Parameter(
                ParamType.INT,
                "number of dots",
                default=40000,
                param_range=(9000, 50000),
            ),
            Parameter(
                ParamType.INT, "number of colors", default=3, param_range=(1, 10)
            ),
        ]

    @classmethod
    def apply(cls, img: list[cv.Mat], params: dict[str, Any]) -> None:
        """Apply the filter to the image."""
        for i in img:
            num_dots = params["number of dots"].default
            num_colors = params["number of colors"].default
            colors = cls.get_rgb_colors(img, num_colors)
            for _ in range(num_dots):
                num = (rnt(0, i.shape[1]), rnt(0, i.shape[0]))
                cv.rectangle(
                    i,
                    num,
                    (num[0], num[1]),
                    (colors[rnt(0, len(colors) - 1)]),
                    cv.FILLED,
                )

    @classmethod
    def get_rgb_colors(cls, img: list[cv.Mat], num: int) -> list[Any]:
        """Get colors"""
        height, width, _ = np.shape(img)
        data = np.float32(np.reshape(img, (height * width, 3)))
        number_clusters = num
        criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        flags = cv.KMEANS_RANDOM_CENTERS
        _, _, centers = cv.kmeans(data, number_clusters, None, criteria, 10, flags)

        rgb_values = []

        for _, row in enumerate(centers):
            rgb = cls.create_bar(row)
            rgb_values.append(rgb)

        colors = []
        for _, row in enumerate(rgb_values):
            colors.append(row)
        return colors

    @staticmethod
    def create_bar(color: Any) -> tuple[int, int, int]:
        """Create rgb color tuple"""
        red, green, blue = int(color[0]), int(color[1]), int(color[2])
        return red, green, blue


if __name__ == "__main__":
    filter = Dotted()
    params = filter.metadata()[1]
    param_dict = {param.name: param for param in params}
    img = cv.imread(r"cats.jpg")
    cv.imshow("Original", img)
    filter.apply(img, param_dict)
    cv.imshow("Dotted", img)
    cv.waitKey(0)
    cv.destroyAllWindows()
