import cv2
import numpy as np
import sys
import os
import math

"""
Testing core functions from library
"""

floorplan_lib_path = os.path.dirname(os.path.realpath(__file__)) + "/../../"
example_image_path = (
    os.path.dirname(os.path.realpath(__file__)) + "/../../Images/Examples/example.png"
)


sys.path.insert(0, floorplan_lib_path)
from FloorplanToBlenderLib import *  # floorplan to blender lib
from subprocess import check_output

"""
Find rooms in image
"""


def detect_windows_and_doors_boxes(img, door_list):

    height, width, channel = img.shape
    blank_image = np.zeros(
        (height, width, 3), np.uint8
    )  # output image same size as original

    # grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = detect.wall_filter(gray)
    gray = ~gray
    rooms, colored_rooms = detect.find_rooms(gray.copy())
    doors, colored_doors = detect.find_details(gray.copy())
    gray_rooms = cv2.cvtColor(colored_doors, cv2.COLOR_BGR2GRAY)

    # get box positions for rooms
    boxes, gray_rooms = detect.precise_boxes(gray_rooms, blank_image)

    cv2.imshow("input", img)
    cv2.imshow("doors and windows", gray_rooms)
    cv2.imshow("colored", colored_doors)
    cv2.waitKey(0)

    classified_boxes = []
    # classify boxes
    # window, door, none
    for box in boxes:
        obj = dict()
        obj["type"] = "none"

        # is a door inside box?
        isDoor = False
        for door in door_list:

            if points_are_inside_or_close_to_box(door, box):
                obj["type"] = "door"
                obj["box"] = box
                obj["features"] = door
                isDoor = True
                break

        if isDoor:
            classified_boxes.append(obj)
            continue

        # is window?
        x, y, w, h = cv2.boundingRect(box)
        cropped = img[y : y + h, x : x + w]
        # bandpassfilter
        total = np.sum(cropped)
        colored = np.sum(cropped > 0)
        low = 0.001
        high = 0.00459

        amount_of_colored = colored / total

        if low < amount_of_colored < high:
            obj["type"] = "window"
            obj["box"] = box
            classified_boxes.append(obj)

        # is nothing at all

    for box in classified_boxes:

        if box["type"] == "door":
            img = cv2.line(img, box["features"][1], box["features"][2], (0, 0, 255), 5)

        elif box["type"] == "window":
            x, y, w, h = cv2.boundingRect(box["box"])

            start = (x, y)
            end = (x + w, y + h)
            img = cv2.line(img, start, end, (0, 255, 0), 5)

    cv2.imshow("Final result", img)
    cv2.waitKey(0)


def points_are_inside_or_close_to_box(door, box):

    for point in door:
        if rectContainsOrAlmostContains(point, box):
            return True
            break


def rectContainsOrAlmostContains(pt, box):

    x, y, w, h = cv2.boundingRect(box)
    isInside = x < pt[0] < x + w and y < pt[1] < y + h

    almostInside = False

    min_dist = 0
    if w < h:
        min_dist = w
    else:
        min_dist = h

    for point in box:
        dist = abs(point[0][0] - pt[0]) + abs(point[0][1] - pt[1])
        if dist <= min_dist:
            almostInside = True
            break

    return isInside or almostInside


def scale_model_point_to_origin(origin, point, x_scale, y_scale):
    dx, dy = (point[0] - origin[0], point[1] - origin[1])
    return (dx * x_scale, dy * y_scale)


def feature_detect(img):
    """
    Find features in image
    """

    # Initiate ORB detector
    orb = cv2.ORB_create(nfeatures=10000000, scoreType=cv2.ORB_FAST_SCORE)

    # find the keypoints with ORB
    kp = orb.detect(img, None)

    # compute the descriptors with ORB
    kp, des = orb.compute(img, kp)

    # draw only keypoints location,not size and orientation
    img2 = cv2.drawKeypoints(img, kp, img, color=(0, 255, 0), flags=0)
    cv2.imshow("keypoints", img2)
    cv2.waitKey(0)


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
        if len(match_group) >= 4:
            list_grouped_matches_filtered.append(match_group)

    # print(list_grouped_matches_filtered, len(list_grouped_matches_filtered))

    # find corners of door in model image
    corners = cv2.goodFeaturesToTrack(model, 3, 0.01, 20)
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

        pt1 = (pos1_model[0] - pos2_model[0], pos1_model[1] - pos2_model[1])
        pt2 = (pos1_cap[0] - pos2_cap[0], pos1_cap[1] - pos2_cap[1])

        ang = math.degrees(angle(pt1, pt2))
        # print(index1, index2, ang)

        # print("Angle between doors ", ang)

        # rotate door
        new_upper_left = rotate(origin, upper_left, math.radians(ang))
        new_upper_right = rotate(origin, upper_right, math.radians(ang))
        new_down = rotate(origin, down, math.radians(ang))

        new_pos1_model = rotate(origin, pos1_model, math.radians(ang))

        # calculate scale, and rescale model
        """
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

        img = cv2.circle(
            cap, moved_new_upper_left, radius=4, color=(0, 0, 0), thickness=5
        )
        img = cv2.circle(
            cap, moved_new_upper_right, radius=4, color=(0, 0, 0), thickness=5
        )
        img = cv2.circle(cap, moved_new_down, radius=4, color=(0, 0, 0), thickness=5)

        list_of_proper_transformed_doors.append(
            [moved_new_upper_left, moved_new_upper_right, moved_new_down]
        )

    # draw door points
    for match in list_grouped_matches_filtered:

        img = cv2.circle(
            cap,
            (match[0][1][0], match[0][1][1]),
            radius=4,
            color=(0, 0, 0),
            thickness=5,
        )

    # Draw matches as lines
    if len(matches) > MIN_MATCHES:

        # draw first 15 matches.
        cap = cv2.drawMatches(
            model, kp_model, cap, kp_frame, matches[:MIN_MATCHES], 0, flags=2
        )
        # show result
        cv2.imshow("frame", cap)
        cv2.waitKey(0)

    else:
        print(
            "Not enough matches have been found - %d/%d" % (len(matches), MIN_MATCHES)
        )

    return list_of_proper_transformed_doors


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


def angle(vector1, vector2):
    x1, y1 = vector1
    x2, y2 = vector2
    inner_product = x1 * x2 + y1 * y2
    len1 = math.hypot(x1, y1)
    len2 = math.hypot(x2, y2)
    return math.acos(inner_product / (len1 * len2))


def average(lst):
    return sum(lst) / len(lst)


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

            pt1 = (pos1_model[0] - pos2_model[0], pos1_model[1] - pos2_model[1])
            pt2 = (pos1_cap[0] - pos2_cap[0], pos1_cap[1] - pos2_cap[1])

            if pt1 == pt2 or pt1 == (0, 0) or pt2 == (0, 0):
                continue

            ang = math.degrees(angle(pt1, pt2))
            diff = ang % 30

            if diff < best:
                best = diff
                index1 = i
                index2 = j

            j += 1
        i += 1
    return index1, index2


"""
We are not allowed to use SURF or SIFT due to licenses in latest OpenCV.
They are Patented!

Therefore the developers created ORB. And it seems to be working fine!
"""

if __name__ == "__main__":
    door_image_path = (
        os.path.dirname(os.path.realpath(__file__))
        + "/../../Images/Models/Doors/door.png"
    )
    example_image_path = (
        os.path.dirname(os.path.realpath(__file__))
        + "/../../Images/Examples/example.png"
    )

    img0 = cv2.imread(example_image_path)
    img1 = cv2.imread(example_image_path, 0)
    img2 = cv2.imread(door_image_path, 0)

    detect_windows_and_doors_boxes(img0, feature_match(img1, img2))
