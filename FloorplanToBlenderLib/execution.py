from . import generate

"""
Execution
This file contains some example usages and creations of multiple floorplans.

FloorplanToBlender3d
Copyright (C) 2021 Daniel Westberg
"""


def simple_single(image_path, show=True):
    """
    Generate one simple floorplan
    @Param image_path path to image
    @Return path to generated files
    """
    filepath, _ = generate.generate_all_files(image_path, show)
    return filepath


def multiple_simple(image_paths, horizontal=True): # TODO: use axis instead
    """
    Generates several new apartments
    @Param image_paths - list of path to images
    @Param horizontal - if apartments should stack horizontal or vertical
    @Return paths to image data
    """
    # Generate data files
    data_paths = list()
    fshape = None
    # for each input image path!
    for image_path in image_paths: 
        # TODO: check if image data already is generated
        # TODO: don't overwrite old data
        
        # Calculate positions and rotations here!
        if fshape is not None:
            # Generate all data for imagepath
            if horizontal: 
                filepath, fshape = generate.generate_all_files(
                    image_path, True, position=(0, fshape[1], 0)
                )
            else:
                filepath, fshape = generate.generate_all_files(
                    image_path, True, position=(fshape[0], 0, 0)
                )

        else:
            filepath, fshape = generate.generate_all_files(image_path, True)

        # add path to send to blender
        data_paths.append(filepath)
    return data_paths


def multiple_coord(image_paths):
    """
    Generates new apartments with fixed coordinates!
    @Param image_paths - list of tuples containing [(img_path, pos)]
    @Return paths to image data
    """
    # Generate data files
    data_paths = list()
    fshape = None
    # for each input image path!
    for tup in image_paths:
        image_path = tup[0]
        pos = tup[1]
        # Calculate positions and rotations here!

        if pos is not None:
            filepath, fshape = generate.generate_all_files(
                image_path, True, position=(pos[0], pos[1], pos[2])
            )
        else:
            if fshape is not None:
                filepath, fshape = generate.generate_all_files(
                    image_path, True, position=(fshape[0], fshape[1], fshape[2])
                )
            else:
                filepath, fshape = generate.generate_all_files(image_path, True)

        # add path to send to blender
        data_paths.append(filepath)
    return data_paths
