import cv2
import numpy as np

'''
Main function for testing and visualising

https://mathematica.stackexchange.com/questions/19546/image-processing-floor-plan-detecting-rooms-borders-area-and-room-names-t
'''
def main():
    img = cv2.imread("example2.png")


    height, width, channels = img.shape
    blank_image = np.zeros((height,width,3), np.uint8) # output image same size as original

    # grayscale
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # create wall image
    wall_img = wall_filter(gray)

    # detect corners
    corners, img = detectCorners(wall_img, img, [255,0,0])

    # detect boxes
    boxes, img = detectPreciseBoxes(wall_img, img ,[100,100,0])

    #detect outer Contours
    contour, img = detectOuterContours(gray, img, [0,255,0])

    # Show images
    cv2.imshow("a", img)
    cv2.imshow("b", wall_img)
    cv2.imshow("c", gray)

    # Exit
    cv2.waitKey()
    cv2.destroyAllWindows()

'''
Test function for future use
'''
def test():

    '''
    Receive image, convert
    '''
    # Read floorplan image
    img = cv2.imread("example2.png")

    # grayscale image
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    '''
    Detect objects in image
    '''
    # create wall image (filter out small objects from image)
    wall_img = wall_filter(gray)

    # detect walls
    boxes, img = detectPreciseBoxes(wall_img)

    # detect outer Contours (simple floor or roof solution)
    contour, img = detectOuterContours(gray)

    # create verts (points 3d)
    verts = []
    # create faces for each plane
    faces = []

    wall_height = 1

    scale = 100

    '''
    Scale and create array of box_verts
    [[box1],[box2],...]
    '''

    # for each wall group
    for box in boxes:
        temp_verts = []
        # for each pos
        for pos in box:

        # add and convert all positions
            temp_verts.extend([(pos[0][0]/scale, pos[0][1]/scale, 0.0)])
            temp_verts.extend([(pos[0][0]/scale, pos[0][1]/scale, wall_height)])

        # add box to list
        verts.extend(temp_verts)

    '''
    Create faces for each point and create mesh
    We want to build each wall as a mesh
    Therefore we split the each vert and send 4 points to each mesh
    '''
    for box in verts:

        # for each two points
        for i in Range(0, len(box) % 4):
            t = i*2
            temp_vert = []
            #Verts to send
            temp_vert.extend(box[i])
            temp_vert.extend(box[i+2])
            temp_vert.extend(box[i+3])
            temp_vert.extend(box[i+1])

            # faces
            faces.extend([(0,1,2,3)])

            # Create mesh



        pass

'''
Filter walls
@Return our thick wallmap
'''
def wall_filter(gray):
    ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    # noise removal
    kernel = np.ones((3,3),np.uint8)
    opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)

    sure_bg = cv2.dilate(opening,kernel,iterations=3)

    dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
    ret, sure_fg = cv2.threshold(0.5*dist_transform,0.2*dist_transform.max(),255,0)

    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg,sure_fg)

    return unknown

'''
Find each corner
'''
def detectCorners(detect_img, output_img = None, color = [255,0,0] ):
    corners = cv2.goodFeaturesToTrack(detect_img, 1000, 0.1, 1)
    corners = np.int0(corners)

    if output_img is not None:
        for corner in corners:
            x,y = corner.ravel()
            cv2.circle(output_img,(x,y),3,255,-1)
    return corners, output_img

'''
Watershed

https://docs.opencv.org/3.1.0/d3/db4/tutorial_py_watershed.html
'''
def Watermark(detect_img, output_img = None, color = [255,0,0]):
    ret, markers = cv2.connectedComponents(detect_img)

    markers = markers+1
    markers[unknown==255] = 0
    if output_img is not None:
        markers = cv2.watershed(output_img,markers)
        output_img[markers == -1] = color
    return markers

'''
Get center of objects

https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_feature2d/py_features_harris/py_features_harris.html
'''
def detectCenterBoxes(detect_img, output_img = None, color = [100,100,0]):
    # find centroids
    ret, labels, stats, centroids = cv2.connectedComponentsWithStats(detect_img,4)

    # define the criteria to stop and refine the corners
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
    corners = cv2.cornerSubPix(detect_img,np.float32(centroids),(5,5),(-1,-1),criteria)

    # Now draw them
    res = np.hstack((centroids,corners))
    res = np.int0(res)
    if output_img is not None:
        output_img[res[:,1],res[:,0]]=[0,0,255]
        output_img[res[:,3],res[:,2]] = [0,255,0]

        i = len(res)-1
        print(res)
        while i >= 0:
            cv2.rectangle(output_img,(int(res[i][0]),int(res[i][1])),(int(res[i][2]),int(res[i][3])),color,3)
            i -= 1
    return res, output_img


'''
Bad boxes in image
@Return boxes
'''
def detectUnpreciseBoxes(detect_img, output_img = None, color = [100,100,0]):
    corners = cv2.cornerHarris(detect_img,2,3,0.04)
    res = cv2.dilate(corners, None, iterations=3)

    res = stats
    if output_img is not None:
        i = len(res)-1
        while i >= 0:
            cv2.rectangle(output_img,(int(res[i][0]),int(res[i][1])),(int(res[i][2]),int(res[i][3])),color,3)
            i -= 1
    return res, output_img

'''
Boxes in image
@Return list of boxes

Source
https://stackoverflow.com/questions/50930033/drawing-lines-and-distance-to-them-on-image-opencv-python
'''
def detectPreciseBoxes(detect_img, output_img = None, color = [100,100,0]):
    res = []

    im, contours, hierarchy = cv2.findContours(detect_img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    #area = sorted(contours, key=cv2.contourArea, reverse=True)

    largest_contour_area = 0
    for cnt in contours:
        largest_contour_area = cv2.contourArea(cnt)
        largest_contour = cnt

        epsilon = 0.001*cv2.arcLength(largest_contour,True)
        approx = cv2.approxPolyDP(largest_contour,epsilon,True)
        if output_img is not None:
            final = cv2.drawContours(output_img, [approx], 0, [100, 200, 0])
        res.append(approx)

    return res, output_img

'''
Remove contours
@Return list of boxes

Source
https://stackoverflow.com/questions/50930033/drawing-lines-and-distance-to-them-on-image-opencv-python
'''
def detectAndRemovePreciseBoxes(detect_img, output_img = None, color = [255, 255, 255]):
    res = []

    im, contours, hierarchy = cv2.findContours(detect_img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    #area = sorted(contours, key=cv2.contourArea, reverse=True)

    largest_contour_area = 0
    for cnt in contours:
        largest_contour_area = cv2.contourArea(cnt)
        largest_contour = cnt

        epsilon = 0.001*cv2.arcLength(largest_contour,True)
        approx = cv2.approxPolyDP(largest_contour,epsilon,True)
        if output_img is not None:
            cv2.drawContours( output_img,  [approx], -1, color, -1);
        res.append(approx)

    return res, output_img

'''
Get the outer side of image
@Return box

Source
https://stackoverflow.com/questions/50930033/drawing-lines-and-distance-to-them-on-image-opencv-python
'''
def detectOuterContours(detect_img, output_img = None, color = [255, 255, 255]):

    ret, thresh = cv2.threshold(detect_img, 230, 255, cv2.THRESH_BINARY_INV)

    img_, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    largest_contour_area = 0
    for cnt in contours:
        if (cv2.contourArea(cnt) > largest_contour_area):
            largest_contour_area = cv2.contourArea(cnt)
            largest_contour = cnt

    epsilon = 0.001*cv2.arcLength(largest_contour,True)
    approx = cv2.approxPolyDP(largest_contour,epsilon,True)
    if output_img is not None:
        final = cv2.drawContours(output_img, [approx], 0, color)
    return approx, output_img


'''
Rect contains

Source:
https://stackoverflow.com/questions/33065834/how-to-detect-if-a-point-is-contained-within-a-bounding-rect-opecv-python
'''
def rectContains(rect,pt):
    return rect[0] < pt[0] < rect[0]+rect[2] and rect[1] < pt[1] < rect[1]+rect[3]


'''
Detect lines in image
@Return list of lines

Source:
https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_houghlines/py_houghlines.html
'''
def detectLines(detect_img, output_img = None, color = [255, 255, 255]):
    edges = cv2.Canny(detect_img,50,120)
    minLineLength = 20
    maxLineGap = 50
    lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)
    i = len(lines)-1

    if output_img is not None:
        while i > 0:
            i -= 1;
            for x1,y1,x2,y2 in lines[i]:
                cv2.line(output_img,(x1,y1),(x2,y2),color,2)

    return lines, output_img


'''
Uncomment this for testing
'''
if __name__ == "__main__":
    test()
#    main()
