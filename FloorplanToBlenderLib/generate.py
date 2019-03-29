import cv2
import numpy as np

from . import detect
from . import IO
from . import transform

# Path
path = "Data/"

def generate_all_files(imgpath):
    '''
    Generate all data files
    '''

    generate_floor_file(imgpath)
    generate_walls_file(imgpath)


def generate_rooms_file(img_path):
    # TODO: generate rooms
    pass

def generate_details_file(img_path):
    # TODO: generate doors
    # TODO: generate windows
    pass

def generate_floor_file(img_path):
    '''
    Receive image, convert
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

    IO.save_to_file(path+"floor_verts", verts)
    IO.save_to_file(path+"floor_faces", faces)

def generate_walls_file(img_path):
    '''
    generate wall data file for floorplan
    @Param img_path, path to input file
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

    # One solution to get data to blender is to write and read from file.
    IO.save_to_file(path+"wall_verts", verts)
    IO.save_to_file(path+"wall_faces", faces)
