"""Filter image to a zero and one image with blurred background"""
from random import randint as rnt
from typing import Any

import cv2 as cv

from glitchup.filters.image_filter import ImageFilter
from glitchup.filters.parameter import Parameter


class NumberFilter(ImageFilter):
    """Add random dots on the image"""

    def num_inputs(self) -> int:
        """Return the number of inputs this filter requires."""
        return 1

    def get_params(self) -> list[Parameter]:
        """Return the list of parameters for this filter."""
        return [
            Parameter(Parameter.ParamType.INT, "Blur", default=30, param_range=(1, 100))
        ]

    def apply(self, img: cv.Mat, params: dict[str, Any]) -> cv.Mat:
        """Apply the filter to the image."""
        blur_num = params["Blur"].default
        img = cv.blur(img, (blur_num, blur_num))
        for x in range(0, img.shape[0], 20):
            for y in range(0, img.shape[1], 20):
                b, g, r = img[int(x), int(y)]
                n = rnt(0, 1)
                c = (int(b + 50), int(g + 50), int(r + 50))
                cv.putText(
                    img,
                    text=str(n),
                    org=(y, x),
                    fontFace=5,
                    fontScale=1,
                    color=c,
                    thickness=3,
                )
        return img


if __name__ == "__main__":
    filter = NumberFilter()
    params = filter.get_params()
    param_dict = {param.name: param for param in params}
    img = cv.imread(r"cats.jpg")
    img = filter.apply(img, param_dict)
    cv.imshow("Numbered", img)
    cv.waitKey(0)
    cv.destroyAllWindows()
