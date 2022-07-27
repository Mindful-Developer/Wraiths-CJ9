"""Filter for a ghosting effect"""

from typing import Any

import cv2
from cv2 import Mat

from .image_filter import ImageFilter
from .parameter import Parameter, ParamType

__all__ = ("Ghosting",)


class Ghosting(ImageFilter):
    """Blurs the image in the positive direction on the y-axis"""

    filter_id = 982

    @staticmethod
    def metadata() -> tuple[int, list[Parameter]]:
        """Return a tuple containing the inputs and parameters of the filter."""
        return 1, [
            Parameter(
                ParamType.INT,
                "opacity",
                default=0.25,
                param_range=(0.0, 0.75),
            ),
            Parameter(
                ParamType.INT,
                "number of ghosts",
                default=10,
                param_range=(7, 13),
            ),
        ]

    @classmethod
    def apply(cls, images: list[Mat], params: dict[str, Any]) -> None:
        """Apply the filter to the image."""
        image = images[0]
        opacity = params["opacity"].default
        num_ghosts = params["number of ghosts"].default

        for i in range(num_ghosts):
            y = i * i

            # Create a copy of the image and translate it down
            translated_image = cv2.copyMakeBorder(
                image, y, y + 1, 0, 0, cv2.BORDER_CONSTANT, value=(0, 0, 0)
            )

            # Remove the excess pixels
            translated_image = translated_image[0:image.shape[0], 0:image.shape[1]]

            # Blend the images together
            cv2.addWeighted(translated_image, opacity, image, 1 - opacity, 0, image)


if __name__ == "__main__":
    filter = Ghosting()
    params = filter.metadata()[1]
    param_dict = {param.name: param for param in params}
    img = cv2.imread(r"D:\test.jpg")
    cv2.imshow("Original", img)
    filter.apply([img], param_dict)
    cv2.imshow("Ghosting", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
