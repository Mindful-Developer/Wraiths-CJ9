"""Filter image to a zero and one image with blurred background"""
from random import randint as rnt
from typing import Any

import cv2 as cv
import numpy as np

from glitchup.filters.image_filter import ImageFilter
from glitchup.filters.parameter import Parameter


class NumberFilter(ImageFilter):
    """Add random dots on the image"""

    def num_inputs(self) -> int:
        """Return the number of inputs this filter requires."""
        return 1

    def get_params(self) -> list[Parameter]:
        """Return the list of parameters for this filter."""
        return []

    def apply(self, img: cv.Mat, params: dict[str, Any]) -> cv.Mat:
        """Apply the filter to the image."""
        img1 = np.zeros((img.shape[0], img.shape[1], 3), dtype="uint8")
        for x in range(0, img.shape[0], 6):
            for y in range(0, img.shape[1], 4):
                b, g, r = img[int(x), int(y)]
                n = rnt(0, 1)
                c = (int(b), int(g), int(r))
                cv.putText(
                    img1,
                    text=str(n),
                    org=(y, x),
                    fontFace=5,
                    fontScale=0.3,
                    color=c,
                    thickness=0,
                )
        return img1


if __name__ == "__main__":
    filter = NumberFilter()
    params = filter.get_params()
    param_dict = {param.name: param for param in params}
    img = cv.imread(r"park.jpg")
    cv.imshow("Original", img)
    img = filter.apply(img, param_dict)
    cv.imshow("Numbered", img)
    cv.waitKey(0)
    cv.destroyAllWindows()
