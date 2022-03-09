import bpy
import os
import sys

"""
FloorplanToBlender3d
Copyright (C) 2021 Daniel Westberg
"""

"""
Imports an arbitrary object and reformat it as something else!
"""
if __name__ == "__main__":
    argv = sys.argv

    input_path = argv[5]
    bpy.ops.wm.open_mainfile(filepath=input_path)

    format = argv[6]
    output_path = argv[
        7
    ]  # strict argc==5 -> len=6 will be used as argument see Reformat_blender_to_obj.py

    if format == ".obj":
        bpy.ops.export_scene.obj(filepath=output_path)
    elif format == ".fbx":
        bpy.ops.export_scene.fbx(filepath=output_path)
    elif format == ".gltf":
        bpy.ops.export_scene.gltf(filepath=output_path)
    elif format == ".x3d":
        bpy.ops.export_scene.x3d(filepath=output_path)
    elif format == ".blend":
        bpy.ops.wm.save_as_mainfile(filepath=output_path)
    else:
        # default
        bpy.ops.export_scene.obj(filepath=output_path)

    # Must exit with 0 to avoid error!
    exit(0)
