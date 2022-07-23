""" Make a image looks dotted"""
from random import randint as rnt
from typing import Any, List

import cv2 as cv
import numpy as np

# Read the image
# the_image = cv.imread('image.jpg')
def dottedfilter(img: Any, quantity: int = 30000) -> None:
    """ Make a image looks dotted """
    def get_rgb_colors(theimg: Any, num: int) -> List[Any]:
        def create_bar(color: Any) -> tuple[int, int, int]:
            red, green, blue = int(color[0]), int(color[1]), int(color[2])
            return (red, green, blue)

        img = theimg
        height, width, _ = np.shape(img)
        # print(height, width)

        data = np.float32(np.reshape(img, (height * width, 3)))

        number_clusters = num
        criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        flags = cv.KMEANS_RANDOM_CENTERS
        _, _, centers = cv.kmeans(data, number_clusters, None, criteria, 10, flags)
        # print(centers)

        rgb_values = []

        for _, row in enumerate(centers):
            rgb = create_bar(row)
            rgb_values.append(rgb)

        colors = []
        for _, row in enumerate(rgb_values):
            colors.append(row)
        return colors

    def modify(img: Any, times: int, colors: List[Any]) -> None:

        for _ in range(times):
            num = (rnt(0, img.shape[1]), rnt(0, img.shape[0]))

            cv.rectangle(img, num, (num[0], num[1]), (colors[rnt(0, len(colors)-1)]), cv.FILLED)

        return

    colors, _ = get_rgb_colors(img, 3)
    modify(img, quantity, colors)

    return

# Apply the filter
# dottedfilter(the_image)
