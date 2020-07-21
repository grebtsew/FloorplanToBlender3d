import cv2
import numpy as np

from . import detect
from . import IO
from . import transform

'''
Generate
This file contains code for generate data files, used when creating blender project.
A temp storage of calculated data and a way to transfer data to the blender script.

FloorplanToBlender3d
Copyright (C) 2019 Daniel Westberg
'''
# TODO: create big window implementation (nicer windows!)
# TODO: write window and door detection and use the generators for them below!

# Paths to save folder
base_path = "Data/"
path = "Data/"

def generate_all_files(imgpath, info, position=None, rotation=None):
    '''
    Generate all data files
    @Param imgpath
    @Param info, boolean if should be printed
    @Param position, vector of float
    @Param rotation, vector of float
    @Return path to generated file, shape
    '''
    global path

    print(" ----- Generate ", imgpath, " at pos ", position ," rot ",rotation," -----")

    # Get path to save data
    path = IO.create_new_floorplan_path(base_path)

    shape = generate_floor_file(imgpath, info)
    new_shape = generate_walls_file(imgpath, info)
    shape = validate_shape(shape, new_shape)
    new_shape = generate_rooms_file(imgpath, info)
    shape = validate_shape(shape, new_shape)

    #verts, height = generate_big_windows_file(imgpath, info)
    #verts, height = generate_small_windows_file(imgpath, info)
    #verts, height = generate_doors_file(imgpath, info)

    transform = generate_transform_file(imgpath, info, position, rotation, shape)

    return path, shape

def validate_shape(old_shape, new_shape):
    '''
    Validate shape, use this to calculate a objects total shape
    @Param old_shape
    @Param new_shape
    @Return total shape
    '''
    shape = [0,0,0]
    shape[0] = max(old_shape[0], new_shape[0])
    shape[1] = max(old_shape[1], new_shape[1])
    shape[2] = max(old_shape[2], new_shape[2])
    return shape

def get_shape(verts, scale):
    '''
    Get shape
    Rescale boxes to specified scale
    @Param verts, input boxes
    @Param scale to use
    @Return rescaled boxes
    '''
    if len(verts) == 0:
        return [0,0,0]

    posList = transform.verts_to_poslist(verts)
    high = [0,0,0]
    low = posList[0]

    for pos in posList:
        if pos[0] > high[0]:
            high[0] = pos[0]
        if pos[1] > high[1]:
            high[1] = pos[1]
        if pos[2] > high[2]:
            high[2] = pos[2]
        if pos[0] < low[0]:
            low[0] = pos[0]
        if pos[1] < low[1]:
            low[1] = pos[1]
        if pos[2] < low[2]:
            low[2] = pos[2]

    return [high[0] - low[0],high[1] - low[1],high[2] - low[2]]

def generate_transform_file(imgpath, info, position, rotation, shape):
    '''
    Generate transform of file
    A transform contains information about an objects position, rotation.
    @Param imgpath
    @Param info, boolean if should be printed
    @Param position, position vector
    @Param rotation, rotation vector
    @Param shape
    @Return transform
    '''
    #create map
    transform = {}
    if position is None:
        transform["position"] = (0,0,0)
    else:
        transform["position"] = position

    if rotation is None:
        transform["rotation"] = (0,0,0)
    else:
        transform["rotation"] = rotation

    if shape is None:
        transform["shape"] = (0,0,0)
    else:
        transform["shape"] = shape

    IO.save_to_file(path+"transform", transform)

    return transform

def generate_rooms_file(img_path, info):
    '''
    Generate room data files
    @Param img_path path to image
    @Param info, boolean if should be printed
    @Return shape
    '''
    # Read floorplan image
    img = cv2.imread(img_path)

    # grayscale image
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # create verts (points 3d), points to use in mesh creations
    verts = []
    # create faces for each plane, describe order to create mesh points
    faces = []

    # Height of waLL
    height = 0.999

    # Scale pixel value to 3d pos
    scale = 100

    gray = detect.wall_filter(gray)

    gray = ~gray

    rooms, colored_rooms = detect.find_rooms(gray.copy())

    gray_rooms =  cv2.cvtColor(colored_rooms,cv2.COLOR_BGR2GRAY)

    # get box positions for rooms
    boxes, gray_rooms = detect.detectPreciseBoxes(gray_rooms, gray_rooms)

    #Create verts
    room_count = 0
    for box in boxes:
        verts.extend([transform.scale_point_to_vector(box, scale, height)])
        room_count+= 1

    # create faces
    for room in verts:
        count = 0
        temp = ()
        for pos in room:
            temp = temp + (count,)
            count += 1
        faces.append([(temp)])

    if(info):
        print("Number of rooms detected : ", room_count)

    IO.save_to_file(path+"rooms_verts", verts)
    IO.save_to_file(path+"rooms_faces", faces)

    return get_shape(verts, scale)

def generate_small_windows_file(img_path, info):
    '''
    Generate small windows data file
    @Param img_path, path to image
    @Param info, boolean if should be printed
    @Return shape
    '''
    # Read floorplan image
    img = cv2.imread(img_path)

    # grayscale image
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # create verts (points 3d), points to use in mesh creations
    verts = []
    # create faces for each plane, describe order to create mesh points
    faces = []

    # Height of waLL
    height = 1

    # Scale pixel value to 3d pos
    scale = 100

    gray = detect.wall_filter(gray)

    gray = ~gray

    rooms, colored_rooms = detect.find_details(gray.copy())

    gray_rooms =  cv2.cvtColor(colored_rooms,cv2.COLOR_BGR2GRAY)

    # get box positions for rooms
    boxes, gray_rooms = detect.detectPreciseBoxes(gray_rooms, gray_rooms)

    windows = []
    #do a split here, objects next to outside ground are windows, rest are doors or extra space

    for box in boxes:
        if(len(box) >= 4):
            x = box[0][0][0]
            x1 = box[2][0][0]
            y = box[0][0][1]
            y1 = box[2][0][1]

            if (abs(x-x1) > abs(y-y1)):
                windows.append([[[x,round((y+y1)/2)]],[[x1,round((y+y1)/2)]]])
            else:
                windows.append([[[round((x+x1)/2),y]],[[round((x+x1)/2),y1]]])

    '''
    Windows
    '''
    #Create verts for window
    v, faces, window_amount1 = transform.create_nx4_verts_and_faces(windows, height=0.25, scale=scale) # create low piece
    v2, faces, window_amount2 = transform.create_nx4_verts_and_faces(windows, height=1, scale=scale, ground= 0.75) # create heigher piece

    verts = v
    verts.extend(v2)
    window_amount = window_amount1 + window_amount2

    if(info):
        print("Windows created : ", window_amount)


    IO.save_to_file(path+"windows_verts", verts)
    IO.save_to_file(path+"windows_faces", faces)

    return get_shape(verts, scale)

def generate_doors_file(img_path, info):
    '''
    Generate door data file
    @Param img_path
    @Param info, boolean if should be print
    @Return shape
    '''
    # Read floorplan image
    img = cv2.imread(img_path)

    # grayscale image
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # create verts (points 3d), points to use in mesh creations
    verts = []
    # create faces for each plane, describe order to create mesh points
    faces = []

    # Height of waLL
    height = 1

    # Scale pixel value to 3d pos
    scale = 100

    gray = detect.wall_filter(gray)

    gray = ~gray

    rooms, colored_rooms = detect.find_details(gray.copy())

    gray_rooms =  cv2.cvtColor(colored_rooms,cv2.COLOR_BGR2GRAY)

    # get box positions for rooms
    boxes, gray_rooms = detect.detectPreciseBoxes(gray_rooms, gray_rooms)

    doors = []

    #do a split here, objects next to outside ground are windows, rest are doors or extra space
    for box in boxes:
        if shape_of_door(point):
            #change doors to actual 2 points instead of 4
            for x,y,x1,y1 in box:
                doors.append([round((x+x1)/2),round((y+y1)/2)])

    '''
    Doors
    '''
    #Create verts for door
    verts, faces, door_amount = transform.create_nx4_verts_and_faces(doors, height, scale)

    if(info):
        print("Doors created : ", door_amount)

    IO.save_to_file(path+"doors_verts", verts)
    IO.save_to_file(path+"doors_faces", faces)

    return get_shape(verts, scale)

def generate_floor_file(img_path, info):
    '''
    Generate floor data file
    @Param img_path, path to image
    @Param info, boolean if should be printed
    @Return shape
    '''
    # Read floorplan image
    img = cv2.imread(img_path)

    # grayscale image
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # detect outer Contours (simple floor or roof solution)
    contour, img = detect.detectOuterContours(gray)

    # create verts (points 3d), points to use in mesh creations
    verts = []
    # create faces for each plane, describe order to create mesh points
    faces = []

    # Height of waLL
    height = 1

    # Scale pixel value to 3d pos
    scale = 100

    #Create verts
    verts = transform.scale_point_to_vector(contour, scale, height)

    # create faces
    count = 0
    for box in verts:
        faces.extend([(count)])
        count += 1


    if(info):
        print("Approximated apartment size : ", cv2.contourArea(contour))

    IO.save_to_file(path+"floor_verts", verts)
    IO.save_to_file(path+"floor_faces", faces)

    return get_shape(verts, scale)

def generate_walls_file(img_path, info):
    '''
    Generate wall data file for floorplan
    @Param img_path, path to input file
    @Param info, boolean if data should be printed
    @Return shape
    '''
    # Read floorplan image
    img = cv2.imread(img_path)

    # grayscale image
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # create wall image (filter out small objects from image)
    wall_img = detect.wall_filter(gray)

    # detect walls
    boxes, img = detect.detectPreciseBoxes(wall_img)

    # create verts (points 3d), points to use in mesh creations
    verts = []
    # create faces for each plane, describe order to create mesh points
    faces = []

    # Height of waLL
    wall_height = 1

    # Scale pixel value to 3d pos
    scale = 100

    # Convert boxes to verts and faces
    verts, faces, wall_amount = transform.create_nx4_verts_and_faces(boxes, wall_height, scale)

    if(info):
        print("Walls created : ", wall_amount)

    # One solution to get data to blender is to write and read from file.
    IO.save_to_file(path+"wall_verts", verts)
    IO.save_to_file(path+"wall_faces", faces)

    return get_shape(verts, scale)
