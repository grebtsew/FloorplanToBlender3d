"""
Feature Matching 

While studing and developing ar i thought this method could be used to find windows and doors

https://bitesofcode.wordpress.com/2017/09/12/augmented-reality-with-python-and-opencv-part-1/
"""
import os
import cv2
import numpy as np
from matplotlib import pyplot as plt

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
       
        list_kp1 = [kp_model[mat.queryIdx].pt for mat in matches[:MIN_MATCHES]] 
        list_kp2 = [kp_frame[mat.trainIdx].pt for mat in matches[:MIN_MATCHES]]
        
       
        print(list_kp1, list_kp2)

       


        #img2 = cv2.circle(img2,(int(x1),int(y1)), 5, (0,255,0), 1)
        #cap = cv2.circle(cap,(int(x2),int(y2)), 5, (0,255,0), 1)

        h,w = img1.shape[:2]
        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
        dst = cv2.perspectiveTransform(pts,M)
        perspectiveM = cv2.getPerspectiveTransform(np.float32(dst),pts)
        cap = cv2.warpPerspective(img2,perspectiveM,(w,h))

        cap = cv2.drawMatches(model, kp_model, cap, kp_frame,
                            matches[:MIN_MATCHES], 0, flags=2)
        # show result
        cv2.imshow('frame', cap)
        cv2.waitKey(0)
    else:
        print( "Not enough matches have been found - %d/%d" % (len(matches),
                                                            MIN_MATCHES))


def pair_cluster_points(matches, MIN_MATCHES):
    for mat in matches[:MIN_MATCHES]:

            # Get the matching keypoints for each of the images
            img1_idx = mat.queryIdx
            img2_idx = mat.trainIdx

            # x - columns
            # y - rows
            (x1,y1) = kp_model[img1_idx].pt
            (x2,y2) = kp_frame[img2_idx].pt
    pass


if __name__ == "__main__":
    door_image_path = os.path.dirname(os.path.realpath(__file__))+"/../../../Images/door.png"
    example_image_path = os.path.dirname(os.path.realpath(__file__))+"/../../../Images/example.png"


    img1 = cv2.imread(example_image_path,0)
    img2 = cv2.imread(door_image_path,0)
    feature_detect(img2)
    feature_detect(img1)

    feature_match(img1,img2)