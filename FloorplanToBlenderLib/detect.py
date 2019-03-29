import cv2
import numpy as np

# TODO: detect windows
# TODO: detect doors
# Calculate size of appartment
# TODO: number of rooms count
# TODO: text detection


def wall_filter(gray):
    '''
    Filter walls
    @Return our thick wallmap
    '''

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

def detectCorners(detect_img, output_img = None, color = [255,0,0] ):
    '''
    Find each corner
    '''
    corners = cv2.goodFeaturesToTrack(detect_img, 1000, 0.1, 1)
    corners = np.int0(corners)

    if output_img is not None:
        for corner in corners:
            x,y = corner.ravel()
            cv2.circle(output_img,(x,y),3,255,-1)
    return corners, output_img

def Watermark(detect_img, output_img = None, color = [255,0,0]):
    '''
    Watershed

    https://docs.opencv.org/3.1.0/d3/db4/tutorial_py_watershed.html
    '''
    ret, markers = cv2.connectedComponents(detect_img)

    markers = markers+1
    markers[unknown==255] = 0
    if output_img is not None:
        markers = cv2.watershed(output_img,markers)
        output_img[markers == -1] = color
    return markers

def detectCenterBoxes(detect_img, output_img = None, color = [100,100,0]):
    '''
    Get center of objects

    https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_feature2d/py_features_harris/py_features_harris.html
    '''

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


def detectUnpreciseBoxes(detect_img, output_img = None, color = [100,100,0]):
    '''
    Bad boxes in image
    @Return boxes
    '''

    corners = cv2.cornerHarris(detect_img,2,3,0.04)
    res = cv2.dilate(corners, None, iterations=3)

    res = corners
    if output_img is not None:
        i = len(res)-1
        while i >= 0:
            cv2.rectangle(output_img,(int(res[i][0]),int(res[i][1])),(int(res[i][2]),int(res[i][3])),color,3)
            i -= 1
    return res, output_img

def detectPreciseBoxes(detect_img, output_img = None, color = [100,100,0]):
    '''
    Boxes in image
    @Return list of boxes

    Source
    https://stackoverflow.com/questions/50930033/drawing-lines-and-distance-to-them-on-image-opencv-python
    '''
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

def remove_noise(img, noise_removal_threshold):
    '''
    help function for finding room
    remove noise from image and return mask
    '''
    img[img < 128] = 0
    img[img > 128] = 255
    _, contours, _ = cv2.findContours(~img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mask = np.zeros_like(img)
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > noise_removal_threshold:
            cv2.fillPoly(mask, [contour], 255)
    return mask

def find_corners_and_draw_lines(img,corners_threshold, room_closing_max_length):
    '''
    help function for finding room
    '''
    # Detect corners (you can play with the parameters here)
    kernel = np.ones((1,1),np.uint8)
    dst = cv2.cornerHarris(img ,2,3,0.04)
    dst = cv2.erode(dst,kernel, iterations = 10)
    corners = dst > corners_threshold * dst.max()

    # Draw lines to close the rooms off by adding a line between corners on the same x or y coordinate
    # This gets some false positives.
    # You could try to disallow drawing through other existing lines for example.
    for y,row in enumerate(corners):
        x_same_y = np.argwhere(row)
        for x1, x2 in zip(x_same_y[:-1], x_same_y[1:]):

            if x2[0] - x1[0] < room_closing_max_length:
                color = 0
                cv2.line(img, (x1, y), (x2, y), color, 1)

    for x,col in enumerate(corners.T):
        y_same_x = np.argwhere(col)
        for y1, y2 in zip(y_same_x[:-1], y_same_x[1:]):
            if y2[0] - y1[0] < room_closing_max_length:
                color = 0
                cv2.line(img, (x, y1), (x, y2), color, 1)
    return img


def find_details(img, noise_removal_threshold=50, corners_threshold=0.01,
               room_closing_max_length=125, gap_in_wall_max_threshold=5000,
               gap_in_wall_min_threshold=10):

    """
    I have copied and changed this function some...

    origin from
    https://stackoverflow.com/questions/54274610/crop-each-of-them-using-opencv-python

    :param img: grey scale image of rooms, already eroded and doors removed etc.
    :param noise_removal_threshold: Minimal area of blobs to be kept.
    :param corners_threshold: Threshold to allow corners. Higher removes more of the house.
    :param room_closing_max_length: Maximum line length to add to close off open doors.
    :param gap_in_wall_threshold: Minimum number of pixels to identify component as room instead of hole in the wall.
    :return: rooms: list of numpy arrays containing boolean masks for each detected room
             colored_house: A colored version of the input image, where each room has a random color.
    """
    assert 0 <= corners_threshold <= 1
    # Remove noise left from door removal

    mask = remove_noise(img, noise_removal_threshold)
    img = ~mask

    find_corners_and_draw_lines(img,corners_threshold,room_closing_max_length)

    img, mask = mark_outside_black(img, mask)

    # Find the connected components in the house
    ret, labels = cv2.connectedComponents(img)
    img = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)
    unique = np.unique(labels)
    details = []
    for label in unique:
        component = labels == label
        if img[component].sum() == 0 or np.count_nonzero(component) < gap_in_wall_min_threshold or np.count_nonzero(component) > gap_in_wall_max_threshold:
            color = 0
        else:
            details.append(component)
            color = np.random.randint(0, 255, size=3)

        img[component] = color

    return details, img

def mark_outside_black(img, mask):
    # Mark the outside of the house as black
    _, contours, _ = cv2.findContours(~img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
    biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]
    mask = np.zeros_like(mask)
    cv2.fillPoly(mask, [biggest_contour], 255)
    img[mask == 0] = 0
    return img, mask


def find_rooms(img, noise_removal_threshold=50, corners_threshold=0.01,
               room_closing_max_length=125,
               gap_in_wall_min_threshold=5000):

    """
    I have copied and changed this function some...

    origin from
    https://stackoverflow.com/questions/54274610/crop-each-of-them-using-opencv-python

    :param img: grey scale image of rooms, already eroded and doors removed etc.
    :param noise_removal_threshold: Minimal area of blobs to be kept.
    :param corners_threshold: Threshold to allow corners. Higher removes more of the house.
    :param room_closing_max_length: Maximum line length to add to close off open doors.
    :param gap_in_wall_threshold: Minimum number of pixels to identify component as room instead of hole in the wall.
    :return: rooms: list of numpy arrays containing boolean masks for each detected room
             colored_house: A colored version of the input image, where each room has a random color.
    """
    assert 0 <= corners_threshold <= 1
    # Remove noise left from door removal

    mask = remove_noise(img, noise_removal_threshold)
    img = ~mask

    find_corners_and_draw_lines(img,corners_threshold,room_closing_max_length)

    img, mask = mark_outside_black(img, mask)

    # Find the connected components in the house
    ret, labels = cv2.connectedComponents(img)
    img = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)
    unique = np.unique(labels)
    rooms = []
    for label in unique:
        component = labels == label
        if img[component].sum() == 0 or np.count_nonzero(component) < gap_in_wall_min_threshold:
            color = 0
        else:
            rooms.append(component)
            color = np.random.randint(0, 255, size=3)
        img[component] = color
    return rooms, img


def detectAndRemovePreciseBoxes(detect_img, output_img = None, color = [255, 255, 255]):
    '''
    Remove contours
    @Return list of boxes

    Source
    https://stackoverflow.com/questions/50930033/drawing-lines-and-distance-to-them-on-image-opencv-python
    '''

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

def detectOuterContours(detect_img, output_img = None, color = [255, 255, 255]):
    '''
    Get the outer side of image
    @Return box

    Source
    https://stackoverflow.com/questions/50930033/drawing-lines-and-distance-to-them-on-image-opencv-python
    '''
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


def rectContains(rect,pt):
    '''
    Rect contains

    Source:
    https://stackoverflow.com/questions/33065834/how-to-detect-if-a-point-is-contained-within-a-bounding-rect-opecv-python
    '''
    return rect[0] < pt[0] < rect[0]+rect[2] and rect[1] < pt[1] < rect[1]+rect[3]


def detectLines(detect_img, output_img = None, color = [255, 255, 255]):
    '''
    Detect lines in image
    @Return list of lines

    Source:
    https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_houghlines/py_houghlines.html
    '''

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
