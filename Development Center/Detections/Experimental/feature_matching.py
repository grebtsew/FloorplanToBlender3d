"""
Feature Matching 

While studing and developing ar i thought this method could be used to find windows and doors

https://bitesofcode.wordpress.com/2017/09/12/augmented-reality-with-python-and-opencv-part-1/
"""
import os
import cv2
import numpy as np
from matplotlib import pyplot as plt


def brisk_feature_detect(img):
    """
    Find features in image
    """
    brisk = cv2.BRISK_create(1, 2)
    (kp,des) = brisk.detectAndCompute(img,None) 
    
    # draw only keypoints location,not size and orientation
    img2 = cv2.drawKeypoints(img, kp, img, color=(0,255,0), flags=0)
    cv2.imshow('keypoints',img2)
    cv2.waitKey(0)

def fast_feature_detect(img):
    """
    Find features in image
    """
    # Initiate FAST object with default values
    fast = cv2.FastFeatureDetector_create(threshold=1)

    # find and draw the keypoints
    kp = fast.detect(img, None)
    
    # calculate des
    br = cv2.BRISK_create(10000000,2)
    kp, des = br.compute(img,  kp)  # note: no mask here!
    
    print("Threshold: ", fast.getThreshold())
    print("nonmaxSuppression: ", fast.getNonmaxSuppression())
    print("neighborhood: ", fast.getType())
    print("Total Keypoints with nonmaxSuppression: ", len(kp))    

    # draw only keypoints location,not size and orientation
    img2 = cv2.drawKeypoints(img, kp, img, color=(0,255,0), flags=0)
    cv2.imshow('keypoints',img2)
    cv2.waitKey(0)

def feature_detect(img):
    """
    Find features in image
    """

    # Initiate ORB detector
    orb = cv2.ORB_create(nfeatures=10000000, scoreType=cv2.ORB_FAST_SCORE)
 
    # find the keypoints with ORB
    kp = orb.detect(img, None)

    # compute the descriptors with ORB
    kp, des = orb.compute(img, kp)

    # draw only keypoints location,not size and orientation
    img2 = cv2.drawKeypoints(img, kp, img, color=(0,255,0), flags=0)
    cv2.imshow('keypoints',img2)
    cv2.waitKey(0)

def fast_feature_match(img1, img2):
    
     # Initiate FAST object with default values
    fast = cv2.FastFeatureDetector_create(threshold=60)
    
    MIN_MATCHES = 0
    cap = img1    
    model = img2
    # ORB keypoint detector
    br = cv2.BRISK_create();
    # create brute force  matcher object
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)  
    # Compute model keypoints and its descriptors
    # find and draw the keypoints
    
    kp_m = fast.detect(img2, None)
    kp_model, des_model = br.compute(img2, kp_m)
    
    # Compute scene keypoints and its descriptors
    kp_f = fast.detect(img1, None)
    kp_frame, des_frame = br.compute(img1, kp_f)
    
    # Match frame descriptors with model descriptors
    matches = bf.match(des_model, des_frame)
    # Sort them in the order of their distance
    matches = sorted(matches, key=lambda x: x.distance)

    if len(matches) > MIN_MATCHES:
        # draw first 15 matches.
        cap = cv2.drawMatches(model, kp_model, cap, kp_frame,
                            matches[:MIN_MATCHES], 0, flags=2)
        # show result
        cv2.imshow('frame', cap)
        cv2.waitKey(0)
    else:
        print( "Not enough matches have been found - %d/%d" % (len(matches),
                                                            MIN_MATCHES))


def feature_match(img1, img2):
    MIN_MATCHES = 20
    cap = img1    
    model = img2
    # ORB keypoint detector
    orb = cv2.ORB_create(nfeatures=10000000, scoreType=cv2.ORB_FAST_SCORE)              
    # create brute force  matcher object
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)  
    # Compute model keypoints and its descriptors
    kp_model, des_model = orb.detectAndCompute(model, None)  
    # Compute scene keypoints and its descriptors
    kp_frame, des_frame = orb.detectAndCompute(cap, None)
    # Match frame descriptors with model descriptors
    matches = bf.match(des_model, des_frame)
    # Sort them in the order of their distance
    matches = sorted(matches, key=lambda x: x.distance)

    if len(matches) > MIN_MATCHES:
        # draw first 15 matches.
        cap = cv2.drawMatches(model, kp_model, cap, kp_frame,
                            matches[:MIN_MATCHES], 0, flags=2)
        # show result
        cv2.imshow('frame', cap)
        cv2.waitKey(0)
    else:
        print( "Not enough matches have been found - %d/%d" % (len(matches),
                                                            MIN_MATCHES))

"""
We are not allowed to use SURF or SIFT due to licenses in latest OpenCV.
They are Patented!

Therefore the developers created ORB. And it seems to be working fine!
"""

if __name__ == "__main__":
    door_image_path = os.path.dirname(os.path.realpath(__file__))+"/../../../Images/door.png"
    example_image_path = os.path.dirname(os.path.realpath(__file__))+"/../../../Images/example.png"


    img1 = cv2.imread(example_image_path,0)
    img2 = cv2.imread(door_image_path,0)
    feature_detect(img2)
    feature_detect(img1)
    #fast_feature_detect(img2)
    #fast_feature_detect(img1)
    #fast_feature_match(img1,img2)
    feature_match(img1,img2)