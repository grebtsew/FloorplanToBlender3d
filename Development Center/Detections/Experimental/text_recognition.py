import cv2
import numpy as np
import os

# Low prio!
# TODO add this in implementation!
# TODO add tesseract to read the text aswell

"""
Text recognition test
"""

example_image_path = (
    os.path.dirname(os.path.realpath(__file__)) + "/../../../Images/Examples/example.png"
)


img = cv2.imread(example_image_path)
mask = np.zeros(img.shape, dtype=np.uint8)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

gray = cv2.GaussianBlur(gray, (9, 9), 1)
_, threshold = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
contours, hierarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

ROI = []

for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    if h < 20:
        cv2.drawContours(mask, [cnt], 0, (255, 255, 255), 1)

kernel = np.ones((7, 7), np.uint8)
dilation = cv2.dilate(mask, kernel, iterations=1)
gray_d = cv2.cvtColor(dilation, cv2.COLOR_BGR2GRAY)
_, threshold_d = cv2.threshold(gray_d, 150, 255, cv2.THRESH_BINARY)
contours_d, hierarchy = cv2.findContours(
    threshold_d, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE
)

for cnt in contours_d:
    x, y, w, h = cv2.boundingRect(cnt)
    if w > 50:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        roi_c = img[y : y + h, x : x + w]
        ROI.append(roi_c)

cv2.imshow("img", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
