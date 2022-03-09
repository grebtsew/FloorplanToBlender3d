# remove small lines or dots on map, also polate color
# https://docs.opencv.org/4.5.2/d5/d69/tutorial_py_non_local_means.html

import numpy as np
import cv2
from matplotlib import pyplot as plt
import cv2
import os
import numpy as np
from PIL import Image


def main():
    example_image_path = (
        os.path.dirname(os.path.realpath(__file__)) + "/../../Images/Examples/example.png"
    )

    img = cv2.imread(example_image_path)

    dst = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)

    cv2.imshow("origin", img)
    cv2.imshow("denoised", dst)
    cv2.waitKey(0)


if __name__ == "__main__":
    main()
