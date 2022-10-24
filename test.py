import cv2
import numpy as np

frame = cv2.imread("images/rat7.jpg")
#TIME AND FRAME NUMBER
frame = cv2.GaussianBlur(frame, (11, 11), 0)
frame = cv2.erode(frame, None, iterations=2)
frame = cv2.dilate(frame, None, iterations=2)
params = cv2.SimpleBlobDetector_Params()

#THRESHOLDS
params.filterByConvexity = True
params.minConvexity = 0.7
params.minThreshold = 200
params.maxThreshold = 255
params.filterByArea = True
params.minArea = 300

detector = cv2.SimpleBlobDetector_create(params)

#X AND Y COORDINATES STORED IN ARRAY
key_points = detector.detect(frame)

#DRAWS KEY POINTS ON EACH INDIVIDUAL FRAME
image_with_keypoints = cv2.drawKeypoints(frame, key_points, np.array([]))
while True:
    cv2.imshow('image_with_keypoints', image_with_keypoints)
    if cv2.waitKey(1) & 0xFF == ord('q'):
            break