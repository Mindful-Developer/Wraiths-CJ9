"""Temporarily using this to test all filters at once."""

# import pytest
import cv2
from glitchup.filters import dottedfilter, ghosting


if __name__ == "__main__":
    filter_list = [dottedfilter.DottedFilter, ghosting.Ghosting]
    test_img_path = "D:/test.jpg"

    for filter_class in filter_list:
        param_list = filter_class.get_params()
        param_dict = {param.name: param for param in param_list}
        img = cv2.imread(test_img_path)
        cv2.imshow("Original", img)
        filter_class.apply([img], param_dict)
        cv2.imshow(filter_class.__name__, img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()