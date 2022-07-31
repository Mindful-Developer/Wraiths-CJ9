#! /usr/bin/env python3

"""Pixel sorting filter"""

from typing import Any

from cv2 import COLOR_BGR2HSV, COLOR_HSV2BGR, Mat, cvtColor

from glitchup.web.filters.image_filter import ImageFilter
from glitchup.web.filters.parameter import Parameter, ParamType


class PixelSort(ImageFilter):
    """Pixel sorting filter"""

    filter_id = 985

    NUM_INPUTS: int = 1
    PARAMETERS: list[Parameter] = [Parameter(ParamType.ENUM,
                                             'direction',
                                             'horizontal',
                                             ('horizontal', 'vertical')),
                                   Parameter(ParamType.ENUM,
                                             'index_parameter',
                                             'hue',
                                             ('hue', 'saturation', 'value',
                                              'red', 'green', 'blue'))]

    def __init__(self) -> None:
        pass

    def num_inputs(self) -> int:
        """Number of input images"""
        return self.NUM_INPUTS

    def metadata(self) -> tuple[int, list[Parameter]]:
        """Set of parameters"""
        return len(self.PARAMETERS), self.PARAMETERS

    def apply(self, images: list[Mat], params: dict[str, Any]) -> None:
        """Apply pixel sort to image"""
        # Extract only the first image
        image = images[0]

        # Apply default parameters
        parameters = {}
        for parameter in self.PARAMETERS:
            parameters[parameter.name] = parameter.default

        # apply passed-in parameters
        for name, value in params.items():
            if name not in parameters:
                raise KeyError(f'Unknown parameter "{name}"')
            parameters[name] = value

        # Apply filter
        self._filter(image, parameters)

    def _filter(self, img: Mat, params: dict[str, Any]) -> None:
        # Change colour space, if necessary
        match params['index_parameter']:
            case 'hue' | 'saturation' | 'value':
                cvtColor(img, COLOR_BGR2HSV, img)
            case 'red' | 'green' | 'blue':
                pass
            case _:
                raise ValueError(f'Unknown index parameter "{params["index_parameter"]}')

        # Always sort rows. Sorting columns is done via transposition
        iter_img = img
        match params['direction']:
            case 'horizontal':
                iter_img = img
            case 'vertical':
                iter_img = img.transpose((1, 0, 2))
            case _:
                raise ValueError(f'Unknown direction "{params["direction"]}"')

        # Perform the sort. This could probably be cleaned up at some point.
        for row in iter_img:
            match params['index_parameter']:
                case 'hue' | 'blue':
                    row[:] = row[row[:, 0].argsort()]
                case 'saturation' | 'green':
                    row[:] = row[row[:, 1].argsort()]
                case 'value' | 'red':
                    row[:] = row[row[:, 2].argsort()]

        # Revert colour space, if necessary
        match params['index_parameter']:
            case 'hue' | 'saturation' | 'value':
                cvtColor(img, COLOR_HSV2BGR, img)
            case 'red' | 'green' | 'blue':
                pass


def main() -> None:
    """Tests"""
    import os

    from cv2 import imread, imwrite

    INPUT_DIR = 'input_images'
    OUTPUT_DIR = 'output_dir'

    filt = PixelSort()
    for filename in os.listdir(INPUT_DIR):
        print(f'Loading {filename}...')
        input_path = os.path.join(INPUT_DIR, filename)
        name, ext = os.path.splitext(filename)
        img = imread(input_path)

        print(f'Saving copy of {filename}')
        output_filename = filename
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        imwrite(output_path, img)

        for direction in ('horizontal', 'vertical'):
            for index_parameter in ('hue', 'saturation', 'value',
                                    'red', 'green', 'blue'):
                params = {'direction': direction,
                          'index_parameter': index_parameter}

                print(f'Applying PixelSort filter ({direction}, {index_parameter})...')
                img_copy = img.copy()
                filt.apply([img_copy], params)

                output_filename = name + f'-{direction}-{index_parameter}' + ext

                print(f'Saving {output_filename}...')
                output_path = os.path.join(OUTPUT_DIR, output_filename)
                imwrite(output_path, img_copy)


if __name__ == '__main__':
    main()
