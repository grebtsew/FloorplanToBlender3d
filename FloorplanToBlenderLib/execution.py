import cv2
import numpy as np

from . import detect
from . import IO
from . import transform

def single():
    pass

def multiple_simple(image_paths, horizontal=True):
    '''
    Generates new appartments
    @Param image_paths - list of path to images
    @Param horizontal - if apartments should stack horizontal or not
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
    Generates new appartments
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

def multiple_dynamic(image_paths):
    '''
    Generates new appartments
    @Param image_paths - list of dynamic tuple, examples [((path, offset), (path), (path)),(),()]
    @Return paths to image data
    '''
    # Generate data files
    data_paths = list()
    fshape = None
    tot_fshape = None
    # for each input image path!
    _x = 0
    for x in image_paths:
        _y=0
        if(isinstance(x[0],str)): # img path
            if fshape is not None:
                fpath, fshape = generate.generate_all_files(image_path, True, position=(tot_fshape[0],0,0))
                data_paths.append(fpath)
                tot_fshape[0]+= fshape[0]
            else:
                fpath, fshape = generate.generate_all_files(image_path, True, position=(0,0,0))
        else:

            for y in x:
                _z=0
                if(isinstance(y[0],str)): # img path
                    if fshape is not None:
                        fpath, fshape = generate.generate_all_files(image_path, True, position=(0,tot_fshape[1],0))
                        data_paths.append(fpath)
                        tot_fshape[1]+= fshape[1]
                    else:
                        fpath, fshape = generate.generate_all_files(image_path, True, position=(0,0,0))
                else:
                    for z in y:
                        if(isinstance(z[0],str)): # img path
                            if fshape is not None:
                                fpath, fshape = generate.generate_all_files(image_path, True, position=(0,0,tot_fshape[2]))
                                data_paths.append(fpath)
                                tot_fshape[2]+= fshape[2]
                            else:
                                fpath, fshape = generate.generate_all_files(image_path, True, position=(0,0,0))
                    _z+=1
                _y+=1
        _x+=1

    return data_paths
