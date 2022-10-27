
import cv2
import numpy as np
import sys

class Skinner():
    def __init__(self):
    
        # Create a VideoCapture object
        self.cap = cv2.VideoCapture(0)

        # Check if camera opened successfully
        if (self.cap.isOpened() == False): 
            sys.exit("Unable to read camera feed")
        # Default resolutions of the frame are obtained.The default resolutions are system dependent.
        # We convert the resolutions from float to integer.
        frame_width = int(self.cap.get(3))
        frame_height = int(self.cap.get(4))
        
        # Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
        self.out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
    
    def stop(self):
         # When everything done, release the video capture and video write objects
        self.cap.release()
        self.out.release()
        # Closes all the frames
        cv2.destroyAllWindows()
    
    def start(self):  
        while(True):
            ret, frame = self.cap.read()
            if ret == True: 
                # Write the frame into the file 'output.avi'
                self.out.write(frame)          
                # Display the resulting frame    
                cv2.imshow('frame',frame)           
                # Press Q on keyboard to stop recording
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.stop()
                    break
            # Break the loop
            else:
                self.stop()
                break 
            
                
         

 
p = Skinner()
p.start()
