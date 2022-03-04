import bpy
import numpy as np
import json
import sys
import math
import os.path

"""
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

This code is tested on Windows 10, Blender 2.93, in December 2021.
"""

"""
Our helpful functions
"""

# TODO: restructure this file with a class and help-function to save a lot of lines of code!
# TODO: fix index should be same as floorplan folder


def read_from_file(file_path):
    """
    Read from file
    read verts data from file
    @Param file_path, path to file
    @Return data
    """
    # Now read the file back into a Python list object
    with open(file_path + ".txt", "r") as f:
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
    x = []
    y = []
    z = []

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


def create_custom_mesh(objname, verts, faces, mat=None, cen=None):
    """
    @Param objname, name of new mesh
    @Param pos, object position [x, y, z]
    @Param vertex, corners
    @Param faces, buildorder
    """
    # Create mesh and object
    myobject, mymesh = init_object(objname)

    # Rearrange verts to put pivot point in center of mesh
    # Find center of verts
    center = get_mesh_center(verts)
    # Subtract center from verts before creation
    proper_verts = subtract_center_verts(center, verts)

    # Generate mesh data
    mymesh.from_pydata(proper_verts, [], faces)
    # Calculate the edges
    mymesh.update(calc_edges=True)

    parent_center = [0, 0, 0]
    if cen is not None:
        parent_center = [int(cen[0] / 2), int(cen[1] / 2), int(cen[2])]

    # Move object to input verts location
    myobject.location.x = center[0] - parent_center[0]
    myobject.location.y = center[1] - parent_center[1]
    myobject.location.z = center[2] - parent_center[2]

    # add material
    if mat is None:  # add random color
        myobject.data.materials.append(
            create_mat(np.random.randint(0, 40, size=4))
        )  # add the material to the object
    else:
        myobject.data.materials.append(mat)  # add the material to the object
    return myobject


def create_mat(rgb_color):
    mat = bpy.data.materials.new(name="MaterialName")  # set new material to variable
    mat.diffuse_color = rgb_color  # change to random color
    return mat


"""
Main functionality here!
"""


def main(argv):

    # Remove starting object cube
    objs = bpy.data.objects
    objs.remove(objs["Cube"], do_unlink=True)

    if len(argv) > 7:  # Note YOU need 8 arguments!
        program_path = argv[5]
        target = argv[6]
    else:
        exit(0)

    """
    Instantiate
    Each argument after 7 will be a floorplan path
    """
    for i in range(7, len(argv)):
        base_path = argv[i]
        create_floorplan(base_path, program_path, i)

    """
    Save to file
    TODO add several save modes here!
    """
    bpy.ops.wm.save_as_mainfile(filepath=program_path + target)  # "/floorplan.blend"

    """
    Send correct exit code
    """
    exit(0)


def create_floorplan(base_path, program_path, name=None):

    if name is None:
        name = 0

    parent, _ = init_object("Floorplan" + str(name))

    """
    Get transform data
    """

    path_to_transform_file = program_path + "/" + base_path + "transform"

    # read from file
    transform = read_from_file(path_to_transform_file)

    rot = transform["rotation"]
    pos = transform["position"]
    scale = transform["scale"]

    # Calculate and move floorplan shape to center
    cen = transform["shape"]

    # Where data is stored, if shared between floorplans
    path_to_data = transform["origin_path"]

    # Set Cursor start
    bpy.context.scene.cursor.location = (0, 0, 0)

    path_to_wall_vertical_faces_file = (
        program_path + "/" + path_to_data + "wall_vertical_faces"
    )
    path_to_wall_vertical_verts_file = (
        program_path + "/" + path_to_data + "wall_vertical_verts"
    )

    path_to_wall_horizontal_faces_file = (
        program_path + "/" + path_to_data + "wall_horizontal_faces"
    )
    path_to_wall_horizontal_verts_file = (
        program_path + "/" + path_to_data + "wall_horizontal_verts"
    )

    path_to_floor_faces_file = program_path + "/" + path_to_data + "floor_faces"
    path_to_floor_verts_file = program_path + "/" + path_to_data + "floor_verts"

    path_to_rooms_faces_file = program_path + "/" + path_to_data + "room_faces"
    path_to_rooms_verts_file = program_path + "/" + path_to_data + "room_verts"

    path_to_doors_vertical_faces_file = (
        program_path + "\\" + path_to_data + "door_vertical_faces"
    )
    path_to_doors_vertical_verts_file = (
        program_path + "\\" + path_to_data + "door_vertical_verts"
    )

    path_to_doors_horizontal_faces_file = (
        program_path + "\\" + path_to_data + "door_horizontal_faces"
    )
    path_to_doors_horizontal_verts_file = (
        program_path + "\\" + path_to_data + "door_horizontal_verts"
    )

    path_to_windows_vertical_faces_file = (
        program_path + "\\" + path_to_data + "window_vertical_faces"
    )
    path_to_windows_vertical_verts_file = (
        program_path + "\\" + path_to_data + "window_vertical_verts"
    )

    path_to_windows_horizontal_faces_file = (
        program_path + "\\" + path_to_data + "window_horizontal_faces"
    )
    path_to_windows_horizontal_verts_file = (
        program_path + "\\" + path_to_data + "window_horizontal_verts"
    )

    """
    Create Walls
    """

    if (
        os.path.isfile(path_to_wall_vertical_verts_file + ".txt")
        and os.path.isfile(path_to_wall_vertical_faces_file + ".txt")
        and os.path.isfile(path_to_wall_horizontal_verts_file + ".txt")
        and os.path.isfile(path_to_wall_horizontal_faces_file + ".txt")
    ):
        # get image wall data
        verts = read_from_file(path_to_wall_vertical_verts_file)
        faces = read_from_file(path_to_wall_vertical_faces_file)

        # Create mesh from data
        boxcount = 0
        wallcount = 0

        # Create parent
        wall_parent, _ = init_object("Walls")

        for walls in verts:
            boxname = "Box" + str(boxcount)
            for wall in walls:
                wallname = "Wall" + str(wallcount)

                obj = create_custom_mesh(
                    boxname + wallname,
                    wall,
                    faces,
                    cen=cen,
                    mat=create_mat((0.5, 0.5, 0.5, 1)),
                )
                obj.parent = wall_parent

                wallcount += 1
            boxcount += 1

        # get image top wall data
        verts = read_from_file(path_to_wall_horizontal_verts_file)
        faces = read_from_file(path_to_wall_horizontal_faces_file)

        # Create mesh from data
        boxcount = 0
        wallcount = 0

        for i in range(0, len(verts)):
            roomname = "VertWalls" + str(i)
            obj = create_custom_mesh(
                roomname,
                verts[i],
                faces[i],
                cen=cen,
                mat=create_mat((0.5, 0.5, 0.5, 1)),
            )
            obj.parent = wall_parent

        wall_parent.parent = parent

    """
    Create Windows
    """
    if (
        os.path.isfile(path_to_windows_vertical_verts_file + ".txt")
        and os.path.isfile(path_to_windows_vertical_faces_file + ".txt")
        and os.path.isfile(path_to_windows_horizontal_verts_file + ".txt")
        and os.path.isfile(path_to_windows_horizontal_faces_file + ".txt")
    ):
        # get image wall data
        verts = read_from_file(path_to_windows_vertical_verts_file)
        faces = read_from_file(path_to_windows_vertical_faces_file)

        # Create mesh from data
        boxcount = 0
        wallcount = 0

        # Create parent
        wall_parent, _ = init_object("Windows")

        for walls in verts:
            boxname = "Box" + str(boxcount)
            for wall in walls:
                wallname = "Wall" + str(wallcount)

                obj = create_custom_mesh(
                    boxname + wallname,
                    wall,
                    faces,
                    cen=cen,
                    mat=create_mat((0.5, 0.5, 0.5, 1)),
                )
                obj.parent = wall_parent

                wallcount += 1
            boxcount += 1

        # get windows
        verts = read_from_file(path_to_windows_horizontal_verts_file)
        faces = read_from_file(path_to_windows_horizontal_faces_file)

        # Create mesh from data
        boxcount = 0
        wallcount = 0

        for i in range(0, len(verts)):
            roomname = "VertWindow" + str(i)
            obj = create_custom_mesh(
                roomname,
                verts[i],
                faces[i],
                cen=cen,
                mat=create_mat((0.5, 0.5, 0.5, 1)),
            )
            obj.parent = wall_parent

        wall_parent.parent = parent

    """
    Create Doors
    """
    if (
        os.path.isfile(path_to_doors_vertical_verts_file + ".txt")
        and os.path.isfile(path_to_doors_vertical_faces_file + ".txt")
        and os.path.isfile(path_to_doors_horizontal_verts_file + ".txt")
        and os.path.isfile(path_to_doors_horizontal_faces_file + ".txt")
    ):

        # get image wall data
        verts = read_from_file(path_to_doors_vertical_verts_file)
        faces = read_from_file(path_to_doors_vertical_faces_file)

        # Create mesh from data
        boxcount = 0
        wallcount = 0

        # Create parent
        wall_parent, _ = init_object("Doors")

        for walls in verts:
            boxname = "Box" + str(boxcount)
            for wall in walls:
                wallname = "Wall" + str(wallcount)

                obj = create_custom_mesh(
                    boxname + wallname,
                    wall,
                    faces,
                    cen=cen,
                    mat=create_mat((0.5, 0.5, 0.5, 1)),
                )
                obj.parent = wall_parent

                wallcount += 1
            boxcount += 1

        # get windows
        verts = read_from_file(path_to_doors_horizontal_verts_file)
        faces = read_from_file(path_to_doors_horizontal_faces_file)

        # Create mesh from data
        boxcount = 0
        wallcount = 0

        for i in range(0, len(verts)):
            roomname = "VertWindow" + str(i)
            obj = create_custom_mesh(
                roomname,
                verts[i],
                faces[i],
                cen=cen,
                mat=create_mat((0.5, 0.5, 0.5, 1)),
            )
            obj.parent = wall_parent

        wall_parent.parent = parent

    """
    Create Floor
    """
    if os.path.isfile(path_to_floor_verts_file + ".txt") and os.path.isfile(
        path_to_floor_faces_file + ".txt"
    ):

        # get image wall data
        verts = read_from_file(path_to_floor_verts_file)
        faces = read_from_file(path_to_floor_faces_file)

        # Create mesh from data
        cornername = "Floor"
        obj = create_custom_mesh(
            cornername, verts, [faces], mat=create_mat((40, 1, 1, 1)), cen=cen
        )
        obj.parent = parent

        """
        Create rooms
        """
        # get image wall data
        verts = read_from_file(path_to_rooms_verts_file)
        faces = read_from_file(path_to_rooms_faces_file)

        # Create parent
        room_parent, _ = init_object("Rooms")

        for i in range(0, len(verts)):
            roomname = "Room" + str(i)
            obj = create_custom_mesh(roomname, verts[i], faces[i], cen=cen)
            obj.parent = room_parent

        room_parent.parent = parent

    # Perform Floorplan final position, rotation and scale
    if rot is not None:
        # compensate for mirrored image
        parent.rotation_euler = [
            math.radians(rot[0]) + math.pi,
            math.radians(rot[1]),
            math.radians(rot[2]),
        ]

    if pos is not None:
        parent.location.x += pos[0]
        parent.location.y += pos[1]
        parent.location.z += pos[2]

    if scale is not None:
        parent.scale.x = scale[0]
        parent.scale.y = scale[1]
        parent.scale.z = scale[2]


if __name__ == "__main__":
    main(sys.argv)
