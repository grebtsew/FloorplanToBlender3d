import bpy
import numpy as np
import json



'''
Floorplan to Blender

This code read data from a file and creates a 3d model of that data.
RUN THIS CODE FROM BLENDER

HOW TO: (old style)

1. Run create script to create data files for your floorplan image.
2. Edit path in this file to generated data files.
3. Start blender
4. Open Blender text editor
5. Open this file "alt+o"
6. Run script

This code is tested on Windows 10, Blender 2.79, in January 2019.
'''

# Edit these paths to your destination
path_to_wall_faces_file = "C:\\Users\\Daniel\\Documents\\GitHub\\ApartmentDrawing-To-Blender\\Data\\wall_faces"
path_to_wall_verts_file = "C:\\Users\\Daniel\\Documents\\GitHub\\ApartmentDrawing-To-Blender\\Data\\wall_verts"

path_to_floor_faces_file = "C:\\Users\\Daniel\\Documents\\GitHub\\ApartmentDrawing-To-Blender\\Data\\floor_faces"
path_to_floor_verts_file = "C:\\Users\\Daniel\\Documents\\GitHub\\ApartmentDrawing-To-Blender\\Data\\floor_verts"

'''
Our helpful functions
'''

def read_from_file(file_path):
    '''
    Read from file
    read verts data from file
    @Param file_path, path to file
    @Return data
    '''
    #Now read the file back into a Python list object
    with open(file_path+'.txt', 'r') as f:
        data = json.loads(f.read())
    return data

def init_object(name):
    mymesh = bpy.data.meshes.new(name)
    myobject = bpy.data.objects.new(name, mymesh)
    bpy.context.scene.objects.link(myobject)
    return myobject, mymesh

def create_custom_mesh(objname, verts, faces, pos = None):
    '''
    @Param objname, name of new mesh
    @Param pos, object position [x, y, z]
    @Param vertex, corners
    @Param buildorder
    '''
    # Create mesh and object
    myobject, mymesh = init_object(objname)

    # Generate mesh data
    mymesh.from_pydata(verts, [], faces)
    # Calculate the edges
    mymesh.update(calc_edges=True)

    # Set Location
    if pos is not None:
        myobject.location.x = pos[0]
        myobject.location.y = pos[1]
        myobject.location.z = pos[2]

    return myobject


'''
Main functionallity here!
'''

'''
Create Walls
All walls are square
Therefore we split data into two files
'''
# get image wall data
verts = read_from_file(path_to_wall_verts_file)
faces = read_from_file(path_to_wall_faces_file)

# Create mesh from data
boxcount = 0
wallcount = 0

# Create parent
wall_parent, wall_parent_mesh = init_object("Walls")

for box in verts:
    boxname="Box"+str(boxcount)
    for wall in box:
        wallname = "Wall"+str(wallcount)

        obj = create_custom_mesh(boxname + wallname, wall, faces)
        obj.parent = wall_parent

        wallcount += 1
    boxcount += 1

'''
Create Floor
'''
# get image wall data
verts = read_from_file(path_to_floor_verts_file)
faces = read_from_file(path_to_floor_faces_file)

# Create mesh from data
cornername="Floor"
create_custom_mesh(cornername, verts, [faces])


'''
Save to file
'''
bpy.ops.wm.save_as_mainfile(filepath="C:\\Users\\Daniel\\Documents\\GitHub\\ApartmentDrawing-To-Blender\\floorplan.blend")


'''
TODO:
# TODO: create materials
Create door
Create windows
Create rooms by splitting the floor
Create details
'''
