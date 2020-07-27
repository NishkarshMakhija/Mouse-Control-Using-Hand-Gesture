import cv2
import imutils
import threading
from abc import ABC,abstractmethod
import time
import numpy as np

'''
    Class to open webcam and get video from it in seperate thread
    To use it:
        get instance of it using method "getInstance()"
        and implement "Camera.frameChangeListener" to get new Frames
'''

class Camera:

    _sInstance = None #Static variables to hold the single Instance
    _frameListenerId = 0 #Sattic variable to keepcount of number of class listining to it

    def __init__(self):
        #Intitializtion of class
        self.__camera = None
        self.__Listener = {}
        self.__frame = None
        self.__showVideo = False
        self.__threadRunning = False
    
    @staticmethod
    def getInstance():
        #Return instance of class
        if Camera._sInstance == None:
            Camera._sInstance = Camera()
        
        return Camera._sInstance
    
    def start(self):
        if self.__threadRunning:
            raise Exception("Camera is already Recording")
        
        if self.__showVideo:
            cv2.namedWindow("Camera")
            
        #Running method "recordVideo" in seperate thread
        self.__threadRunning = True
        self.__t1 = threading.Thread(target=self.__recordVideo,args=())
        self.__t1.start()
        
    def __recordVideo(self):
        '''
            This method records the video in sperate thread
            Resize frame to width = 700
            and creates its HSV
        '''
        
        # get the reference to the webcam
        
        self.__camera = cv2.VideoCapture(0)
        
        # allow the camera or video file to warm up
        time.sleep(1.0)
        
        #keep looping until interrupted
        while(self.__threadRunning):
            # get the current frame
            (grabbed, frame) = self.__camera.read()
            
            # resize the frame
            frame = imutils.resize(frame, width=700)

            # flip the frame so that it is not the mirror view
            frame = cv2.flip(frame, 1)
            
            #Create HSV of Frame
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
            self.__frame = frame
            
            self.__updateFrameChange(frame,hsv)
            
            if self.__showVideo:
                self.__displayFrame()
                #cv2.imshow("HSV",hsv)
                
        self.__camera.release()
            
    def __updateFrameChange(self,frame,hsv):
        #This method will let all the listener of this class that new frame is captured.
        for i in self.__Listener:
            if self.__Listener[i] != None:
                self.__Listener[i].onframeChange(frame,hsv)
            else:
                #If listener is none
                #Remove it from directory of listeners
                del self.__Listener[i]
            
    def addFrameChangeListener(self,frameChangeListener):
        #This method is used by Listener classes to register themselves
        #It will return them registration id also
        #registration id will be used to deregister Listener
        Camera._frameListenerId +=1
        self.__Listener[Camera._frameListenerId] = frameChangeListener
        return Camera._frameListenerId
        
    def removeFrameChangeListener(self,frameListenerId):
        #This method is used to deregister listener
        if frameListenerId in self.__Listener:
            del self.__Listener[frameListenerId]
            return True
        return False
        
    def getFrameSize(self):
        if isinstance(self.__frame,np.ndarray):
            return self.__frame.shape[:2] 
        return None
        
    def getFrame(self):
        return self.__frame
        
    def showVideo(self,showVideo):
        if type(showVideo) == bool:
            self.__showVideo = showVideo
        else:
            raise Exception("showVideo should be boolean Type")
            
    def __displayFrame(self):
        cv2.imshow("Camera",self.__frame)
        key = cv2.waitKey(1) & 0xFF
        #if key == ord("q"):
            #sys.exit()
    
    def stop(self):
        #It will stop the running Thread
        self.__threadRunning = False
        time.sleep(0.5) #Let Camera Stop Recording
        
        #Remove all the listeneres
        self.__Listener = {}
        #Destroy all the windows
        cv2.destroyAllWindows()
        
        
        
            
    #Interface to be used by listener to listen to frame change
    class frameChangeListener(ABC):
        @abstractmethod
        def onframeChange(self,frame,hsv):
            pass
    