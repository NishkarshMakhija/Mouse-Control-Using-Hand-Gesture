from Camera import Camera
from ObjectTracker import ObjectTracker
from Util import Util
import pyautogui
import cv2
import numpy as np

class MouseMovement(ObjectTracker.objectListener):
    
    __MouseMovementId = 1
    __MouseClickId = 2
    __RightClickId = 3
    
    def __init__(self,config):
    
        self.__config = config
        
        #Intiate Camera
        self.__camera = Camera.getInstance()
        
        #Display Camera as per Configuration. (Configuration value is True/False)
        self.__camera.showVideo(self.__config.getData("camera"))
        self.__camera.start()
        
        self.__movement = True #Indicates whether to move mouse or not
        self.__leftClick = False #To be used by leftMouseClick
        self.__rightClick = False #To be used by rightMouseClick
        
        self.__initiateObjectTrackers()
        
        #To be used to store Masked Frame of different Objects
        self.__maskedFrames = {}
        self.__displayMask = self.__config.getData("mask")
        
        #If mask has to displayed... Make a window for it.
        if self.__displayMask:
            cv2.namedWindow("Mask")
    
    def __initiateObjectTrackers(self):
        #This method intializes all the Object Trackers according to its need
        
        self.movementTracker = ObjectTracker()
        self.movementTracker.setMask(Util.getMaskFromColor(self.__config.getData("movementColor")))
        self.movementTracker.startTracking()
        self.movementTracker.setObjectListener(self,MouseMovement.__MouseMovementId)
        self.movementTracker.setDisplayTrack(False)
        
        
        if self.__config.getData("leftMouseClick"):
            self.leftClickTracker = ObjectTracker()
            self.leftClickTracker.setMask(Util.getMaskFromColor(self.__config.getData("leftMouseColor")))
            self.leftClickTracker.startTracking()
            self.leftClickTracker.setObjectListener(self,MouseMovement.__MouseClickId)
            self.leftClickTracker.setDisplayTrack(False)
           
        if self.__config.getData("rightMouseClick"):
            self.rightClickTracker = ObjectTracker()
            self.rightClickTracker.setMask(Util.getMaskFromColor(self.__config.getData("rightMouseColor")))
            self.rightClickTracker.startTracking()
            self.rightClickTracker.setObjectListener(self,MouseMovement.__RightClickId)
            self.rightClickTracker.setDisplayTrack(False)
        
        
    #Implemeted Methods of ObjectTracker.objectListener
    def objectEntered(self,resultId):
        print(resultId,"Entered")
        if resultId == MouseMovement.__MouseClickId:
            self.__leftClick = True #Indicates Left Click Object Entered
        
        elif resultId == MouseMovement.__RightClickId:
            self.__rightClick = True #Indicates Right Click Object Entered
           
        print(self.__movement)
        if self.__leftClick or self.__rightClick:
            self.__movement = False #Stops the movement of Cursor
    
    #Implemeted Methods of ObjectTracker.objectListener
    def objectExisted(self,resultId):
        #print(resultId,"Existed")
        if resultId == MouseMovement.__RightClickId:
            #Click The Left Click
            self.__pressRightClick()
            self.__rightClick = False
            
        elif resultId == MouseMovement.__MouseClickId:
            #Click The Left Click
            self.__pressLeftClick()
            self.__leftClick = False
            
        if self.__leftClick==False and self.__rightClick==False:
            self.__movement = True #Begins the movement of Cursor 
         
        
    #Implemeted Methods of ObjectTracker.objectListener
    def objectMoved(self,resultId,dX,dY):
        #print(resultId,dX,dY)
        if resultId == MouseMovement.__MouseMovementId:
            self.__moveMouse(dX,dY)
    
    #Implemeted Methods of ObjectTracker.objectListener    
    def maskedFrame(self,resultId,maskFrame):
        #This method will display all the masked Frame of all Objects of different Color
        #To show all simulatneously, it is bitwising OR to all masked Frame.
        if self.__displayMask:
            self.__maskedFrames[resultId] = maskFrame
            
            fin = maskFrame
            for i in self.__maskedFrames:
                c = self.__maskedFrames[i]
                fin = cv2.bitwise_or(fin,c,mask= None)
                
            cv2.imshow("Mask",fin)
        
    def __moveMouse(self,dX,dY):
        #This method will move the relative to current position
        #print("Mouse Moving",self.__movement,dX,dY)
        if self.__movement == False:
            return
        #if np.abs(dX)<5 and np.abs(dY)<5:
         #   return
        pyautogui.FAILSAFE = False
        dX *= -1
        dY *= -1
    
        size = self.__camera.getFrameSize()
        if size!=None:
            (height, width) = size
            asR = pyautogui.size()[1]//700
        
            dX = dX // asR
            dY = dY // asR
            
                    
        pyautogui.moveRel(dX,dY,duration=0.1)
        #pyautogui.moveRel(-5,0,duration=0.1)
        
        cv2.putText(self.__camera.getFrame(),"dx: {}, dy: {}".format(dX, dY),(10,500-10),cv2.FONT_HERSHEY_SIMPLEX,0.35,(255,0,0),1)
        
    def __pressLeftClick(self):
        #This method will click Left mouse Button
        
        curPos = pyautogui.position() 
        pyautogui.click(curPos.x,curPos.y)
        
        
    def __pressRightClick(self):
        #This method will click Right mouse Button
        
        curPos = pyautogui.position()
        pyautogui.click(curPos.x,curPos.y,button="right")
        
        
    def stop(self):
        self.__camera.stop()
        
'''
def main():
    mm = MouseMovement()

if __name__ == "__main__":
    main()
'''