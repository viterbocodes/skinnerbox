import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time 
import serial
import numpy as np
from datetime import datetime
import tkinter.ttk as ttk
import tkinter as tk
import serial.tools.list_ports
from tkinter.messagebox import showinfo
import json

class Arduino:
    def __init__(self, port):
        self.dev = serial.Serial(port, baudrate=9600)
        time.sleep(1)

    def query_old(self, message):
        time.sleep(1)
        self.dev.write(message.encode('ascii'))
        line = self.dev.readline().decode('ascii').strip()
        return line
    
    def send(self, message):
        time.sleep(1)
        self.dev.write(message.encode('ascii'))
        
    def query(self):
        #time.sleep(1)
        message="q,0,0"
        self.dev.write(message.encode('ascii'))
        line = self.dev.readline().decode('ascii').strip()
        return line


class App:
     def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source
        self.recording = 0;
        self.start_time = time.time()
        self.ard = None
        self.data= {0:[0,'start','start']}
 
         # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)
        
        frame_width = int(self.vid.get_width())
        frame_height = int(self.vid.get_height())
        
        #create output video
        # Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
        self.out = cv2.VideoWriter('videos/output.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))
        
 
        # Create a canvas that can fit the above video souCrce size
        self.canvas = tkinter.Canvas(window, width = 960 , height = 480)
        self.canvas.pack()
 
         # Button that lets the user take a snapshot
        self.btn_snapshot=tkinter.Button(window, text="Snapshot", width=50, command=self.snapshot)
        self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=True)
        
        # Button that starts Recording
        self.btn_snapshot=tkinter.Button(window, text="Record", width=50, command=self.record)
        self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=True)
        
        self.motion = tk.IntVar()
        self.cap_motion = tk.Checkbutton(window, text='Capture Motion',variable=self.motion, onvalue=1, offvalue=0, command=self.do_motion)
        self.cap_motion.pack()
        
        # label
        label = ttk.Label(text="Please select a port:")
        label.pack()
        # create a combobox
        port_list = self.serial_ports()
        list1 = tk.StringVar(value=port_list)
        listbox = tk.Listbox(window,listvariable=list1, height=2)  
        listbox.pack()  
        listbox.bind("<<ListboxSelect>>", self.port_change)
        # Create a label widget
        self.feeback=ttk.Label(window, text="")
        self.feeback.pack(pady= 30)
                        
       
         # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()

        self.window.mainloop()
        
        
     def do_motion(self):
        print("motion")
    
     def serial_ports():    
        return  [p.device for p in serial.tools.list_ports.comports()]

    
     def record(self):
          if (self.ard!= None):
            self.start_time = time.time()
            self.recording=1;
            self.feeback.configure(text="Running")
          else:
            self.feeback.configure(text="Arduino Not Connected")
          
     def select_lang():
         return 1
     
     def item_selected(self, event=None):
            """Set active_item to the combobox option selected by the user"""
            selected_name = self.combo_box.get()
     
     
     def port_change(self,event):
        selection = event.widget.curselection()
        if selection and self.recording==0:
            index = selection[0]
            data = event.widget.get(index)
            if self.connect_ard(data):
                self.feeback.configure(text="Arduino Connected")
        else:
            #label.configure(text="")
            a=1
    #end mission_selected
    # bind the selected value changes
     def option_selected(event):
        """ handle the month changed event """
        showinfo(
            title='Result',
            message=f'You selected {3}')
          
     def stop(self):
          self.out.release()
          self.recording=0;
     def serial_ports(self):    
        return [p.device for p in serial.tools.list_ports.comports()]
        #return serial.tools.list_ports.comports()
        
     def exp_logic(self):  
        #### conditional long to send to decide what to send  and when #######
        ### action,action pin, duration is to be set
        ### actions= d = digital write, q=get data from
        self.ard.send("d,13,5")
        #### conditional long to send to decide what to send and when #######  
        return True;

     def on_select(self,event=None):
        # get selection from event    
        print("event.widget:", event.widget.get())

        # or get selection directly from combobox
        print("comboboxes: ", self.cb.get())

     def connect_ard(self,port):
         self.ard =  Arduino(port)
         return self.ard
    
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

        #im_with_keypoints = cv2.drawKeypoints(frame, keypoints, np.array([]), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        # Show blobs
        #cv2.imshow("Keypoints", im_with_keypoints)
        
        return keypoints
     def check_ard(self):
        data =  self.ard.query()
        if (len(data)>5):
            Dict = json.load(data);
            return Dict
        else:
            return None  
     def snapshot(self):
         # Get a frame from the video source
        ret, frame = self.vid.get_frame()
 
        if ret:
             cv2.imwrite("images/frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

     def update(self):
         # Get a frame from the video source
         ret, frame = self.vid.get_frame()
 
         if ret:
            if 1==1:
                # Put current DateTime on each frame
                font = cv2.FONT_HERSHEY_PLAIN
                elapsed_time = time.time() - self.start_time
                
                cv2.putText(frame, str(time.strftime("%H:%M:%S", time.gmtime(elapsed_time))), (20, 40),
                font, 2, (255, 255, 255), 2, cv2.LINE_AA)
            if (int(elapsed_time) % 2 == 0 and self.ard != None):
                data=self.check_ard()
                if data:
                    now = round((time.time() - self.timer), 2)
                    result = '{0:02.0f}:{1:02.0f}'.format(*divmod(now * 60, 60))
                    for key,value in dict:
                        self.data[now] = [now,'event',value]
                        
            if (int(elapsed_time) % 3 == 0 and self.recording==1 and self.motion.get()==1):
                #self.active_key=10;
                self.exp_logic();
                keypoints = self.get_rat_loc(frame)
                self.keypoints = keypoints
                if keypoints != None and len(keypoints)>0:
                    self.keypoints = keypoints
                    frame = cv2.drawKeypoints(frame, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW) 
            if self.recording:
                self.out.write(frame) 
 
         self.window.after(self.delay, self.update)
 
 
class MyVideoCapture:
    def __init__(self, video_source=0):
         # Open the video source
         self.vid = cv2.VideoCapture(video_source)
         if not self.vid.isOpened():
             raise ValueError("Unable to open video source", video_source) 
         # Get video source width and height
         # Set properties. Each returns === True on success (i.e. correct resolution)
         self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
         self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
         self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
         self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_width(self):
         return self.width
     
    def get_height(self):
        return self.height
     
    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                 # Return a boolean success flag and the current frame converted to BGR
                 return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
             return (ret, None)
 
     # Release the video source when the object is destroyed
    def __del__(self):
         if self.vid.isOpened():
             self.vid.release()
             
 
# Create a window and pass it to the Application object
App(tkinter.Tk(), "Tkinter and OpenCV")