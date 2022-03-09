import cv2
import numpy as np
import os

"""
Here we test OD template detection on windows

Problem with this solution is that we would need to test all 360 angles...
"""

example_image_path = (
    os.path.dirname(os.path.realpath(__file__)) + "/../../../Images/Examples/example.png"
)
window_image_path = (
    os.path.dirname(os.path.realpath(__file__)) + "/../../../Images/Models/Windows/window.png"
)

image = cv2.imread(example_image_path)
cv2.imshow("people", image)
cv2.waitKey(0)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

template = cv2.imread(window_image_path, 0)
w, h = template.shape
# result of template matching of object over an image
result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF)
sin_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

top_left = max_loc
# increasing the size of bounding rectangle by 50 pixels
bottom_right = (top_left[0] + h, top_left[1] + w)
cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 5)

cv2.imshow("object found", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
