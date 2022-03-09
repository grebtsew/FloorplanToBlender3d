import cv2
import os

"""
Detect corners of image
testing setting limits
"""

example_image_path = (
    os.path.dirname(os.path.realpath(__file__)) + "/../../../Images/Examples/example.png"
)

img = cv2.imread(example_image_path)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

corners = cv2.goodFeaturesToTrack(gray, 1000, 0.99999, 50)

for corner in corners:
    x, y = corner[0]
    x = int(x)
    y = int(y)
    cv2.rectangle(img, (x - 10, y - 10), (x + 10, y + 10), (0, 255, 0), 2)

cv2.imshow("Corners Found", img)
cv2.waitKey()
cv2.destroyAllWindows()
