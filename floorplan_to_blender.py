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

for box in boxes:
    temp_verts = []
    counter_box_size = 0

    for pos in box:
        # add and convert all positions
        verts.append(pos[0], pos[1], 0)
        verts.append(pos[0], pos[1], wall_height)

        counter_curr += 1
        counter_box_size += 1

    # get correct position indexes
    for i in range(0, counter_box_size):
        temp_verts.append(counter_curr - i)

    faces.append(temp_verts)

edges = []

mesh = bpy.data.meshes.new(name=name)
mesh.from_pydata(verts, edges, faces)
# useful for development when the mesh may be invalid.
mesh.validate(verbose=True)
mesh.update()
object_data_add(context, mesh, operator=self)

ob = bpy.data.objects.new(name, mesh)
bpy.context.scene.objects.link(ob)
bpy.context.scene.update()
