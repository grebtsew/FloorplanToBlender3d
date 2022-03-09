import bpy
import sys

"""
FloorplanToBlender3d
Copyright (C) 2021 Daniel Westberg
"""

"""
Used to open a .blender file and export it as .obj file.
"""

# Start
if __name__ == "__main__":
    argv = sys.argv

    output_path = argv[
        5
    ]  # strict argc==5 -> len=6 will be used as argument see Reformat_blender_to_obj.py

    bpy.ops.export_scene.obj(filepath=output_path)

    # Must exit with 0 to avoid error!
    exit(0)
