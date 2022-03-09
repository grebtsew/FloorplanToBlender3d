"""
Test function from stackoverflow
https://stackoverflow.com/questions/55356251/how-to-detect-doors-and-windows-from-a-floor-plan-image
"""

import cv2
import matplotlib.pyplot as plt
import numpy as np
import os

example_image_path = (
    os.path.dirname(os.path.realpath(__file__)) + "/../../../Images/Examples/example.png"
)

img = cv2.imread(example_image_path)

img_bw = 255 * (cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) > 20).astype("uint8")

se1 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
se2 = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
mask = cv2.morphologyEx(img_bw, cv2.MORPH_CLOSE, se1)
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, se2)

mask = np.dstack([mask, mask, mask]) / 255
out = img * mask
plt.figure(figsize=(15, 10))
plt.imshow(out, cmap="gray")
cv2.imshow("test", out)
cv2.waitKey(0)
