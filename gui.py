#from asyncio.windows_events import NULL
import tkinter as tk
import cv2
from pyfirmata import Arduino, util
import time
import gui
import numpy as np
import csv
import pandas as pd
import serial
import json


def exp_logic(self):  
    #### conditional long to send to decide what to send  and when #######
    ### action,action pin, duration is to be set
    ### actions= d = digital write, q=get data from
    send_val="d,13,5"
    #### conditional long to send to decide what to send and when #######  
    return send_val

class Arduino:
    def __init__(self, port):
        #self.dev = serial.Serial(port, baudrate=19200)
        time.sleep(1)

    def query(self, message):
        time.sleep(1)
        #self.dev.write(message.encode('ascii'))
        #line = self.dev.readline().decode('ascii').strip()
        #return line
    

class Skinner(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.timer = time.time()
        self.writer=None;
        self.data= {0:[0,'start','start']}
        self.exp=None;
        self.active_key=0;
        self.keypoints= None;
        self.get_location = 1;
        self.action_active=0;
        self.vid_capture = cv2.VideoCapture(0)
        self.vid_cod = cv2.VideoWriter_fourcc(*'XVID')
        self.output = cv2.VideoWriter("videos/cam_video.mp4", self.vid_cod, 20.0, (640,480))
        self.board=None;
        self.actions = {200: [2,3,0], 400: [5,3,0]}
        self.button_start = tk.Button(self, text="Start", command=self.on_start)
        self.button_end = tk.Button(self, text="End", command=self.on_end)
        self.exp_name = tk.Entry(self)
        label2 = tk.Label(self, text='Type your Number:')
        label2.config(font=('helvetica', 10))
        #canvas1.create_window(200, 100, window=label2)
        entry1 = tk.Entry(self) 
        self.label = tk.Label(self, width=80)
        self.label.pack(side="top", fill="x")
        self.button_start.pack(pady=20)
        self.button_end.pack(pady=20)
        self.exp_name.pack(pady=20)
        self.ard =  Arduino('COM4')
    def __draw_label(self,img, text, pos, bg_color):
        cv2.putText(img,str(text),pos, cv2.FONT_HERSHEY_SIMPLEX, 1, bg_color, 2, cv2.LINE_AA)
        return img
    def connect_ard(port):
        serial.Serial(port, baudrate=19200)
        time.sleep(1)
    def on_end(self):
        # close the already opened camera
        self.vid_capture.release()
        # close the already opened file
        self.output.release()
        # close the window and de-allocate any associated memory usage
        cv2.destroyAllWindows()
        self.board.analog[0].disable_reporting()
    def check_ard(self):
        send_val=exp_logic();
        Dict = json.load(self.ard.query(send_val));
        return Dict
    def ard_action(self):
        #self.board.digital[13].write(1)
        time.sleep(1)
        
    def get_rat_loc(self,frame):
        # Read image
        #im = cv2.imread("images/rat4.jpg", cv2.IMREAD_COLOR)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, (5, 75, 25), (25, 255, 255))
        #im = cv2.subtract(255, im)
        imask = mask>0
        orange = np.zeros_like(frame, np.uint8)
        orange[imask] = frame[imask]

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
        frame = frame[y:y+h, x:x+w]




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
        keypoints = detector.detect(frame)

        # Draw detected blobs as red circles.
        # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures
        # the size of the circle corresponds to the size of blob

        im_with_keypoints = cv2.drawKeypoints(frame, keypoints, np.array([]), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        # Show blobs
        #cv2.imshow("Keypoints", im_with_keypoints)
        return keypoints, im_with_keypoints
        
    def do_action(self,action,sleepTime):
        #self.board.digital[action].write(1)
        time.sleep(sleepTime)
        #self.board.digital[action].write(0)
    def save_data(self):
        with open('data/' + self.exp_name, 'w') as f:  # You will need 'wb' mode in Python 2.x
            w = csv.DictWriter(f, self.data.keys())
            w.writeheader()
            w.writerow(self.data)
    def on_start(self):
        exp_name = self.exp_name.get()   
        starttime = time.time()
        i = 0
        while(True):
            # Check for event
            data=self.check_ard()
            now = round((time.time() - self.timer), 2)
            if data:
                for key,value in dict:
                    self.data[now] = [now,'event',value]
            self.action_active=30
            # Capture each frame of webcam video
            ret,frame = self.vid_capture.read()
            lab=now;
            ## do action if called for for n seconds
            if i % 4 == 0:
                for key,value in self.actions.items(): 
                    if (int(key)>int(now) and value!=None and value[1]!=0): 
                        self.actions[key] = self.do_action(value[0],value[1])
            if (self.action_active>0):
                lab=str(now) + "::" + str(data)
                self.action_active=self.action_active-1
            img=self.__draw_label(frame, lab, (30,30), (130,0,0))
            if self.get_location and i % 10 == 0:
                self.active_key=10;
                keypoints = self.get_rat_loc(frame)
                self.keypoints = keypoints
                if keypoints != None and len(keypoints)>0:
                    self.keypoints = keypoints
                    print("keyed")
                    print(f"X: {keypoints[0].pt[0]} and Y: {keypoints[0].pt[1]}.")
                    img = cv2.drawKeypoints(img, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
                ii=0
                for j in keypoints:
                    x = keypoints[ii].pt[0] #i is the index of the blob you want to get the position
                    y = keypoints[ii].pt[1]
                    self.data[now] = [now,'location',x,y]
                    ii=ii+1;
            if self.keypoints is not None and len(keypoints)>0 and self.active_key>0:
                im_with_keypoints = cv2.drawKeypoints(img, keypoints, np.array([]), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
                print(f"X: {keypoints[0].pt[0]} and Y: {keypoints[0].pt[1]}.")
                self.active_key = self.active_key - 1
            cv2.imshow(self.exp, img) 
            self.output.write(img)
            # Close and break the loop after pressing "x" key
            if cv2.waitKey(1) &0XFF == ord('x'):
                break
            i = i + 1
            