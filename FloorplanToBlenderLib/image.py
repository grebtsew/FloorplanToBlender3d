import cv2
import numpy as np
from PIL import Image
from . import detect


def pil_rescale_image(image,factor ):
    width, height = image.size
    return image.resize((int(width*factor),int(height*factor)), resample=Image.BOX)

def cv2_rescale_image(image,factor):
    return cv2.resize(image, None, fx=factor, fy=factor )

def pil_to_cv2(image):
    return cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)

def calculate_scale_factor(preferred, value):
    return preferred/value

def denoising(img):
    return cv2.fastNlMeansDenoisingColored(img,None,10,10,7,21)

def remove_noise(img, noise_removal_threshold):
    """
    Remove noise from image and return mask
    Help function for finding room
    @Param img @mandatory image to remove noise from
    @Param noise_removal_threshold @mandatory threshold for noise
    @Return return new mask of image
    """
    img[img < 128] = 0
    img[img > 128] = 255
    contours, _ = cv2.findContours(~img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mask = np.zeros_like(img)
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > noise_removal_threshold:
            cv2.fillPoly(mask, [contour], 255)
    return mask

def average(lst):
    return sum(lst) / len(lst)

def calculate_wall_width_average(img):
    # Calculates average pixels per image wall
    image = img
    # grayscale image
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # Resulting image
    height, width, channels = img.shape
    blank_image = np.zeros((height,width,3), np.uint8) # output image same size as original

    # create wall image (filter out small objects from image)
    wall_img = detect.wall_filter(gray)
    wall_temp = wall_img
    '''
    Detect Wall
    '''
    # detect walls
    boxes, img = detect.detectPreciseBoxes(wall_img, blank_image)

    # filter out to only count walls
    filtered_boxes = list()
    for box in boxes:
        if len(box) == 4: # got only 4 corners  # detect oblong
            x,y,w,h = cv2.boundingRect(box)
            # Calculate scale value
            # 1. get shortest (width) side
            if w > h:
                shortest = h
            else:
                shortest = w 
            filtered_boxes.append(shortest)
    # 2. calculate average
    return average(filtered_boxes)
