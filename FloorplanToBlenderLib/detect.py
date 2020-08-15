import cv2
import numpy as np

# TODO: detect windows
# TODO: detect doors
# Calculate (actual) size of appartment
# TODO: text detection

"""
Detect
This file contains functions used when detecting and calculating shapes in images.

FloorplanToBlender3d
Copyright (C) 2019 Daniel Westberg
"""

def wall_filter(gray):
    """
    Filter walls
    Filter out walls from a grayscale image
    @Param image
    @Return image of walls
    """
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


def detectPreciseBoxes(detect_img, output_img = None, color = [100,100,0]):
    """
    Detect corners with boxes in image with high precision
    @Param detect_img image to detect from @mandatory
    @Param output_img image for output
    @Param color to set on output
    @Return corners(list of boxes), output image
    @source https://stackoverflow.com/questions/50930033/drawing-lines-and-distance-to-them-on-image-opencv-python
    """
    res = []

    contours, hierarchy = cv2.findContours(detect_img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    #area = sorted(contours, key=cv2.contourArea, reverse=True)

    largest_contour_area = 0
    for cnt in contours:
        largest_contour_area = cv2.contourArea(cnt)
        largest_contour = cnt

        epsilon = 0.001*cv2.arcLength(largest_contour,True)
        approx = cv2.approxPolyDP(largest_contour,epsilon,True)
        if output_img is not None:
            final = cv2.drawContours(output_img, [approx], 0, color)
        res.append(approx)

    return res, output_img

def remove_noise(img, noise_removal_threshold):
    """
    Remove noise from image and return mask
    Help function for finding room
    @Param img @mandatory image to remove noise from
    @Param noise_removal_threshold @mandatory threshold for noise
    @Return return new mask of image
    """
    img[img < 128] = 0
    img[img > 128] = 255
    contours, _ = cv2.findContours(~img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mask = np.zeros_like(img)
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > noise_removal_threshold:
            cv2.fillPoly(mask, [contour], 255)
    return mask

def find_corners_and_draw_lines(img, corners_threshold, room_closing_max_length):
    """
    Finds corners and draw lines from them
    Help function for finding room
    @Param image input image
    @Param corners_threshold threshold for corner distance
    @Param room_closing_max_length threshold for room max size
    @Return output image
    """
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
                cv2.line(img, (x1[0], y), (x2[0], y), color, 1)

    for x,col in enumerate(corners.T):
        y_same_x = np.argwhere(col)
        for y1, y2 in zip(y_same_x[:-1], y_same_x[1:]):
            if y2[0] - y1[0] < room_closing_max_length:
                color = 0
                cv2.line(img, (x, y1[0]), (x, y2[0]), color, 1)
    return img



def mark_outside_black(img, mask):
    """
    Mark white background as black
    @Param @mandatory img image input
    @Param @mandatory mask mask to use
    @Return image, mask
    """
    # Mark the outside of the house as black
    contours, _ = cv2.findContours(~img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
    biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]
    mask = np.zeros_like(mask)
    cv2.fillPoly(mask, [biggest_contour], 255)
    img[mask == 0] = 0
    return img, mask


def find_rooms(img, noise_removal_threshold=50, corners_threshold=0.01,
               room_closing_max_length=130,
               gap_in_wall_min_threshold=5000):

    """
    I have copied and changed this function some...

    origin from
    https://stackoverflow.com/questions/54274610/crop-each-of-them-using-opencv-python

    @param img: grey scale image of rooms, already eroded and doors removed etc.
    @param noise_removal_threshold: Minimal area of blobs to be kept.
    @param corners_threshold: Threshold to allow corners. Higher removes more of the house.
    @param room_closing_max_length: Maximum line length to add to close off open doors.
    @param gap_in_wall_threshold: Minimum number of pixels to identify component as room instead of hole in the wall.
    @return: rooms: list of numpy arrays containing boolean masks for each detected room
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
    """
    Remove contours of detected walls from image
    @Param detect_img image to detect from @mandatory
    @Param output_img image for output
    @Param color to set on output
    @Return list of boxes, actual image
    @source https://stackoverflow.com/questions/50930033/drawing-lines-and-distance-to-them-on-image-opencv-python
    """

    res = []

    contours, hierarchy = cv2.findContours(detect_img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
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
    """
    Get the outer side of floorplan, used to get ground
    @Param detect_img image to detect from @mandatory
    @Param output_img image for output
    @Param color to set on output
    @Return approx, box
    @Source https://stackoverflow.com/questions/50930033/drawing-lines-and-distance-to-them-on-image-opencv-python
    """
    ret, thresh = cv2.threshold(detect_img, 230, 255, cv2.THRESH_BINARY_INV)

    contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

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
    """
    Count if Rect contains point
    @Param rect rectangle
    @Param pt point
    @Return boolean
    @source: https://stackoverflow.com/questions/33065834/how-to-detect-if-a-point-is-contained-within-a-bounding-rect-opecv-python
    """
    return rect[0] < pt[0] < rect[0]+rect[2] and rect[1] < pt[1] < rect[1]+rect[3]


'''
Currently none used code below here!, outcommented to avoid confusion with contributors.
'''

def find_details(img, noise_removal_threshold=50, corners_threshold=0.01,
               room_closing_max_length=130, gap_in_wall_max_threshold=5000,
               gap_in_wall_min_threshold=10):

    """
    !!! Currently not used in IMPLEMENTATION !!!
    I have copied and changed this function some...

    origin from
    https://stackoverflow.com/questions/54274610/crop-each-of-them-using-opencv-python

    @Param img: grey scale image of rooms, already eroded and doors removed etc.
    @Param noise_removal_threshold: Minimal area of blobs to be kept.
    @Param corners_threshold: Threshold to allow corners. Higher removes more of the house.
    @Param room_closing_max_length: Maximum line length to add to close off open doors.
    @Param gap_in_wall_threshold: Minimum number of pixels to identify component as room instead of hole in the wall.
    @Return: rooms: list of numpy arrays containing boolean masks for each detected room
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
