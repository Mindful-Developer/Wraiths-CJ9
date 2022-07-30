"""Filter for a RGB shifted 3D glasses effect"""

from random import randint as rnt
from typing import Any, List

import cv2 as cv  # type: ignore
import numpy as np

from src.glitchup.web.filters.image_filter import ImageFilter
from src.glitchup.web.filters.parameter import Parameter, ParamType


class Shiftrgb(ImageFilter):
    """Splits the image into 3 colors, creating a 3D glasses look."""

    # filter_id = ???

    @staticmethod
    def metadata() -> tuple[int, list[Parameter]]:
        """Return a tuple with the inputs and parameters of the filter."""
        return 1, [
            Parameter(
                ParamType.INT,
                "horizontal offset",
                default=8,
                param_range=(8, 80),
            ),
            Parameter(
                ParamType.INT, "scan line density", default=4, param_range=(2, 20)
            ),
        ]

    @classmethod
    def apply(cls, images: list[cv.Mat], params: dict[str, Any]) -> None:
        """Apply the filter to the image."""
        # Make RGB + Gray image copies for the shift
        x_offset = params["horizontal offset"].default
        line_density = params["scan line density"].default
        img = images[0].copy()
        # Red
        red = img[:, :, 2]
        red_img = np.zeros(img.shape, np.uint8)
        red_img[:, :, 2] = red

        # Green
        green = img[:, :, 1]
        green_img = np.zeros(img.shape, np.uint8)
        green_img[:, :, 1] = green

        # Blue
        blue = img[:, :, 0]
        blue_img = np.zeros(img.shape, np.uint8)
        blue_img[:, :, 0] = blue

        # Gray
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        gray = cv.cvtColor(gray, cv.COLOR_GRAY2BGR)

        for col in range(img.shape[1]):
            for row in range(0, img.shape[0], line_density):
                # col
                gray[:, col, 0] = blue[
                    :,
                    col + x_offset
                    if col + x_offset < img.shape[0]
                    else img.shape[0] - col - x_offset,
                ]
                if col > x_offset:
                    gray[:, col, 2] = red[:, col - x_offset]

                else:
                    gray[:, col, 2] = red[:, col]
                gray[:, col, 1] = green[:, col]

                # row
                gray[row, :, 0] = blue[
                    row - x_offset
                    if row + x_offset < img.shape[1]
                    else gray.shape[1] - row - x_offset,
                    :,
                ]

                if row > x_offset:
                    gray[row, :, 2] = red[row - x_offset, :]
                else:
                    gray[row, :, 2] = red[row, :]
                gray[row, :, 1] = green[row, :]

        cv.imwrite("shiftrgb.jpg", gray)
        cv.imshow("ShiftRGB", gray)


if __name__ == "__main__":

    params = Shiftrgb.metadata()[1]
    param_dict = {param.name: param for param in params}

    img = cv.imread(r"D:/test.jpg")
    cv.imshow("Original", img)
    Shiftrgb.apply([img], param_dict)
    cv.imshow("ShiftRGB", img)
    cv.waitKey(0)
    cv.destroyAllWindows()
