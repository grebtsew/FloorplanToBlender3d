from subprocess import check_output

"""
If we want to use the floorplan in for instance blender we can use this script to format the .blender file as .obj to fetch it in unity!
"""

blender_install_path = "C:\\Program Files\\Blender Foundation\\Blender\\blender.exe"
program_path = ".."

check_output(
    [
        blender_install_path,
        "--background",
        program_path + "/floorplan.blend",
        "--python",
        program_path + "/Blender/blender_export_obj_script.py",
        program_path + "/result.obj",
    ]
)
