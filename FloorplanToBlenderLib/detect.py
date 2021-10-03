import cv2
import numpy as np
from . import image
from . import const
from . import IO
from . import draw
from . import image
import math

# Calculate (actual) size of apartment

"""
Detect
This file contains functions used when detecting and calculating shapes in images.

FloorplanToBlender3d
Copyright (C) 2021 Daniel Westberg
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

    mask = image.remove_noise(img, noise_removal_threshold)
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

def points_are_inside_or_close_to_box(door,box):

    for point in door:
        if rectContainsOrAlmostContains(point, box):
            return True
            break

def angle(vector1, vector2):
    x1, y1 = vector1
    x2, y2 = vector2
    inner_product = x1*x2 + y1*y2
    len1 = math.hypot(x1, y1)
    len2 = math.hypot(x2, y2)
    return math.acos(inner_product/(len1*len2))

def rectContainsOrAlmostContains(pt, box):

    x,y,w,h = cv2.boundingRect(box)
    isInside = x < pt[0] <x+w and y < pt[1] < y+h
    
    almostInside = False

    min_dist = 0
    if (w < h):
        min_dist = (w)
    else:
         min_dist = (h)

    for point in box:
        dist = abs(point[0][0]-pt[0])+abs(point[0][1]-pt[1])
        if (dist <= min_dist):
            almostInside = True
            break

    return isInside or almostInside

def doors(image_path, scale_factor):
    model = cv2.imread(const.DOOR_MODEL,0)
    img = cv2.imread(image_path,0)

    img = image.cv2_rescale_image(img, scale_factor)
    _, doors = feature_match(img, model)
    return doors

def windows(image_path, scale_factor):
    model = cv2.imread(const.DOOR_MODEL,0)
    img = cv2.imread(image_path,0)

    img = image.cv2_rescale_image(img, scale_factor)
    windows, _ = feature_match(img, model)   
    return windows

def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy

def scale_model_point_to_origin( origin, point,x_scale, y_scale):
            dx, dy = (point[0] - origin[0], point[1] - origin[1])
            return (dx * x_scale, dy * y_scale)

def calculate_best_matches_with_modulus_angle(match_list):
    # calculate best matches by looking at the most significant feature distances
    index1 = 0
    index2 = 0
    best = math.inf

    i = 0
    for match1 in match_list:
        j = 0
        for match2 in match_list:
            
            pos1_model = match_list[i][0]
            pos2_model = match_list[j][0]

            pos1_cap = match_list[i][1]
            pos2_cap = match_list[j][1]

            pt1 = (pos1_model[0]- pos2_model[0], pos1_model[1] -pos2_model[1])
            pt2 = (pos1_cap[0]-pos2_cap[0], pos1_cap[1]-pos2_cap[1])
            
            if pt1 == pt2 or pt1 == (0,0) or pt2 == (0,0):
                continue

            ang = math.degrees(angle(pt1, pt2))
            diff = ang % 30

            if diff < best :
                best = diff
                index1 = i
                index2 = j
    
            j += 1
        i += 1
    return index1, index2

def feature_match(img1, img2):
    MIN_MATCHES = 20
    cap = img1    
    model = img2
    # ORB keypoint detector
    orb = cv2.ORB_create(nfeatures=10000000, scoreType=cv2.ORB_FAST_SCORE)              
    # create brute force  matcher object
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)  
    # Compute model keypoints and its descriptors
    kp_model, des_model = orb.detectAndCompute(model, None)  
    # Compute scene keypoints and its descriptors
    kp_frame, des_frame = orb.detectAndCompute(cap, None)
    # Match frame descriptors with model descriptors
    matches = bf.match(des_model, des_frame)
    # Sort them in the order of their distance
    matches = sorted(matches, key=lambda x: x.distance)
    
    # calculate bounds
    # these are important for group matching!
    min_x = math.inf
    min_y = math.inf
    max_x = 0
    max_y = 0

    all_matches_pos = []
    for mat in matches:
        # Get the matching keypoints for each of the images
        img1_idx = mat.queryIdx
        img2_idx = mat.trainIdx

        # x - columns
        # y - rows
        # Get the coordinates
        (x1, y1) = kp_model[img1_idx].pt

        # bound checks
        if x1 < min_x:
            min_x = x1
        if x1 > max_x:
            max_x = x1
        
        if y1 < min_y:
            min_y = y1
        if y1 > max_y:
            max_y = y1

    # calculate min/max sizes!
    h = max_y - min_y
    w = max_x - min_x

    # Initialize lists
    list_grouped_matches = []

    # Create a list of objects containing matches  group on nearby matches
    for mat in matches:
        # Get the matching keypoints for each of the images
        img1_idx = mat.queryIdx
        img2_idx = mat.trainIdx

        # x - columns
        # y - rows
        # Get the coordinates
        (x1, y1) = kp_model[img1_idx].pt
        (x2, y2) = kp_frame[img2_idx].pt
        i = 0
        found = False

        for existing_match in list_grouped_matches:
            if abs(existing_match[0][1][0] - x2) < w and  abs(existing_match[0][1][1] - y2) < h:
                # add to group
                list_grouped_matches[i].append(((int(x1), int(y1)),(int(x2), int(y2))))
                found = True
                break
            # increment
            i += 1
        
        if not found:
            tmp = list()
            tmp.append(((int(x1), int(y1)),(int(x2), int(y2))))
            list_grouped_matches.append(list(list(list(tmp))))
        

    # Remove groups with only singles because we cant calculate rotation then!
    list_grouped_matches_filtered = []

    for match_group in list_grouped_matches:
        if len(match_group) >= 4 :
            list_grouped_matches_filtered.append(match_group)
        

    # find corners of door in model image
    corners = cv2.goodFeaturesToTrack(model, 3, 0.01, 20)
    corners = np.int0(corners)
    
    # This is still a little hardcoded but still better than before!
    upper_left = corners[1][0]
    upper_right =  corners[0][0]
    down = corners[2][0]

    max_x = 0
    max_y = 0
    min_x = math.inf
    min_y = math.inf

    for cr in corners:
        x1 = cr[0][0]
        y1 = cr[0][1]

        if x1 < min_x:
            min_x = x1
        if x1 > max_x:
            max_x = x1
        
        if y1 < min_y:
            min_y = y1
        if y1 > max_y:
            max_y = y1

    origin = (int((max_x+min_x)/2), int((min_y+max_y)/2))

    """
    # Show corners
    for corner in corners:
        x,y = corner.ravel()
        cv2.circle(model,(x,y),5,0,5)
    cv2.imshow('dst',model)
    cv2.waitKey(0)   
    """
    list_of_proper_transformed_doors = []

    doors_actual_pos = []
    # Calculate position and rotation of doors
    for match in list_grouped_matches_filtered:
        
        # calculate offsets from points
        index1, index2 = calculate_best_matches_with_modulus_angle(match)

        pos1_model = match[index1][0]
        pos2_model = match[index2][0]

        # calculate actual position from offsets with rotation!
        pos1_cap = match[index1][1]
        pos2_cap = match[index2][1]

        pt1 = (pos1_model[0]- pos2_model[0], pos1_model[1] -pos2_model[1])
        pt2 = (pos1_cap[0]-pos2_cap[0], pos1_cap[1]-pos2_cap[1])
        
        ang = math.degrees(angle(pt1, pt2))
        #print(index1, index2, ang)

        #print("Angle between doors ", ang)

        # rotate door
        new_upper_left = rotate(origin, upper_left, math.radians(ang))
        new_upper_right = rotate(origin, upper_right, math.radians(ang))
        new_down = rotate(origin, down, math.radians(ang))
        
        new_pos1_model = rotate(origin, pos1_model, math.radians(ang))

        # calculate scale, and rescale model
        """
        # TODO: fix this scaling problem!
        new_cap1 = rotate(origin, pos1_cap, math.radians(ang))
        new_cap2 = rotate(origin, pos2_cap, math.radians(ang))
        new_model1 = rotate(origin, pos1_model, math.radians(ang))
        new_model2 = rotate(origin, pos2_model, math.radians(ang))

        cap_size = [(new_cap1[0]- new_cap2[0]), (new_cap1[1]- new_cap2[1])]
        model_size = [(new_model1[0]-new_model2[0]),(new_model1[1]-new_model2[1])]
        
        
        if cap_size[1] != 0 or model_size[1] != 0:
            x_scale = abs(cap_size[0]/model_size[0])
            y_scale = abs(cap_size[1]/model_size[1])
            print(x_scale, y_scale)
            scaled_upper_left = scale_model_point_to_origin( origin, new_upper_left,x_scale, y_scale)
            #scaled_upper_right = scale_model_point_to_origin( origin, new_upper_right,x_scale, y_scale)
            #scaled_down = scale_model_point_to_origin( origin, new_down,x_scale, y_scale)
            scaled_pos1_model = scale_model_point_to_origin( origin, new_pos1_model,x_scale, y_scale)
        else:
        """
        scaled_upper_left = new_upper_left
        scaled_upper_right = new_upper_right
        scaled_down = new_down
        scaled_pos1_model = new_pos1_model
    

        offset = (scaled_pos1_model[0]-pos1_model[0], scaled_pos1_model[1]-pos1_model[1])

        # calculate dist!
        move_dist = (pos1_cap[0]- pos1_model[0],pos1_cap[1]- pos1_model[1])
        
        # draw corners!
        moved_new_upper_left = (int(scaled_upper_left[0]+move_dist[0] - offset[0]), int(scaled_upper_left[1]+move_dist[1]-offset[1] ))
        moved_new_upper_right =(int(scaled_upper_right[0]+move_dist[0] - offset[0]), int(scaled_upper_right[1]+move_dist[1]-offset[1] ))
        moved_new_down =( int(scaled_down[0]+move_dist[0] - offset[0]),int(scaled_down[1]+move_dist[1]-offset[1]) )

        #img2 = cv2.circle(cap, moved_new_upper_left, radius=4, color=(0, 0, 0), thickness=5)
        #img2 = cv2.circle(cap, moved_new_upper_right, radius=4, color=(0, 0, 0), thickness=5)
        #img2 = cv2.circle(cap, moved_new_down, radius=4, color=(0, 0, 0), thickness=5)
       
        list_of_proper_transformed_doors.append([moved_new_upper_left, moved_new_upper_right, moved_new_down])
     
    # draw door points
    #for match in list_grouped_matches_filtered:
    #img = cv2.circle(cap, (match[0][1][0],match[0][1][1]), radius=4, color=(0, 0, 0), thickness=5)


    # Draw matches as lines
    """
    if len(matches) > MIN_MATCHES:

        # draw first 15 matches.
        cap = cv2.drawMatches(model, kp_model, cap, kp_frame,
                            matches[:MIN_MATCHES], 0, flags=2)
        # show result
        #cv2.imshow('frame', cap)
        #cv2.waitKey(0)

    else:
        print( "Not enough matches have been found - %d/%d" % (len(matches),
                                                            MIN_MATCHES))
    """

    gray = wall_filter(img1)
    gray = ~gray
    rooms, colored_rooms = find_rooms(gray.copy())
    doors, colored_doors = find_details(gray.copy())
    gray_rooms =  cv2.cvtColor(colored_doors,cv2.COLOR_BGR2GRAY)

    # get box positions for rooms
    boxes, gray_rooms = detectPreciseBoxes(gray_rooms)

    windows = []
    doors = []
    # classify boxes
    # window, door, none
    for box in boxes:
    
        # is a door inside box?
        isDoor = False
        _door = []
        for door in list_of_proper_transformed_doors:
            
            if points_are_inside_or_close_to_box(door,box): # TODO: match door with only one box, the closest one!
                isDoor = True
                _door = door
                break
        
        if isDoor:
            doors.append((_door,box))
            continue
        
        # is window?
        x,y,w,h = cv2.boundingRect(box)
        cropped = img1[y:y+h, x:x+w]
        # bandpassfilter
        total = np.sum(cropped)
        colored = np.sum(cropped > 0)
        low = 0.001
        high = 0.00459
        
        amount_of_colored = colored/total
        
        if(low < amount_of_colored < high):
            windows.append(box)

    if True: # Draw doors
        #img3 = draw.doors(img1, doors)
        #draw.image(img3)
        pass

    if True: # Draw windows
        #img3= draw.boxesOnImage(img1, windows)
        #draw.image(img3)
        pass


    return rescale_rect(windows, 1.05), doors

def flatten(alist):
    if alist == []:
        return []
    elif type(alist) is not list:
        return [alist]
    else:
        return flatten(alist[0]) + flatten(alist[1:])

def rescale_rect(list_of_rects, scale_factor):
    
    rescaled_rects = []
    for rect in list_of_rects:
        x,y,w,h = cv2.boundingRect(rect)

        center = (x+w/2, y+h/2)

        # Get center diff
        xdiff = abs(center[0] - x)
        ydiff = abs(center[1]- y)
        
        xshift = xdiff * scale_factor
        yshift = ydiff * scale_factor
        
        width = 2*xshift
        height = 2*yshift

        # upper left
        new_x = x - abs(xdiff - xshift)
        new_y = y - abs(ydiff - yshift)

        # create contour
        contour = np.array([[[new_x,new_y]], [[new_x+width,new_y]], [[new_x+width,new_y+height]], [[new_x,new_y+height]]]) 
        rescaled_rects.append(contour)

    return rescaled_rects

def find_details(img, noise_removal_threshold=50, corners_threshold=0.01,
               room_closing_max_length=130, gap_in_wall_max_threshold=5000,
               gap_in_wall_min_threshold=10):

    """
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

    mask = image.remove_noise(img, noise_removal_threshold)
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