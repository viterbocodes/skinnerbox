#!/usr/bin/python

# Standard imports
import cv2
import numpy as np;

# Read image
im = cv2.imread("images/rat4.jpg", cv2.IMREAD_COLOR)
hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, (5, 75, 25), (25, 255, 255))
#im = cv2.subtract(255, im)
imask = mask>0
orange = np.zeros_like(im, np.uint8)
orange[imask] = im[imask]

#color filter

# Define lower and uppper limits of what we call "brown"
brown_lo=np.array([10,0,0])
brown_hi=np.array([20,255,255])

# Mask image to only select browns
mask=cv2.inRange(hsv,brown_lo,brown_hi)

# Change image to .. where we found brown
#im[mask>0]=(0,0,0)


y=80
x=0
h=255
w=255
im = im[y:y+h, x:x+w]




# Setup SimpleBlobDetector parameters.
params = cv2.SimpleBlobDetector_Params()
# Set Area filtering parameters
params.filterByArea = True
params.minArea = 300

params.filterByColor = False
params.blobColor = 255
 
# Set Circularity filtering parameters
params.filterByCircularity = False
params.minCircularity = 0.2
 
# Set Convexity filtering parameters
params.filterByConvexity = True
params.minConvexity = 0.4
     
# Set inertia filtering parameters
params.filterByInertia = True
params.minInertiaRatio = 0.25


 

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