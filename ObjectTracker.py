from Camera import Camera
from Util import Util
import cv2
from collections import deque
from abc import ABC,abstractmethod
import numpy as np
import sys

class ObjectTracker(Camera.frameChangeListener):

    def __init__(self):
        self.__pts = deque(maxlen = 32) #To store last 32 points(x,y) of object
        self.__objectListener = None
        self.__resultId = None
        self.__objectExist = False
        self.__displayTrack = False
        
    def setMask(self,listOfMasks):
        self.__listOfMasks = listOfMasks
        
    def startTracking(self):
        self.__camera = Camera.getInstance()
        self.__frameListenerId = self.__camera.addFrameChangeListener(self)
       
    def setDisplayTrack(self,displayTrack):
        self.__displayTrack = displayTrack
        
    def setObjectListener(self,objectListener,resultId):
        self.__objectListener = objectListener
        self.__resultId = resultId
        
    #This is the implemented method of Camera.frameChangeListener    
    def onframeChange(self,frame,hsv):
        #cv2.imshow("frame",frame)
        #cv2.imshow("hsv",hsv)
        #key = cv2.waitKey(1) & 0xFF
        
        self.__trackObject(frame,hsv)
        
    def __broadcastObjectChange(self,center,dX,dY):
        
        if self.__objectListener !=None:
            #Code to update ObjectEnter and ObjectExisted
            if center!= None and self.__objectExist == False:
                self.__objectExist = True
                self.__objectListener.objectEntered(self.__resultId)
            elif center == None and self.__objectExist == True:
                self.__objectExist = False
                self.__objectListener.objectExisted(self.__resultId)
                
            #Code to update Object Movement
            self.__objectListener.objectMoved(self.__resultId,dX,dY)
        
        
    def __trackObject(self,frame,hsv):
        res = self.__applyMask(frame,hsv)
        #Get maximum contour
        contours = self.__getContours(res)
        #get center of contour
        center = self.__getCenterOfContour(contours)
        
        #Code to track
        self.__pts.appendleft(center)
        direction = ""
        dX = 0
        dY = 0
        newFrame = frame.copy()
        for i in range(1,len(self.__pts)):
            if self.__pts[i-1] is None or self.__pts[i] is None:
                continue
                
            if len(self.__pts)>=10 and i==1 and self.__pts[-10] is not None:
                dX = self.__pts[-10][0] - self.__pts[i][0]
                dY = self.__pts[-10][1] - self.__pts[i][1]
                (dirX, dirY) = ("", "")
            
                #For displaying direction if needed.
                if np.abs(dX) > 20:
                    dirX = "West" if np.sign(dX) == 1 else "East"
                
                # ensure there is significant movement in the
                # y-direction
                if np.abs(dY) > 20:
                    dirY = "North" if np.sign(dY) == 1 else "South"
                    
                # handle when both directions are non-empty
                if dirX != "" and dirY != "":
                    direction = "{}-{}".format(dirY, dirX)
                
                # otherwise, only one direction is non-empty
                else:
                    direction = dirX if dirX != "" else dirY
              
            if self.__displayTrack:
                thickness = int(np.sqrt(32 / float(i + 1)) * 2.5)
                newFrame = cv2.line(frame, self.__pts[i - 1],  self.__pts[i], (0, 255, 255), thickness)
            
        #Broadcase change to Listeners
        self.__broadcastObjectChange(center,dX,dY)
        
        if self.__displayTrack:
            cv2.putText(newFrame, direction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
            0.65, (0, 0, 255), 3)
            cv2.putText(newFrame, "dx: {}, dy: {}".format(dX, dY),
            (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
            0.35, (0, 0, 255), 1)
            
            self.__display(newFrame,contours,center,res)
            
    #Used for debugging Purpose only to display mask of only thi particular Object Tracker
    def __display(self,frame,contours,center,maskFrame):
        if center!=None:
            frame = self.__drawCountours(frame,contours,center)
        
        cv2.imshow(str(self.__resultId),frame)
        cv2.imshow("res",maskFrame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            sys.exit()
        
        
    def __applyMask(self,frame,hsv):
        '''
            It will apply all the mask 
            and return after doing Bitwise-AND with original image
        '''
        lowerColor = self.__listOfMasks[0]["lower"]
        upperColor = self.__listOfMasks[0]["upper"]
        mask = cv2.inRange(hsv, lowerColor, upperColor)
        for color in self.__listOfMasks[1:]:
            lowerColor = color["lower"]
            upperColor = color["upper"]
            mask1 = cv2.inRange(hsv, lowerColor, upperColor)
            mask = mask + mask1
        
        # Bitwise-AND mask and original image
        maskFrame = cv2.bitwise_and(frame,frame, mask= mask)
        
        if self.__objectListener != None:
            self.__objectListener.maskedFrame(self.__resultId,maskFrame)
        return maskFrame
        
    def __getContours(self,maskedFrame):
        '''
            Find the contours
            Return Maximum Size contour(Area wise)
        '''
        #Convert to grayscale and blur it
        gray = cv2.cvtColor(maskedFrame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)
        
        # get the contours in the Frame
        (contours, _) = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if len(contours) == 0:
            #No Contours Found
            return None
        else:
            # based on contour area, get the maximum contour area
            segmented = max(contours, key=cv2.contourArea)
            return segmented
        
    def __getCenterOfContour(self,contours):
        '''
            It will return the center of contour if it's area is greater than 150
        '''
        try:
            area = cv2.contourArea(contours)
        except:
            area = 0
        
        if area<200:
            return None
           
        '''
        if isinstance(contours,np.ndarray):
            print("Area=",area,len(contours))
        else:
            print("Area=",area,None)
        '''
        
        #Commpute Center of the contours
        M = cv2.moments(contours)
        try:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            return (cX,cY)
        except:
            return None
            
    def __drawCountours(self,frame,contours,center):
        frame = cv2.circle(frame, (center[0], center[1]), 5, (255, 255, 255), -1)
        frame = cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)
        return frame
            
            
    #Interface to be used by listener to listen to Object change
    class objectListener(ABC):
        @abstractmethod
        def objectEntered(self,resultId):
            pass
        def objectExisted(self,resultId):
            pass
        def objectMoved(self,resultId,dX,dY):
            pass
        def maskedFrame(self,resultId,maskFrame):
            pass
