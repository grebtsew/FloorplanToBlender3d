
import cv2
import numpy as np
from matplotlib import pyplot as plt

'''
https://docs.opencv.org/3.1.0/d3/db4/tutorial_py_watershed.html

https://mathematica.stackexchange.com/questions/19546/image-processing-floor-plan-detecting-rooms-borders-area-and-room-names-t

Using opencv
'''

img = cv2.imread("example.png")

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

# noise removal
kernel = np.ones((3,3),np.uint8)
opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)

sure_bg = cv2.dilate(opening,kernel,iterations=3)

dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
ret, sure_fg = cv2.threshold(dist_transform,0.02*dist_transform.max(),255,0)

sure_fg = np.uint8(sure_fg)
unknown = cv2.subtract(sure_bg,sure_fg)



'''
Find each corner

'''
corners = cv2.goodFeaturesToTrack(unknown, 100, 0.01, 10)
corners = np.int0(corners)


for corner in corners:
    x,y = corner.ravel()
    cv2.circle(unknown,(x,y),3,255,-1)


'''
Show on original image
ret, markers = cv2.connectedComponents(sure_fg)

markers = markers+1
markers[unknown==255] = 0
markers = cv2.watershed(img,markers)
img[markers == -1] = [255,0,0]


cv2.imshow('img', img)
'''


'''

Get center of objects
https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_feature2d/py_features_harris/py_features_harris.html

# find centroids
ret, labels, stats, centroids = cv2.connectedComponentsWithStats(sure_fg,4)


# define the criteria to stop and refine the corners
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
corners = cv2.cornerSubPix(unknown,np.float32(centroids),(5,5),(-1,-1),criteria)

# Now draw them
res = np.hstack((centroids,corners))
res = np.int0(res)
#img[res[:,1],res[:,0]]=[0,0,255]
#img[res[:,3],res[:,2]] = [0,255,0]

#cv2.imshow('subpixel',img)
'''


'''
corners = cv2.cornerHarris(unknown,2,3,0.04)
res = cv2.dilate(corners, None, iterations=3)
'''
'''
res = stats
i = len(res)-1
print(res)
while i > 0:
    cv2.rectangle(unknown,(int(res[i][0]),int(res[i][1])),(int(res[i][2]),int(res[i][3])),(100,100,0),3)


    i -= 1

'''


'''
Boxes in image
https://stackoverflow.com/questions/50930033/drawing-lines-and-distance-to-them-on-image-opencv-python
'''
im, contours, hierarchy = cv2.findContours(unknown,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
area = sorted(contours, key=cv2.contourArea, reverse=True)

'''
i = len(area)-1

while i >= 0:
    c = area[i]
    rect = cv2.minAreaRect(c)
    box = cv2.boxPoints(rect)

    box = np.int0(box)
    cv2.drawContours(unknown,[box],0,(100,100,0),2)
    i-= 1



#cv2.imshow('Corner',unknown)
#cv2.imshow('image',img)
#print(len(res))
#cv2.imshow('show', corners)
'''

'''
Create array of walls
And show
'''



res = []
box_i = len(area)-1
corners_i = len(corners)-1

# find box

# find point1 in box
# find point2 in box
# draw between them


'''
Draw lines
https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_houghlines/py_houghlines.html
'''
'''
edges = cv2.Canny(unknown,50,150,apertureSize = 3)
minLineLength = 100
maxLineGap = 10
lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)
i = len(lines)-1
while i > 0:
    i -= 1;
    for x1,y1,x2,y2 in lines[i]:
        cv2.line(unknown,(x1,y1),(x2,y2),(100,100,0),2)

#cv2.imshow('houghlines5',img)

#cv2.line(img,(0,0),(511,511),(255,0,0),5)
'''


cv2.imshow('image',unknown)
cv2.waitKey(0)



'''
Wall exist
'''
def wallExist(wall_list, wall):
    return wall in wall_list

'''
Rect contains

Source:
https://stackoverflow.com/questions/33065834/how-to-detect-if-a-point-is-contained-within-a-bounding-rect-opecv-python
'''
def rectContains(rect,pt):
    logic = rect[0] < pt[0] < rect[0]+rect[2] and rect[1] < pt[1] < rect[1]+rect[3]
    return logic
