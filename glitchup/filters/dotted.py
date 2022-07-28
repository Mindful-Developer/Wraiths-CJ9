import json
from random import randint as rnt
from typing import Any

import cv2 as cv
import numpy as np
from numpy.typing import NDArray

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
    def to_json(cls) -> str:
        """Return a JSON representation of the filter."""
        param_dict: dict[str, Parameter | int] = {
            param.name: param for param in cls.metadata()[1]
        }
        param_dict["inputs"] = cls.metadata()[0]
        return json.dumps(param_dict)

    @classmethod
    def apply(cls, images: list[cv.Mat], params: dict[str, Any]) -> None:
        """Apply the filter to the image."""
        img = images[0]
        num_dots = params["number of dots"].default
        num_colors = params["number of colors"].default
        colors = cls.get_rgb_colors(img, num_colors)

        for _ in range(num_dots):
            num = (rnt(0, img.shape[1]), rnt(0, img.shape[0]))
            cv.rectangle(
                img,
                num,
                (num[0], num[1]),
                (colors[rnt(0, len(colors) - 1)]),
                cv.FILLED,
            )

    @classmethod
    def get_rgb_colors(cls, img: list[cv.Mat], num: int) -> list[tuple[int, int, int]]:
        """Get colors"""
        height, width, _ = np.shape(img)
        data = np.float32(np.reshape(img, (height * width, 3)))
        criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        flags = cv.KMEANS_RANDOM_CENTERS
        _, _, centers = cv.kmeans(data, num, None, criteria, 10, flags)
        return [cls.create_bar(row) for row in centers]

    @staticmethod
    def create_bar(color: NDArray[np.float32]) -> tuple[int, int, int]:
        """Create rgb color tuple"""
        return int(color[0]), int(color[1]), int(color[2])


if __name__ == "__main__":
    params = Dotted.metadata()[1]
    param_dict = {param.name: param for param in params}
    img = cv.imread(r"D:\test.jpg")
    cv.imshow("Original", img)
    Dotted.apply([img], param_dict)
    cv.imshow("Dotted", img)
    cv.waitKey(0)
    cv.destroyAllWindows()
