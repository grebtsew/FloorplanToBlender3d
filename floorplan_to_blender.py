import bpy

'''
Floorplan to Blender

This file contains code to convert a floorplan to blender objects.
'''

from Drawing_To_Array import drawing_to_array as floorplan

import cv2
import numpy as np

'''
Receive image, convert
'''
# Read floorplan image
img = cv2.imread("Drawing_To_Array/example2.png")

# grayscale image
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

'''
Detect objects in image
'''
# create wall image (filter out small objects from image)
wall_img = floorplan.wall_filter(gray)

# detect walls
boxes, img = floorplan.detectPreciseBoxes(wall_img)

# detect outer Contours (simple floor or roof solution)
contour, img = floorplan.detectOuterContours(gray)

# TODO:
# detect doors
# detect windows
# detect other objects (such as fridge, dishwasher, closets)

'''
Create 3d object for blender
'''

# create verts (points 3d)
verts = []
# create faces for each plane
faces = []

wall_height = 1

# Convert 2d poses to 3d poses and boxes

counter_curr = 0
counter_box_size= 0

# for each wall group
for box in boxes:
    temp_verts = []
    counter_box_size = 0

    # for each pos
    for pos in box:
        # add and convert all positions
        verts.extend([(pos[0], pos[1], 0.0)])
        verts.extend([(pos[0], pos[1], wall_height)])

        counter_curr += 1
        counter_box_size += 1

    # get correct position indexes
    for i in range(0, counter_box_size):
        temp_verts.extend([(counter_curr - i)])

    faces.append(temp_verts)

    #create_custom_mesh("Wall"+counter_curr, [0,0,0], verts, faces)




def create_custom_mesh(objname, pos, vertex, faces):
    '''
    @Param objname, name of new meshe
    @Param pos, object position [x, y, z]
    @Param vertex, corners
    @Param buildorder
    '''

    mymesh = bpy.data.meshes.new(objname)

    myobject = bpy.data.objects.new(objname, mymesh)

    bpy.context.scene.objects.link(myobject)

    # Generate mesh data
    mymesh.from_pydata(vertex, [], faces)
    # Calculate the edges
    mymesh.update(calc_edges=True)

    # Set Location
    myobject.location.x = pos[0]
    myobject.location.y = pos[1]
    myobject.location.z = pos[2]

    return myobject
