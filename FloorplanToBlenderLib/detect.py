import cv2
import numpy as np
from . import image
from . import const
from . import image
from . import calculate
from . import transform
import math

# Calculate (actual) size of apartment

"""
Detect
This file contains functions used when detecting and calculating shapes in images.

FloorplanToBlender3d
Copyright (C) 2022 Daniel Westberg
"""


def wall_filter(gray):
    """
    Filter walls
    Filter out walls from a grayscale image
    @Param image
    @Return image of walls
    """
    _, thresh = cv2.threshold(
        gray,
        const.WALL_FILTER_TRESHOLD[0],
        const.WALL_FILTER_TRESHOLD[1],
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU,
    )

    # noise removal
    kernel = np.ones(const.WALL_FILTER_KERNEL_SIZE, np.uint8)
    opening = cv2.morphologyEx(
        thresh,
        cv2.MORPH_OPEN,
        kernel,
        iterations=const.WALL_FILTER_MORPHOLOGY_ITERATIONS,
    )

    sure_bg = cv2.dilate(
        opening, kernel, iterations=const.WALL_FILTER_DILATE_ITERATIONS
    )

    dist_transform = cv2.distanceTransform(
        opening, cv2.DIST_L2, const.WALL_FILTER_DISTANCE
    )
    ret, sure_fg = cv2.threshold(
        const.WALL_FILTER_DISTANCE_THRESHOLD[0] * dist_transform,
        const.WALL_FILTER_DISTANCE_THRESHOLD[1] * dist_transform.max(),
        const.WALL_FILTER_MAX_VALUE,
        const.WALL_FILTER_THRESHOLD_TECHNIQUE,
    )

    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)

    return unknown


def precise_boxes(detect_img, output_img=None, color=[100, 100, 0]):
    """
    Detect corners with boxes in image with high precision
    @Param detect_img image to detect from @mandatory
    @Param output_img image for output
    @Param color to set on output
    @Return corners(list of boxes), output image
    @source https://stackoverflow.com/questions/50930033/drawing-lines-and-distance-to-them-on-image-opencv-python
    """
    res = []

    contours, _ = cv2.findContours(
        detect_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    for cnt in contours:
        epsilon = const.PRECISE_BOXES_ACCURACY * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)
        if output_img is not None:
            output_img = cv2.drawContours(output_img, [approx], 0, color)
        res.append(approx)

    return res, output_img


def __corners_and_draw_lines(img, corners_threshold, room_closing_max_length):
    """
    Finds corners and draw lines from them
    Help function for finding room
    @Param image input image
    @Param corners_threshold threshold for corner distance
    @Param room_closing_max_length threshold for room max size
    @Return output image
    """
    # Detect corners (you can play with the parameters here)
    kernel = np.ones(const.PRECISE_HARRIS_KERNEL_SIZE, np.uint8)

    dst = cv2.cornerHarris(
        img,
        const.PRECISE_HARRIS_BLOCK_SIZE,
        const.PRECISE_HARRIS_KSIZE,
        const.PRECISE_HARRIS_K,
    )
    dst = cv2.erode(dst, kernel, iterations=const.PRECISE_ERODE_ITERATIONS)
    corners = dst > corners_threshold * dst.max()

    # Draw lines to close the rooms off by adding a line between corners on the same x or y coordinate
    # This gets some false positives.
    # You could try to disallow drawing through other existing lines for example.
    for y, row in enumerate(corners):
        x_same_y = np.argwhere(row)
        for x1, x2 in zip(x_same_y[:-1], x_same_y[1:]):

            if x2[0] - x1[0] < room_closing_max_length:
                color = 0
                cv2.line(img, (x1[0], y), (x2[0], y), color, 1)

    for x, col in enumerate(corners.T):
        y_same_x = np.argwhere(col)
        for y1, y2 in zip(y_same_x[:-1], y_same_x[1:]):
            if y2[0] - y1[0] < room_closing_max_length:
                color = 0
                cv2.line(img, (x, y1[0]), (x, y2[0]), color, 1)
    return img


def find_rooms(
    img,
    noise_removal_threshold=const.FIND_ROOMS_NOISE_REMOVAL_THRESHOLD,
    corners_threshold=const.FIND_ROOMS_CORNERS_THRESHOLD,
    room_closing_max_length=const.FIND_ROOMS_CLOSING_MAX_LENGTH,
    gap_in_wall_min_threshold=const.FIND_ROOMS_GAP_IN_WALL_MIN_THRESHOLD,
):
    """
    src: https://stackoverflow.com/questions/54274610/crop-each-of-them-using-opencv-python

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

    __corners_and_draw_lines(img, corners_threshold, room_closing_max_length)

    img, mask = image.mark_outside_black(img, mask)

    # Find the connected components in the house
    ret, labels = cv2.connectedComponents(img)
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    unique = np.unique(labels)
    rooms = []
    for label in unique:
        component = labels == label
        if (
            img[component].sum() == 0
            or np.count_nonzero(component) < gap_in_wall_min_threshold
        ):
            color = 0
        else:
            rooms.append(component)
            color = np.random.randint(0, 255, size=3)
        img[component] = color
    return rooms, img


def and_remove_precise_boxes(detect_img, output_img=None, color=[255, 255, 255]):
    """
    Currently not used in the main implementation
    Remove contours of detected walls from image
    @Param detect_img image to detect from @mandatory
    @Param output_img image for output
    @Param color to set on output
    @Return list of boxes, actual image
    @source https://stackoverflow.com/questions/50930033/drawing-lines-and-distance-to-them-on-image-opencv-python
    """
    res = []
    contours, hierarchy = cv2.findContours(
        detect_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    for cnt in contours:

        epsilon = const.REMOVE_PRECISE_BOXES_ACCURACY * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)
        if output_img is not None:
            output_img = cv2.drawContours(output_img, [approx], -1, color, -1)
        res.append(approx)

    return res, output_img


def outer_contours(detect_img, output_img=None, color=[255, 255, 255]):
    """
    Get the outer side of floorplan, used to get ground
    @Param detect_img image to detect from @mandatory
    @Param output_img image for output
    @Param color to set on output
    @Return approx, box
    @Source https://stackoverflow.com/questions/50930033/drawing-lines-and-distance-to-them-on-image-opencv-python
    """
    ret, thresh = cv2.threshold(
        detect_img,
        const.OUTER_CONTOURS_TRESHOLD[0],
        const.OUTER_CONTOURS_TRESHOLD[1],
        cv2.THRESH_BINARY_INV,
    )

    contours, hierarchy = cv2.findContours(
        thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    largest_contour_area = 0
    for cnt in contours:
        if cv2.contourArea(cnt) > largest_contour_area:
            largest_contour_area = cv2.contourArea(cnt)
            largest_contour = cnt

    epsilon = const.PRECISE_BOXES_ACCURACY * cv2.arcLength(largest_contour, True)
    approx = cv2.approxPolyDP(largest_contour, epsilon, True)
    if output_img is not None:
        output_img = cv2.drawContours(output_img, [approx], 0, color)
    return approx, output_img


def doors(image_path, scale_factor):
    model = cv2.imread(const.DOOR_MODEL, 0)
    img = cv2.imread(
        image_path, 0
    )  # TODO: it is not very effective to read image again here!

    img = image.cv2_rescale_image(img, scale_factor)
    _, doors = feature_match(img, model)
    return doors


def windows(image_path, scale_factor):
    model = cv2.imread(const.DOOR_MODEL, 0)
    img = cv2.imread(
        image_path, 0
    )  # TODO: it is not very effective to read image again here!

    img = image.cv2_rescale_image(img, scale_factor)
    windows, _ = feature_match(img, model)
    return windows


def feature_match(img1, img2):
    """
    Feature match models to floorplans in order to distinguish doors from windows.
    Also calculate where doors should exist.
    Compares result with detailed boxes and filter depending on colored pixels to deviate windows, doors and unknowns.
    """
    cap = img1
    model = img2
    # ORB keypoint detector
    orb = cv2.ORB_create(
        nfeatures=const.WINDOWS_AND_DOORS_FEATURE_N, scoreType=cv2.ORB_FAST_SCORE
    )
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

    # --- calculate bounds ---

    # these are important for group matching!
    min_x = math.inf
    min_y = math.inf
    max_x = 0
    max_y = 0

    for mat in matches:
        # Get the matching keypoints for each of the images
        img1_idx = mat.queryIdx

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

    # --- Create a list of objects containing matches group on nearby matches ---

    for mat in matches:
        # Get the matching keypoints for each of the images
        img1_idx = mat.queryIdx
        img2_idx = mat.trainIdx

        # Get the coordinates
        # x - columns
        # y - rows
        (x1, y1) = kp_model[img1_idx].pt
        (x2, y2) = kp_frame[img2_idx].pt
        i = 0
        found = False

        for existing_match in list_grouped_matches:
            if (
                abs(existing_match[0][1][0] - x2) < w
                and abs(existing_match[0][1][1] - y2) < h
            ):
                # add to group
                list_grouped_matches[i].append(((int(x1), int(y1)), (int(x2), int(y2))))
                found = True
                break
            # increment
            i += 1

        if not found:
            tmp = list()
            tmp.append(((int(x1), int(y1)), (int(x2), int(y2))))
            list_grouped_matches.append(list(list(list(tmp))))

    # Remove groups with only singles because we cant calculate rotation then!
    list_grouped_matches_filtered = []
    for match_group in list_grouped_matches:
        if len(match_group) >= const.WINDOWS_AND_DOORS_MAX_CORNERS:
            list_grouped_matches_filtered.append(match_group)

    # find corners of door in model image
    corners = cv2.goodFeaturesToTrack(
        model,
        const.WINDOWS_AND_DOORS_FEATURE_TRACK_MAX_CORNERS,
        const.WINDOWS_AND_DOORS_FEATURE_TRACK_QUALITY,
        const.WINDOWS_AND_DOORS_FEATURE_TRACK_MIN_DIST,
    )
    corners = np.int0(corners)

    # This is still a little hardcoded but still better than before!
    upper_left = corners[1][0]
    upper_right = corners[0][0]
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

    origin = (int((max_x + min_x) / 2), int((min_y + max_y) / 2))

    list_of_proper_transformed_doors = []

    # Calculate position and rotation of doors
    for match in list_grouped_matches_filtered:

        # calculate offsets from points
        index1, index2 = calculate.best_matches_with_modulus_angle(match)

        pos1_model = match[index1][0]
        pos2_model = match[index2][0]

        # calculate actual position from offsets with rotation!
        pos1_cap = match[index1][1]
        pos2_cap = match[index2][1]

        pt1 = (pos1_model[0] - pos2_model[0], pos1_model[1] - pos2_model[1])
        pt2 = (pos1_cap[0] - pos2_cap[0], pos1_cap[1] - pos2_cap[1])

        ang = math.degrees(calculate.angle_between_vectors_2d(pt1, pt2))

        # rotate door
        new_upper_left = transform.rotate_round_origin_vector_2d(
            origin, upper_left, math.radians(ang)
        )
        new_upper_right = transform.rotate_round_origin_vector_2d(
            origin, upper_right, math.radians(ang)
        )
        new_down = transform.rotate_round_origin_vector_2d(
            origin, down, math.radians(ang)
        )
        new_pos1_model = transform.rotate_round_origin_vector_2d(
            origin, pos1_model, math.radians(ang)
        )

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

        offset = (
            scaled_pos1_model[0] - pos1_model[0],
            scaled_pos1_model[1] - pos1_model[1],
        )

        # calculate dist!
        move_dist = (pos1_cap[0] - pos1_model[0], pos1_cap[1] - pos1_model[1])

        # draw corners!
        moved_new_upper_left = (
            int(scaled_upper_left[0] + move_dist[0] - offset[0]),
            int(scaled_upper_left[1] + move_dist[1] - offset[1]),
        )
        moved_new_upper_right = (
            int(scaled_upper_right[0] + move_dist[0] - offset[0]),
            int(scaled_upper_right[1] + move_dist[1] - offset[1]),
        )
        moved_new_down = (
            int(scaled_down[0] + move_dist[0] - offset[0]),
            int(scaled_down[1] + move_dist[1] - offset[1]),
        )

        list_of_proper_transformed_doors.append(
            [moved_new_upper_left, moved_new_upper_right, moved_new_down]
        )

    gray = wall_filter(img1)
    gray = ~gray  # TODO: is it necessary to convert to grayscale again?
    rooms, colored_rooms = find_rooms(gray.copy())
    doors, colored_doors = find_details(gray.copy())
    gray_rooms = cv2.cvtColor(colored_doors, cv2.COLOR_BGR2GRAY)

    # get box positions for rooms
    boxes, gray_rooms = precise_boxes(gray_rooms)

    windows = []
    doors = []
    # classify boxes
    # window, door, none
    for box in boxes:

        # is a door inside box?
        is_door = False
        _door = []
        for door in list_of_proper_transformed_doors:

            if calculate.points_are_inside_or_close_to_box(
                door, box
            ):  # TODO: match door with only one box, the closest one!
                is_door = True
                _door = door
                break

        if is_door:
            doors.append((_door, box))
            continue

        # is window?
        x, y, w, h = cv2.boundingRect(box)
        cropped = img1[y : y + h, x : x + w]
        # bandpassfilter
        total = np.sum(cropped)
        colored = np.sum(cropped > 0)
        low = const.WINDOWS_COLORED_PIXELS_THRESHOLD[0]
        high = const.WINDOWS_COLORED_PIXELS_THRESHOLD[1]

        amount_of_colored = colored / total

        if low < amount_of_colored < high:
            windows.append(box)

    return transform.rescale_rect(windows, const.WINDOWS_RESCALE_TO_FIT), doors


def find_details(
    img,
    noise_removal_threshold=const.DETAILS_NOISE_REMOVAL_THRESHOLD,
    corners_threshold=const.DETAILS_CORNERS_THRESHOLD,
    room_closing_max_length=const.DETAILS_CLOSING_MAX_LENGTH,
    gap_in_wall_max_threshold=const.DETAILS_GAP_IN_WALL_THRESHOLD[1],
    gap_in_wall_min_threshold=const.DETAILS_GAP_IN_WALL_THRESHOLD[0],
):

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

    __corners_and_draw_lines(img, corners_threshold, room_closing_max_length)

    img, mask = image.mark_outside_black(img, mask)

    # Find the connected components in the house
    ret, labels = cv2.connectedComponents(img)
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    unique = np.unique(labels)
    details = []
    for label in unique:
        component = labels == label
        if (
            img[component].sum() == 0
            or np.count_nonzero(component) < gap_in_wall_min_threshold
            or np.count_nonzero(component) > gap_in_wall_max_threshold
        ):
            color = 0
        else:
            details.append(component)
            color = np.random.randint(0, 255, size=3)

        img[component] = color

    return details, img
