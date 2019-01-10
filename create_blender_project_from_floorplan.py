from subprocess import check_output


'''
Start here
'''
if __name__ == "__main__":

    # Set required paths
    image_path = "Examples/example.png"
    blender_install_path = "C:\\Program Files\\Blender Foundation\\Blender\\blender.exe"

    # Set other paths
    data_path = "Data/"
    blender_script_path = "Blender/floorplan_to_3dObject_in_blender.py"

    # Generate data files
    generate.generate_all_files(image_path, data_path)

    # Create blender project
    check_output([blender_install_path,
     "--background",
     "--python",
     blender_script_path,
     data_path # Send this as parameter to script
       ])


    #https://blender.stackexchange.com/questions/1365/how-can-i-run-blender-from-command-line-or-a-python-script-without-opening-a-gui
    #blender --background --factory-startup --python $HOME/background_job.py -- \
    #          --text="Hello World" \
    #          --render="/tmp/hello" \
    #          --save="/tmp/hello.blend"
    #
    # Notice:
    # '--factory-startup' is used to avoid the user default settings from
    #                     interfering with automated scene generation.
    #
    # '--' causes blender to ignore all following arguments so python can use them.
    #
    # See blender --help for details.
