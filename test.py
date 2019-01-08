import cv2
import numpy as np
from FloorplanToBlenderLib import * # floorplan to blender lib
from subprocess import check_output

'''
This is a test file, used to develop and test new functions
'''


def test():
    '''
    Test function for future use
    '''

    '''
    Receive image, convert
    '''
    # Read floorplan image
    img = cv2.imread("Examples/example.png")

    # grayscale image
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # Resulting image
    height, width, channels = img.shape
    blank_image = np.zeros((height,width,3), np.uint8) # output image same size as original

    # create wall image (filter out small objects from image)
    wall_img = detect.wall_filter(gray)

    # detect walls
#    boxes, img = detect.detectPreciseBoxes(wall_img)

    # detect outer Contours (simple floor or roof solution)
    #contour, img = detectOuterContours(gray)

    res, out = detect.detectAndRemovePreciseBoxes(wall_img, output_img = gray )

    # detect walls
    boxes, img = detect.detectPreciseBoxes(out, output_img = gray)

    # create verts (points 3d), points to use in mesh creations
    verts = []
    # create faces for each plane, describe order to create mesh points
    faces = []

    # Height of waLL
    height = 0

    # Scale pixel value to 3d pos
    scale = 100

    #cv2.imshow('1t', img)
    cv2.imshow('2t', gray)

    cv2.waitKey(0)

    print(boxes)
    #print(out)

    #save_to_file("floor_verts", verts)
    #save_to_file("floor_faces", faces)

    # Write walls on image, by using draw line and box positions
    #write_boxes_on_2d_image(boxes, blank_image)

    #verts, faces, wall_amount = create_verts_and_faces(boxes, wall_height, scale)

    #write_verts_on_2d_image(verts, blank_image)

    # One solution to get data to blender is to write and read from file.
    #save_to_file("test", verts)
    #verts = read_from_file("C:\\Users\\Daniel\\Documents\\GitHub\\ApartmentDrawing-To-Blender\\Drawing_To_Array\\test")
    #print (verts)
    print("Test Done!")



'''
Start here
'''
if __name__ == "__main__":
    #test()
    #generate.generate_all_files("Examples/example.png")

    print("C:\\Program Files\\Blender Foundation\\Blender\\blender.exe "+
    "--background --python Blender/floorplan_to_3dObject_in_blender "+
    "--text='Floorplan' " +
    "--save='Floorplan.blend'")


#          --save="/tmp/hello.blend"

    check_output(["C:\\Program Files\\Blender Foundation\\Blender\\blender.exe ",
     "--background",
    # "--factory-startup",
     "--python",
     "Blender/floorplan_to_3dObject_in_blender.py",
       ])
