import cv2
import numpy as np

from . import detect
from . import IO
from . import transform
from . import generate

'''
Execution
This file contains some example usages and creations of multiple floorplans.

FloorplanToBlender3d
Copyright (C) 2019 Daniel Westberg
'''

def simple_single(image_path):
    '''
    Generate one simple floorplan
    @Param image_path path to image
    @Return path to generated files
    '''
    fpath, fshape = generate.generate_all_files(image_path, True)
    return fpath

def multiple_simple(image_paths, horizontal=True):
    '''
    Generates several new appartments
    @Param image_paths - list of path to images
    @Param horizontal - if apartments should stack horizontal or vertical
    @Return paths to image data
    '''
    # Generate data files
    data_paths = list()
    fshape = None
    # for each input image path!
    for image_path in image_paths:
        # Calculate positions and rotations here!

        if fshape is not None:
            # Generate all data for imagepath
            if horizontal:
                fpath, fshape = generate.generate_all_files(image_path, True, position=(0,fshape[1],0))
            else:
                fpath, fshape = generate.generate_all_files(image_path, True, position=(fshape[0],0,0))

        else:
            fpath, fshape = generate.generate_all_files(image_path, True)

        # add path to send to blender
        data_paths.append(fpath)
    return data_paths

def multiple_coord(image_paths):
    '''
    Generates new appartments with fixed coordinates!
    @Param image_paths - list of tuples containing [(img_path, pos)]
    @Return paths to image data
    '''
    # Generate data files
    data_paths = list()
    fshape = None
    # for each input image path!
    for tup in image_paths:
        image_path = tup[0]
        pos = tup[1]
        # Calculate positions and rotations here!

        if pos is not None:
            fpath, fshape = generate.generate_all_files(image_path, True, position=(pos[0],pos[1],pos[2]))
        else:
            if fshape is not None:
                fpath, fshape = generate.generate_all_files(image_path, True, position=(fshape[0],fshape[1],fshape[2]))
            else:
                fpath, fshape = generate.generate_all_files(image_path, True)

        # add path to send to blender
        data_paths.append(fpath)
    return data_paths
