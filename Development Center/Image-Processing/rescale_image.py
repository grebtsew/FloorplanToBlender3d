import cv2
import os
import numpy as np
from PIL import Image

example_image_path = (
    os.path.dirname(os.path.realpath(__file__)) + "/../../Images/Examples/example2.png"
)

scalefactor = 2.5  # downscale < 1 < upscale


def pil_rescale_image(image, factor):

    width, height = image.size
    d = image.resize((int(width * factor), int(height * factor)), resample=Image.BOX)

    return d


def cv2_rescale_image(image, factor):
    return cv2.resize(image, None, fx=factor, fy=factor)


def pil_to_cv2(image):
    return cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)


def main():
    # Pil read
    c = Image.open(example_image_path)

    # for cv2
    d = cv2_rescale_image(pil_to_cv2(c), scalefactor)

    # for pil
    d2 = pil_rescale_image(c, scalefactor)
    d2 = pil_to_cv2(d2)

    # Show result
    cv2.imshow("origin", pil_to_cv2(c))
    cv2.imshow("reshape-cv2", d)
    cv2.imshow("reshape-pil", d2)
    cv2.waitKey(0)

    # Save to file
    # cv2.imwrite(os.path.dirname(os.path.realpath(__file__))+"/rescaled.png",pil_to_cv2(d2))


if __name__ == "__main__":
    main()
