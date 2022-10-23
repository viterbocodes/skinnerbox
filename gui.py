#from asyncio.windows_events import NULL
import tkinter as tk
import cv2
from pyfirmata import Arduino, util
import time
import gui
import numpy as np
import csv





class Skinner(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.timer = time.time()
        self.writer=None;
        self.exp=None;
        self.get_location = 0;
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
    def __draw_label(self,img, text, pos, bg_color):
        font_face = cv2.FONT_HERSHEY_SIMPLEX
        scale = 0.4
        color = (0, 0, 0)
        thickness = cv2.FILLED
        margin = 2
        txt_size = cv2.getTextSize(text, font_face, scale, thickness)

        end_x = pos[0] + txt_size[0][0] + margin
        end_y = pos[1] - txt_size[0][1] - margin

        cv2.rectangle(img, pos, (end_x, end_y), bg_color, thickness)
        cv2.putText(img, text, pos, font_face, scale, color, 1, cv2.LINE_AA)
        return img
    def on_end(self):
        # close the already opened camera
        self.vid_capture.release()
        # close the already opened file
        self.output.release()
        # close the window and de-allocate any associated memory usage
        cv2.destroyAllWindows()
        self.board.analog[0].disable_reporting()
    def create_or_edit_csv_file(file,frames):
        """ This method creates a CSV file, if it doesnt exist, and writes to it, if it does exist it 
        overwrites all information in it. The information in each row of the CSV file follows as: x coordinate, y coordinate, time at current frame, and frame number. There may exist multiple blobs for a given frame.
        """
        with open (file, 'w+') as csv_file:
            file_stream_writer = csv.writer(csv_file)
            for frame in frames:
                for key_point in frame[:-2]:
                    time_at_current_frame = frame[-2]
                    frame_number_at_current_frame = frame[-1]
                    x_coordinate = key_point.pt[0]
                    y_coordinate = key_point.pt[1]
                    file_stream_writer.writerow(["{} {} {} {}".format(x_coordinate, y_coordinate, 
                                                time_at_current_frame, frame_number_at_current_frame)])

    def check_ard(self):
        #it = util.Iterator(self.board)
        #it.start()
        #self.board.analog[0].enable_reporting()
        #print ("Read Start")
        #print(self.board.analog[0].read())
        #time.sleep(1)
        #print(self.board.analog[1].read())
        time.sleep(1)
        #print(self.board.analog[2].read())
        #result = MyDialog(self).show()
        #self.label.configure(text="your result: %s" % result)
        #board = Arduino('/dev/ttyACM1')
    def ard_action(self):
        #self.board.digital[13].write(1)
        time.sleep(1)
        
    def get_rat_loc(self,frame,min_x,min_y):
        frame = cv2.GaussianBlur(frame, (11, 11), 0)
        frame = cv2.erode(frame, None, iterations=2)
        frame = cv2.dilate(frame, None, iterations=2)
        mask =  cv2.inRange(frame, self.miceLower, self.miceUpper)
        params = cv2.SimpleBlobDetector_Params()
        #THRESHOLDS
        params.filterByConvexity = True
        params.minConvexity = 0.7
        params.minThreshold = 200
        params.maxThreshold = 255
        params.filterByArea = True
        params.minArea = 300
        
        #X AND Y COORDINATES STORED IN ARRAY
        key_points = detector.detect(mask)
        detector = cv2.SimpleBlobDetector_create(params)
        keyPoints = detector.detect(frame) #list of blobs keypoints
        
    def do_action(self,action,sleepTime):
        #self.board.digital[action].write(1)
        time.sleep(sleepTime)
        #self.board.digital[action].write(0)
        
    def on_start(self):
        #board = Arduino('/dev/ttyACM1')
        #board = Arduino('COM4') # Change to your port
        '''   for x in range(6):
                    board.digital[9].write(1)
                    time.sleep(0.5)
                    board.digital[9].write(0)
                    time.sleep(0.5) '''   
        starttime = time.time()
        exp_name = self.exp_name.get()
        with open( 'data/' + exp_name + '.csv', 'w+', newline='') as file:
            now = round((time.time() - self.timer), 2)
            self.writer = csv.writer(file)
            self.writer.writerow([now,"start","start" , exp_name])
        while(True):
            # Check for event
            data=self.check_ard()
            now = round((time.time() - self.timer), 2)
            if data:
                with open( 'data/' + exp_name + '.csv', 'w+', newline='') as file:
                    self.writer = csv.writer(file)
                    self.writer.writerow([now,"action", data, exp_name])
                self.action_active=30
            # Capture each frame of webcam video
            ret,frame = self.vid_capture.read()
            lab=now;
            ## do action if called for for n seconds
            for key,value in self.actions.items(): 
                if (int(key)>int(now) and value[1]!=0): 
                    self.actions[key] = self.do_action(value[0],value[1])
            if (self.action_active>0):
                lab=str(now + "::" + data)
                self.action_active=self.action_active-1
            img=self.__draw_label(frame, "lab", (20,20), (255,0,0))
            if self.get_location and int(now) % 4 == 0:
                keypoints = self.get_rat_loc(frame)
                im_with_keypoints = cv2.drawKeypoints(img, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
                for i in keypoints:
                    x = keypoints[i].pt[0] #i is the index of the blob you want to get the position
                    y = keypoints[i].pt[1]
                    with open( 'data/' + exp_name + '.csv', 'w+', newline='') as file:
                        self.writer = csv.writer(file)
                        self.writer.writerow([now,"location", keypoints, exp_name])
            cv2.imshow(self.exp, img) 
            self.output.write(img)
            # Close and break the loop after pressing "x" key
            if cv2.waitKey(1) &0XFF == ord('x'):
                break
            
    