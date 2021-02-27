"""
The process class represents a thread handling stuff in new threads
"""
import threading
from process.process import Process

import sys
sys.path.insert(0,'..')
from FloorplanToBlenderLib import * # floorplan to blender lib

"""This process should create a 3d object file using the FTBLibrary"""
class Create(Process):

    def __init__(self, data, shared_variables):
        super().__init__(data, shared_variables=shared_variables)
        # We expect following fields in data
        # {'func': 'transform', 'id':id, 'format':'.obj'}
        self.process["task"]= data['func']
        self.process["in"]= data['id']
        self.process["cstate"]= 4 #set amount of state -1 here, useful for gui later!
        # we will overwrite old objects!
        self.update("out", data['id']+data['format'])
    
    def run(self):
        # This is where the new thread will start
        image_path = self.shared.get_image_path(self.process["in"])
        
        _, blender_install_path, _, _ = IO.config_get_default()

        # Set other paths (don't need to change these)
        program_path = os.path.dirname(os.path.realpath(__file__))
        blender_script_path = "Blender/floorplan_to_3dObject_in_blender.py"

        IO.clean_data_folder("Data/")

        self.process["state"] = self.process["state"]+1
        self.update("status", "Image processing calculations")
        # Generate data files
        data_paths = list()
        data_paths = [execution.simple_single(image_paths[0])]

        
        '''
        #Debug print
        print(str([blender_install_path,
        "-noaudio", # this is an ubuntu hax fix
        "--background",
        "--python",
        blender_script_path,
        program_path # Send this as parameter to script
        ] +  data_paths))
        '''

        self.process["state"] = self.process["state"]+1
        self.update("status", "Creating objects in Blender3d")
        # Create blender project
        check_output([blender_install_path,
        "-noaudio", # this is a dockerfile ubuntu hax fix
        "--background",
        "--python",
        blender_script_path,
        program_path, # Send this as parameter to script
        ] +  data_paths)

        self.process["state"] = self.process["state"]+1
        self.update("status", "Create Object file")
        
        self.process["state"] = self.process["state"]+1
        self.update("status", "Clear tmp files and cashe")
        
        self.process["state"] = self.process["state"]+1
        self.update("status", "Done")

