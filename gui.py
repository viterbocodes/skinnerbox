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



class Arduino:
    def __init__(self, port):
        self.dev = serial.Serial(port, baudrate=19200)
        time.sleep(1)

    def query(self, message):
        self.dev.write(message.encode('ascii'))
        line = self.dev.readline().decode('ascii').strip()
        return line
    

class Skinner(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.timer = time.time()
        self.writer=None;
        self.data= {0:[0,'start','start']}
        self.exp=None;
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
    def check_ard(self,myValues = [], *args):
        Dict = json.loadsself.ard.query("sens\n")
        return Dict
    def ard_action(self):
        #self.board.digital[13].write(1)
        time.sleep(1)
        
    def get_rat_loc(self,frame):
        frame = cv2.GaussianBlur(frame, (11, 11), 0)
        frame = cv2.erode(frame, None, iterations=2)
        frame = cv2.dilate(frame, None, iterations=2)
        #mask =  cv2.inRange(frame, self.miceLower, self.miceUpper)
        params = cv2.SimpleBlobDetector_Params()
        #THRESHOLDS
        params.filterByConvexity = True
        params.minConvexity = 0.7
        params.minThreshold = 200
        params.maxThreshold = 255
        params.filterByArea = True
        params.minArea = 300
        
        #X AND Y COORDINATES STORED IN ARRAY
        #key_points = detector.detect(frame)
        detector = cv2.SimpleBlobDetector_create(params)
        keyPoints = detector.detect(frame) #list of blobs keypoints
        return keyPoints
        
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
            for key,value in self.actions.items(): 
                if (int(key)>int(now) and value!=None and value[1]!=0): 
                    self.actions[key] = self.do_action(value[0],value[1])
            if (self.action_active>0):
                lab=str(now) + "::" + str(data)
                self.action_active=self.action_active-1
            img=self.__draw_label(frame, lab, (30,30), (130,0,0))
            if self.get_location and i % 8 == 0:
                keypoints = self.get_rat_loc(frame)
                if keypoints != None:
                    img = cv2.drawKeypoints(img, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
                for i in keypoints:
                    x = keypoints[i].pt[0] #i is the index of the blob you want to get the position
                    y = keypoints[i].pt[1]
                    self.data[now] = [now,'location',tuple(x,y)]
            cv2.imshow(self.exp, img) 
            self.output.write(img)
            # Close and break the loop after pressing "x" key
            if cv2.waitKey(1) &0XFF == ord('x'):
                break
            i = i + 1
            