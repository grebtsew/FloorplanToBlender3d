from subprocess import check_output
import os
import sys
floorplan_lib_path = os.path.dirname(os.path.realpath(__file__))+"/../../"

sys.path.insert(0,floorplan_lib_path)
from FloorplanToBlenderLib import * # floorplan to blender lib

from pyfiglet import Figlet

f = Figlet(font='slant')
print (f.renderText('Floorplan to Blender3d'))

'''
Multi create coordinates
This is an example of how to create multiple floorplans with coordinates.
'''
if __name__ == "__main__":

    # Set required default paths
    blender_install_path = "" # path to blender installation folder

    image_path, blender_install_path, t, s = IO.config_get_default()

    # Set other paths (don't need to change these)
    program_path = os.path.dirname(os.path.realpath(__file__))
    blender_script_path = floorplan_lib_path+"/Blender/floorplan_to_3dObject_in_blender.py"

    # Clean
    IO.clean_data_folder(floorplan_lib_path+"/Data/")

    image_paths = [(floorplan_lib_path+"/Images/example.png", (1,1,1)),(floorplan_lib_path+"/Images/example.png", (20,1,1)),(floorplan_lib_path+"/Images/example.png", (-10,1,1)) ]

    print("")
    print(" Show array of floorplans to create with coordinates:")
    print("")
    for tup in image_paths:
        print(tup)

    # the actual generating
    data_paths = execution.multiple_coord(image_paths)

    repaths = []
    for p in data_paths:
        print
        repaths.append(floorplan_lib_path+"/"+p)

    data_paths = repaths
    
    print("")
    print("Creates blender project")
    print("")

    # Create blender project
    check_output([blender_install_path,
     "--background",
     "--python",
     blender_script_path,
     program_path # Send this as parameter to script
     ] +  data_paths) # TODO something is up with this! Check on this later!

    print("Project created at: " + program_path + "\\floorplan.blender")
    print("")
    print("Done, Have a nice day!")
