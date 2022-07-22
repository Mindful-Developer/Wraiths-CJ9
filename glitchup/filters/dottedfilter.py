from typing import Tuple
import cv2 as cv
from matplotlib.pyplot import get
import numpy as np
from random import randint as rnt

# Read the image
# the_image = cv.imread('image.jpg')



def dottedfilter(img: np.ndarray, quantity: int=30000) -> np.ndarray:

    def get_rgb_colors(theimg: np.ndarray, num: int):
        def create_bar(height, width, color):
            # print(color)
            bar = np.zeros((height, width, 3), np.uint8)
            bar[:] = color
            red, green, blue = int(color[0]), int(color[1]), int(color[2])
            return bar, (red, green, blue)

        img = theimg
        height, width, _ = np.shape(img)
        # print(height, width)

        data = np.float32(np.reshape(img, (height * width, 3)))

        number_clusters = num
        criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        flags = cv.KMEANS_RANDOM_CENTERS
        _, _, centers = cv.kmeans(data, number_clusters, None, criteria, 10, flags)
        # print(centers)

        font = cv.FONT_HERSHEY_SIMPLEX
        bars = []
        rgb_values = []

        for index, row in enumerate(centers):
            bar, rgb = create_bar(200, 200, row)
            bars.append(bar)
            rgb_values.append(rgb)

        img_bar = np.hstack(bars)

        colors = []
        for index, row in enumerate(rgb_values):
            image = cv.putText(img_bar, f'{index + 1}. RGB: {row}', (5 + 200 * index, 200 - 10),
                                font, 0.5, (255, 0, 0), 1, cv.LINE_AA)
            # print(f'{index + 1}. RGB{row}')
            colors.append(row)
            # print(row)
        return colors, img_bar

    def modify(img, times, colors):
        # print(num)
        for x in range(times):
            num = (rnt(0, img.shape[1]), rnt(0, img.shape[0]))
            # num2 = (rnt(0, img.shape[1]), rnt(0, img.shape[0]))
            # print(x)
            cv.rectangle(img, num, (num[0],num[1]), (colors[rnt(0, len(colors)-1)]), cv.FILLED)


    # cv.imshow('Cat', img)
    colors, pallette_bar = get_rgb_colors(img, 3)
# print()
    modify(img, quantity, colors)


# Apply the filter
# dottedfilter(the_image)