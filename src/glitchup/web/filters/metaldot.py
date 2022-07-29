"""Filter image to a zero and one image with blurred background"""
from random import randint as rnt
from typing import Any, List

import cv2 as cv
import numpy as np

from .image_filter import ImageFilter
from .parameter import Parameter, ParamType


class MetalDot(ImageFilter):
    """Add metal like dots on the image"""

    filter_id = 984

    @staticmethod
    def metadata() -> tuple[int, list[Parameter]]:
        """Return a tuple containing the inputs and parameters of the filter."""
        return 1, [
            Parameter(ParamType.INT, "range number", default=0, param_range=(0, 30)),
            Parameter(ParamType.INT, "color", default=1, param_range=(0, 8)),
        ]

    @classmethod
    def apply(cls, images: list[cv.Mat], params: dict[str, Any]) -> None:
        """Apply the filter to the image."""
        img = images[0].copy()
        range_number = params["range number"].default
        for x in range(0, img.shape[0], 6):
            for y in range(0, img.shape[1], 4):
                n = rnt(0, range_number)
                c = tuple(cls.get_color(params, xc=int(x), yc=int(y)))
                cv.putText(
                    img,
                    text=str(n),
                    org=(y, x),
                    fontFace=5,
                    fontScale=0.3,
                    color=c,
                    thickness=0,
                )
        im2 = cv.Laplacian(img, cv.CV_32F)
        im2 = np.uint8(np.absolute(im2))
        cv.addWeighted(img, 0, im2, 1, 0, images[0])

    @staticmethod
    def get_color(params: dict[str, Any], xc: int, yc: int) -> List[int]:
        """Get color from parameter"""
        pattern = (
            "x x x",
            "x x y",
            "x y x",
            "y x x",
            "y y x",
            "x y y",
            "y x y",
            "y y y",
        )
        choosed = params["color"].default
        choosed = pattern[int(choosed)].split(" ")
        # print(choosed)
        c = []
        for t in choosed:
            if t == "x":
                c.append(xc)
            elif t == "y":
                c.append(yc)
        return c


if __name__ == "__main__":
    params = MetalDot.metadata()[1]
    param_dict = {param.name: param for param in params}
    img = cv.imread(r"park.jpg")
    cv.imshow("Original", img)
    MetalDot.apply([img], param_dict)
    cv.imshow("Metaldotted", img)
    cv.waitKey(0)
    cv.destroyAllWindows()
