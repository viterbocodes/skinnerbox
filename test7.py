#!/usr/bin/python

# Standard imports
import cv2
import numpy as np;

# Read image
im = cv2.imread("images/rat.jpeg", cv2.IMREAD_GRAYSCALE)

#im = cv2.subtract(255, im)


# Setup SimpleBlobDetector parameters.
params = cv2.SimpleBlobDetector_Params()
# Set Area filtering parameters
params.filterByArea = True
params.minArea = 100

params.filterByColor = True
params.blobColor = 255
 
# Set Circularity filtering parameters
params.filterByCircularity = True
params.minCircularity = 0.2
 
# Set Convexity filtering parameters
params.filterByConvexity = True
params.minConvexity = 0.4
     
# Set inertia filtering parameters
params.filterByInertia = True
params.minInertiaRatio = 0.3

params.filterByArea = True
params.minArea = 300
 

# Create a detector with the parameters
ver = (cv2.__version__).split('.')
if int(ver[0]) < 3:
    detector = cv2.SimpleBlobDetector(params)
else:
    detector = cv2.SimpleBlobDetector_create(params)

# Detect blobs.
keypoints = detector.detect(im)

# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures
# the size of the circle corresponds to the size of blob

im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# Show blobs
cv2.imshow("Keypoints", im_with_keypoints)
cv2.waitKey(0)