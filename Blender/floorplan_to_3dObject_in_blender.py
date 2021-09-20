import bpy
import numpy as np
import json
import sys
import math

'''
Floorplan to Blender

FloorplanToBlender3d
Copyright (C) 2021 Daniel Westberg

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
    # Create new blender object and return references to mesh and object
    mymesh = bpy.data.meshes.new(name)
    myobject = bpy.data.objects.new(name, mymesh)
    bpy.context.collection.objects.link(myobject)
    return myobject, mymesh

def average(lst): 
    return sum(lst) / len(lst) 

def get_mesh_center(verts):
    # Calculate center location of a mesh from verts
    x=[]
    y=[]
    z=[]

    for vert in verts:
        x.append(vert[0])
        y.append(vert[1])
        z.append(vert[2])

    return [average(x), average(y), average(z)]

def subtract_center_verts(verts1, verts2):
    # Remove verts1 from all verts in verts2, return result, verts1 & verts2 must have same shape!
    for i in range(0, len(verts2)):
        verts2[i][0] -= verts1[0]
        verts2[i][1] -= verts1[1]
        verts2[i][2] -= verts1[2]
    return verts2

def create_custom_mesh(objname, verts, faces, pos = None, rot = None, mat = None, cen = None):
    '''
    @Param objname, name of new mesh
    @Param pos, object position [x, y, z]
    @Param vertex, corners
    @Param faces, buildorder
    '''
    # Create mesh and object
    myobject, mymesh = init_object(objname)

    # Rearrange verts to put pivot point in center of mesh
    # Find center of verts
    center = get_mesh_center(verts)
    # Subtract center from verts before creation
    proper_verts = subtract_center_verts(center,verts)

    # Generate mesh data
    mymesh.from_pydata(proper_verts, [], faces)
    # Calculate the edges
    mymesh.update(calc_edges=True)

    parent_center = [0,0,0]
    if cen is not None:
        parent_center = [int(cen[0]/2),int(cen[1]/2),int(cen[2])]

    # Move object to input verts location
    myobject.location.x = center[0] - parent_center[0]
    myobject.location.y = center[1] - parent_center[1]
    myobject.location.z = center[2] - parent_center[2]

    # Move to Custom Location
    if pos is not None:
        myobject.location.x += pos[0]
        myobject.location.y += pos[1]
        myobject.location.z += pos[2]

    if rot is not None:
        myobject.rotation_euler = rot

    # add contraint for pivot point
    #pivot = myobject.constraints.new(type='PIVOT')
    
    # add material
    if mat is None: # add random color
        myobject.data.materials.append(create_mat( np.random.randint(0, 40, size=4))) #add the material to the object
    else:
        myobject.data.materials.append(mat) #add the material to the object
    return myobject

def create_mat(rgb_color):
    mat = bpy.data.materials.new(name="MaterialName") #set new material to variable
    mat.diffuse_color = rgb_color #change to random color
    return mat

'''
Main functionality here!
'''
def main(argv):
    '''
    Create Walls
    All walls are square
    Therefore we split data into two files
    '''

    # Remove starting object cube
    # Select all
    objs = bpy.data.objects
    objs.remove(objs["Cube"], do_unlink=True)

    if(len(argv) > 7): # Note YOU need 8 arguments!
        program_path = argv[5]
        target = argv[6]
    else:
        exit(0)


    '''
    Instantiate
    '''
    for i in range(7,len(argv)):
        base_path = argv[i]
        create_floorplan(base_path, program_path, i)

    '''
    Save to file
    TODO add several save modes here!
    '''
    bpy.ops.wm.save_as_mainfile(filepath=program_path + target) #"/floorplan.blend"

    '''
    Send correct exit code
    '''
    exit(0)


def create_floorplan(base_path,program_path, name=0):

    parent, parent_mesh = init_object("Floorplan"+str(name))
    
    #base_path = base_path.replace('/','\\')

    path_to_wall_faces_file = program_path +"/" + base_path + "wall_faces"
    path_to_wall_verts_file = program_path +"/" + base_path + "wall_verts"

    path_to_top_wall_faces_file = program_path +"/" + base_path + "top_wall_faces"
    path_to_top_wall_verts_file = program_path +"/" + base_path + "top_wall_verts"

    path_to_floor_faces_file = program_path +"/" +base_path + "floor_faces"
    path_to_floor_verts_file = program_path +"/" +base_path + "floor_verts"

    path_to_rooms_faces_file = program_path +"/" + base_path + "rooms_faces"
    path_to_rooms_verts_file = program_path +"/" + base_path + "rooms_verts"

# TODO add  doors here!
    path_to_windows_faces_file = program_path +"\\" + base_path + "windows_faces"
    path_to_windows_verts_file = program_path +"\\" + base_path + "windows_verts"

    path_to_transform_file = program_path+"/" + base_path + "transform"

    '''
    Get transform
    '''
    # read from file
    transform = read_from_file(path_to_transform_file)

    rot = transform["rotation"]
    pos = transform["position"]

    # Calculate and move floorplan shape to center
    cen = transform["shape"]

    # rotate to fix mirrored floorplan
    parent.rotation_euler = (0, math.pi, 0)

    # Set Cursor start
    bpy.context.scene.cursor.location = (0,0,0)

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

    for walls in verts:
        boxname = "Box"+str(boxcount)
        for wall in walls:
            wallname = "Wall"+str(wallcount)

            obj = create_custom_mesh(
                boxname + wallname, wall, faces, pos=pos, rot=rot, cen=cen, mat=create_mat((0.5, 0.5, 0.5, 1)))
            obj.parent = wall_parent

            wallcount += 1
        boxcount += 1

    wall_parent.parent = parent

    '''
    Create Top  Walls
    '''
    # get image top wall data
    verts = read_from_file(path_to_top_wall_verts_file)
    faces = read_from_file(path_to_top_wall_faces_file)

    # Create mesh from data
    boxcount = 0
    wallcount = 0

    # Create parent
    top_wall_parent, top_wall_parent_mesh = init_object("TopWalls")

    for i in range(0, len(verts)):
        roomname = "TopWalls"+str(i)
        obj = create_custom_mesh(
            roomname, verts[i], faces[i], pos=pos, rot=rot, cen=cen, mat=create_mat((0.5, 0.5, 0.5, 1)))
        obj.parent = top_wall_parent

    top_wall_parent.parent = parent
    
    '''
    Create Windows
    '''
    # get image wall data
    verts = read_from_file(path_to_windows_verts_file)
    faces = read_from_file(path_to_windows_faces_file)

    # Create mesh from data
    boxcount = 0
    wallcount = 0

    # Create parent
    wall_parent, wall_parent_mesh = init_object("Windows")

    for walls in verts:
        boxname = "Box"+str(boxcount)
        for wall in walls:
            wallname = "Wall"+str(wallcount)

            obj = create_custom_mesh(
                boxname + wallname, wall, faces, pos=pos, rot=rot, cen=cen, mat=create_mat((0.5, 0.5, 0.5, 1)))
            obj.parent = wall_parent

            wallcount += 1
        boxcount += 1

    wall_parent.parent = parent


    '''
    Create Floor
    '''
    # get image wall data
    verts = read_from_file(path_to_floor_verts_file)
    faces = read_from_file(path_to_floor_faces_file)

    # Create mesh from data
    cornername="Floor"
    obj = create_custom_mesh(cornername, verts, [faces], pos=pos, mat=create_mat((40,1,1,1)), cen=cen)
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
        obj = create_custom_mesh(roomname, verts[i], faces[i], pos=pos, rot=rot, cen=cen)
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
    Save as param
    '''
