# imports
import cv2
import numpy as np;

# Read image
img = cv2.imread('images/rat.jpeg', cv2.IMREAD_GRAYSCALE)

# Set up the blob detector.
detector = cv2.SimpleBlobDetector()

# Detect blobs from the image.
keypoints = detector.detect(img)

# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS - This method draws detected blobs as red circles and ensures that the size of the circle corresponds to the size of the blob.
blobs = cv2.drawKeypoints(img, keypoints, cv2.blank, (0,255,255), cv2.DRAW_MATCHES_FLAGS_DEFAULT)

# Show keypoints
cv2.imshow('Blobs',blobs)
cv2.waitKey(0)