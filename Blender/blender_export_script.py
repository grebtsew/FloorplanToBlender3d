import bpy
import os

blend_file_path = bpy.data.filepath
directory = os.path.dirname(blend_file_path)
target_file = os.path.join(directory, 'myfile.obj')

bpy.ops.export_scene.obj(filepath=target_file)
