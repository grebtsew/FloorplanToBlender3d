import bpy
import numpy as np
import json
import sys
import math

'''
Floorplan to Blender

FloorplanToBlender3d
Copyright (C) 2019 Daniel Westberg

This code read data from a file and creates a 3d model of that data.
RUN THIS CODE FROM BLENDER

The new implementation starts blender and executes this script in a new project
so tutorial below can be ignored if you don't want to do this manually in blender.

HOW TO: (old style)

1. Run create script to create data files for your floorplan image.
2. Edit path in this file to generated data files.
3. Start blender
4. Open Blender text editor
5. Open this file "alt+o"
6. Run script

This code is tested on Windows 10, Blender 2.79, in January 2019.
'''

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

def create_custom_mesh(objname, verts, faces, pos = None, rot = None, mat = None):
    '''
    @Param objname, name of new mesh
    @Param pos, object position [x, y, z]
    @Param vertex, corners
    @Param faces, buildorder
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

    if rot is not None:
        myobject.rotation_euler = rot

    # rotate to fix mirrored floorplan
    myobject.rotation_euler = (0, math.pi, 0)

    # add material
    if mat is None: # add random color
        myobject.data.materials.append(create_mat( np.random.randint(0, 40, size=3))) #add the material to the object
    else:
        myobject.data.materials.append(mat) #add the material to the object
    return myobject

def create_mat(rgb_color):
    mat = bpy.data.materials.new(name="MaterialName") #set new material to variable
    mat.diffuse_color = rgb_color #change to random color
    return mat

'''
Main functionallity here!
'''
def main(argv):
    '''
    Create Walls
    All walls are square
    Therefore we split data into two files
    '''

    if(len(argv) > 5): # Note YOU need 6 arguments!
        program_path = argv[4]

    else:
        exit(0)

    '''
    Instantiate
    '''
    for i in range(5,len(argv)):
        base_path = argv[i]
        create_floorplan(base_path, program_path, i)

    '''
    Save to file
    '''
    bpy.ops.wm.save_as_mainfile(filepath=program_path + "\\floorplan.blend")

    '''
    Send correct exit code
    '''
    exit(0)


def create_floorplan(base_path,program_path, name=0):

    parent, parent_mesh = init_object("Floorplan"+str(name))

    base_path = base_path.replace('/','\\')

    path_to_wall_faces_file = program_path +"\\" + base_path + "wall_faces"
    path_to_wall_verts_file = program_path +"\\" + base_path + "wall_verts"

    path_to_floor_faces_file = program_path +"\\" +base_path + "floor_faces"
    path_to_floor_verts_file = program_path +"\\" +base_path + "floor_verts"

    path_to_rooms_faces_file = program_path +"\\" + base_path + "rooms_faces"
    path_to_rooms_verts_file = program_path +"\\" + base_path + "rooms_verts"

#    path_to_windows_faces_file = program_path +"\\" + base_path + "windows_faces"
#    path_to_windows_verts_file = program_path +"\\" + base_path + "windows_verts"

    path_to_transform_file = program_path+"\\" + base_path + "transform"

    '''
    Get transform
    '''
    # read from file
    transform = read_from_file(path_to_transform_file)

    rot = transform["rotation"]
    pos = transform["position"]

    '''
    Create Walls
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

            obj = create_custom_mesh(boxname + wallname, wall, faces, pos=pos, rot=rot)
            obj.parent = wall_parent

            wallcount += 1
        boxcount += 1

    wall_parent.parent = parent

    '''
    Create windows
    '''
    '''
    # get image wall data
    verts = read_from_file(path_to_windows_verts_file)
    faces = read_from_file(path_to_windows_faces_file)

    # Create mesh from data
    boxcount = 0
    windowcount = 0

    # Create parent
    window_parent, window_parent_mesh = init_object("Windows")

    for window in verts:
        windowname = "Window"+str(windowcount)

        obj = create_custom_mesh(windowname, window[0], faces, pos=pos, rot=rot)
        obj.parent = window_parent

        windowcount += 1

    window_parent.parent = parent
    '''

    '''
    Create Floor
    '''
    # get image wall data
    verts = read_from_file(path_to_floor_verts_file)
    faces = read_from_file(path_to_floor_faces_file)

    # Create mesh from data
    cornername="Floor"
    obj = create_custom_mesh(cornername, verts, [faces], mat=create_mat((40,1,1)))
    obj.parent = parent

    '''
    Create rooms
    '''
    # get image wall data
    verts = read_from_file(path_to_rooms_verts_file)
    faces = read_from_file(path_to_rooms_faces_file)

    # Create parent
    room_parent, room_parent_mesh = init_object("Rooms")

    for i in range(0,len(verts)):
        roomname="Room"+str(i)
        obj = create_custom_mesh(roomname, verts[i], faces[i], pos=pos, rot=rot)
        obj.parent = room_parent

    room_parent.parent = parent

# Start
if __name__ == "__main__":
    main(sys.argv)

    '''
    TODO:
    Create door
    Create window
    Create details
    '''
