import cv2
import numpy as np
import json

'''
This file contains the old implementation
Where all functions are in this file...
'''


def main():
    '''
    Main function for testing and visualising

    https://mathematica.stackexchange.com/questions/19546/image-processing-floor-plan-detecting-rooms-borders-area-and-room-names-t
    '''

    img = cv2.imread("example2.png")


    height, width, channels = img.shape
    blank_image = np.zeros((height,width,3), np.uint8) # output image same size as original

    # grayscale
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # create wall image
    wall_img = wall_filter(gray)

    # detect corners
    corners, img = detectCorners(wall_img, img, [255,0,0])

    # detect boxes
    boxes, img = detectPreciseBoxes(wall_img, img ,[100,100,0])

    #detect outer Contours
    contour, img = detectOuterContours(gray, img, [0,255,0])

    # Show images
    cv2.imshow("a", img)
    cv2.imshow("b", wall_img)
    cv2.imshow("c", gray)

    # Exit
    cv2.waitKey()
    cv2.destroyAllWindows()

def generate_all_files():
    '''
    Generate all data files
    '''
    imgpath = "example.png"

    generate_floor_file(imgpath)
    generate_walls_file(imgpath)

def test():
    '''
    Test function for future use
    '''

    '''
    Receive image, convert
    '''
    # Read floorplan image
    img = cv2.imread("example.png")

    # grayscale image
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # Resulting image
    height, width, channels = img.shape
    blank_image = np.zeros((height,width,3), np.uint8) # output image same size as original

    # create wall image (filter out small objects from image)
    wall_img = wall_filter(gray)

    # detect walls
    boxes, img = detectPreciseBoxes(wall_img)

    # detect outer Contours (simple floor or roof solution)
    #contour, img = detectOuterContours(gray)

    res = detectAndRemovePreciseBoxes(wall_img, output_img = gray )

    # detect walls
    boxes, img = detectPreciseBoxes(out, output_img = gray)

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
TODO
Detect doors
'''

'''
TODO
Detect windows
'''

'''
TODO
Detect floors
'''

'''
TODO
Detect extra details
Maybe text detections
'''

def scale_point_to_vector(boxes, scale = 1, height = 0):
    '''
    @Param boxes
    @Param scale
    @Param height
    '''
    res = []
    for box in boxes:
        for pos in box:
            res.extend([(pos[0]/scale, pos[1]/scale, height)])
    return res

def generate_floor_file(img_path):
    '''
    Receive image, convert
    '''
    # Read floorplan image
    img = cv2.imread(img_path)

    # grayscale image
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # detect outer Contours (simple floor or roof solution)
    contour, img = detectOuterContours(gray)

    # create verts (points 3d), points to use in mesh creations
    verts = []
    # create faces for each plane, describe order to create mesh points
    faces = []

    # Height of waLL
    height = 0

    # Scale pixel value to 3d pos
    scale = 100

    #Create verts
    verts = scale_point_to_vector(contour, scale, height)

    # create faces
    count = 0
    for box in verts:
        faces.extend([(count)])
        count += 1

    save_to_file("floor_verts", verts)
    save_to_file("floor_faces", faces)

def generate_walls_file(img_path):
    '''
    generate wall data file for floorplan
    @Param img_path, path to input file
    '''
    # Read floorplan image
    img = cv2.imread(img_path)

    # grayscale image
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # create wall image (filter out small objects from image)
    wall_img = wall_filter(gray)

    # detect walls
    boxes, img = detectPreciseBoxes(wall_img)

    # create verts (points 3d), points to use in mesh creations
    verts = []
    # create faces for each plane, describe order to create mesh points
    faces = []

    # Height of waLL
    wall_height = 1

    # Scale pixel value to 3d pos
    scale = 100

    # Convert boxes to verts and faces
    verts, faces, wall_amount = create_nx4_verts_and_faces(boxes, wall_height, scale)

    # One solution to get data to blender is to write and read from file.
    save_to_file("wall_verts", verts)
    save_to_file("wall_faces", faces)

def save_to_file(file_path, data):
    '''
    Save to file
    Saves our resulting array as json in file.
    @Param file_path, path to outputfile
    @Param data, data to write to file
    '''
    with open(file_path+'.txt', 'w') as f:
        f.write(json.dumps(data))

    print("Created file : " + file_path + ".txt")

def read_from_file(file_path):
    '''
    Read from file
    read verts data from file
    @Param file_path, path to file
    @Return data
    '''
    #Now read the file back into a Python list object
    with open(file_path+'.txt', 'r') as f:
        data = json.loads(f.read())
    return data


def write_verts_on_2d_image(boxes, blank_image):
    '''
    Write verts as lines and show image
    @Param boxes, numpy array of boxes
    @Param blank_image, image to write and show
    '''

    for box in boxes:
        for wall in box:
            # draw line
            cv2.line(blank_image,(int(wall[0][0]),int(wall[1][1])),(int(wall[2][0]),int(wall[2][1])),(255,0,0),5)

    cv2.imshow('show image',blank_image)
    cv2.waitKey(0)

def create_nx4_verts_and_faces(boxes, height = 1, scale = 1):
    '''
    Create verts and faces

    @Param boxes,
    @Param height,
    @Param scale,
    @Return verts - as [[wall1],[wall2],...] numpy array, faces - as array to use on all boxes, wall_amount - as integer
    Use the result by looping over boxes in verts, and create mesh for each box with same face and pos
    See create_custom_mesh in floorplan code
    '''
    wall_counter = 0
    verts = []

    for box in boxes:
        box_verts = []
        for index in range(0, len(box) ):
            temp_verts = []
            # Get current
            curr = box[index][0];

            # is last, link to first
            if(len(box)-1 >= index+1):
                next = box[index+1][0];
            else:
                next = box[0][0]; # link to first pos

            # Create all 3d poses for each wall
            temp_verts.extend([(curr[0]/scale, curr[1]/scale, 0.0)])
            temp_verts.extend([(curr[0]/scale, curr[1]/scale, height)])
            temp_verts.extend([(next[0]/scale, next[1]/scale, 0.0)])
            temp_verts.extend([(next[0]/scale, next[1]/scale, height)])

            # add wall verts to verts
            box_verts.extend([temp_verts])

            # wall counter
            wall_counter += 1

        verts.extend([box_verts])

    faces = [(0, 1, 3, 2)]
    return verts, faces, wall_counter

def create_verts(boxes, height, scale):
    '''
    Simplified converts 2d poses to 3d poses, and adds a hight position
    @Param boxes, 2d boxes as numpy array
    @Param height, 3d height change
    @Param scale, pixel scale amount
    @Return verts, numpy array of vectors
    '''

    '''
    Scale and create array of box_verts
    [[box1],[box2],...]
    '''
    verts = []

    # for each wall group
    for box in boxes:
        temp_verts = []
        # for each pos
        for pos in box:

        # add and convert all positions
            temp_verts.extend([(pos[0][0]/scale, pos[0][1]/scale, 0.0)])
            temp_verts.extend([(pos[0][0]/scale, pos[0][1]/scale, height)])

        # add box to list
        verts.extend(temp_verts)

    return verts

def write_boxes_on_2d_image(boxes, blank_image):
    '''
    Write boxes as lines and show image
    @Param boxes, numpy array of boxes
    @Param blank_image, image to write and show
    '''

    for box in boxes:
        for index in range(0, len(box) ):

            curr = box[index][0];

            if(len(box)-1 >= index+1):
                next = box[index+1][0];
            else:
                next = box[0][0]; # link to first pos

            # draw line
            cv2.line(blank_image,(curr[0],curr[1]),(next[0],next[1]),(255,0,0),5)



    cv2.imshow('show image',blank_image)
    cv2.waitKey(0)



def wall_filter(gray):
    '''
    Filter walls
    @Return our thick wallmap
    '''

    ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    # noise removal
    kernel = np.ones((3,3),np.uint8)
    opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)

    sure_bg = cv2.dilate(opening,kernel,iterations=3)

    dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
    ret, sure_fg = cv2.threshold(0.5*dist_transform,0.2*dist_transform.max(),255,0)

    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg,sure_fg)

    return unknown

def detectCorners(detect_img, output_img = None, color = [255,0,0] ):
    '''
    Find each corner
    '''
    corners = cv2.goodFeaturesToTrack(detect_img, 1000, 0.1, 1)
    corners = np.int0(corners)

    if output_img is not None:
        for corner in corners:
            x,y = corner.ravel()
            cv2.circle(output_img,(x,y),3,255,-1)
    return corners, output_img

def Watermark(detect_img, output_img = None, color = [255,0,0]):
    '''
    Watershed

    https://docs.opencv.org/3.1.0/d3/db4/tutorial_py_watershed.html
    '''
    ret, markers = cv2.connectedComponents(detect_img)

    markers = markers+1
    markers[unknown==255] = 0
    if output_img is not None:
        markers = cv2.watershed(output_img,markers)
        output_img[markers == -1] = color
    return markers

def detectCenterBoxes(detect_img, output_img = None, color = [100,100,0]):
    '''
    Get center of objects

    https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_feature2d/py_features_harris/py_features_harris.html
    '''

    # find centroids
    ret, labels, stats, centroids = cv2.connectedComponentsWithStats(detect_img,4)

    # define the criteria to stop and refine the corners
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
    corners = cv2.cornerSubPix(detect_img,np.float32(centroids),(5,5),(-1,-1),criteria)

    # Now draw them
    res = np.hstack((centroids,corners))
    res = np.int0(res)
    if output_img is not None:
        output_img[res[:,1],res[:,0]]=[0,0,255]
        output_img[res[:,3],res[:,2]] = [0,255,0]

        i = len(res)-1
        print(res)
        while i >= 0:
            cv2.rectangle(output_img,(int(res[i][0]),int(res[i][1])),(int(res[i][2]),int(res[i][3])),color,3)
            i -= 1
    return res, output_img


def detectUnpreciseBoxes(detect_img, output_img = None, color = [100,100,0]):
    '''
    Bad boxes in image
    @Return boxes
    '''

    corners = cv2.cornerHarris(detect_img,2,3,0.04)
    res = cv2.dilate(corners, None, iterations=3)

    res = stats
    if output_img is not None:
        i = len(res)-1
        while i >= 0:
            cv2.rectangle(output_img,(int(res[i][0]),int(res[i][1])),(int(res[i][2]),int(res[i][3])),color,3)
            i -= 1
    return res, output_img

def detectPreciseBoxes(detect_img, output_img = None, color = [100,100,0]):
    '''
    Boxes in image
    @Return list of boxes

    Source
    https://stackoverflow.com/questions/50930033/drawing-lines-and-distance-to-them-on-image-opencv-python
    '''
    res = []

    im, contours, hierarchy = cv2.findContours(detect_img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    #area = sorted(contours, key=cv2.contourArea, reverse=True)

    largest_contour_area = 0
    for cnt in contours:
        largest_contour_area = cv2.contourArea(cnt)
        largest_contour = cnt

        epsilon = 0.001*cv2.arcLength(largest_contour,True)
        approx = cv2.approxPolyDP(largest_contour,epsilon,True)
        if output_img is not None:
            final = cv2.drawContours(output_img, [approx], 0, [100, 200, 0])
        res.append(approx)

    return res, output_img

def detectAndRemovePreciseBoxes(detect_img, output_img = None, color = [255, 255, 255]):
    '''
    Remove contours
    @Return list of boxes

    Source
    https://stackoverflow.com/questions/50930033/drawing-lines-and-distance-to-them-on-image-opencv-python
    '''

    res = []

    im, contours, hierarchy = cv2.findContours(detect_img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    #area = sorted(contours, key=cv2.contourArea, reverse=True)

    largest_contour_area = 0
    for cnt in contours:
        largest_contour_area = cv2.contourArea(cnt)
        largest_contour = cnt

        epsilon = 0.001*cv2.arcLength(largest_contour,True)
        approx = cv2.approxPolyDP(largest_contour,epsilon,True)
        if output_img is not None:
            cv2.drawContours( output_img,  [approx], -1, color, -1);
        res.append(approx)

    return res, output_img

def detectOuterContours(detect_img, output_img = None, color = [255, 255, 255]):
    '''
    Get the outer side of image
    @Return box

    Source
    https://stackoverflow.com/questions/50930033/drawing-lines-and-distance-to-them-on-image-opencv-python
    '''
    ret, thresh = cv2.threshold(detect_img, 230, 255, cv2.THRESH_BINARY_INV)

    img_, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    largest_contour_area = 0
    for cnt in contours:
        if (cv2.contourArea(cnt) > largest_contour_area):
            largest_contour_area = cv2.contourArea(cnt)
            largest_contour = cnt

    epsilon = 0.001*cv2.arcLength(largest_contour,True)
    approx = cv2.approxPolyDP(largest_contour,epsilon,True)
    if output_img is not None:
        final = cv2.drawContours(output_img, [approx], 0, color)
    return approx, output_img


def rectContains(rect,pt):
    '''
    Rect contains

    Source:
    https://stackoverflow.com/questions/33065834/how-to-detect-if-a-point-is-contained-within-a-bounding-rect-opecv-python
    '''
    return rect[0] < pt[0] < rect[0]+rect[2] and rect[1] < pt[1] < rect[1]+rect[3]


def detectLines(detect_img, output_img = None, color = [255, 255, 255]):
    '''
    Detect lines in image
    @Return list of lines

    Source:
    https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_houghlines/py_houghlines.html
    '''

    edges = cv2.Canny(detect_img,50,120)
    minLineLength = 20
    maxLineGap = 50
    lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)
    i = len(lines)-1

    if output_img is not None:
        while i > 0:
            i -= 1;
            for x1,y1,x2,y2 in lines[i]:
                cv2.line(output_img,(x1,y1),(x2,y2),color,2)

    return lines, output_img


'''
Uncomment this for testing
'''
if __name__ == "__main__":
    test()
    #generate_all_files()
    #main()


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
