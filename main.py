from tkinter import *
from tkinter import messagebox
from ToggleButton import ToggleButton
from ColorRadioButton import ColorRadioButton
from Config import Config
from MouseMovement import MouseMovement
from Camera import Camera
import traceback

#This class contains the code to create GUI.
#No real work is being done in this 
#It is only responsible for saving configuration and showing main window as per configuration

#It starts/stops the main application as per user command


class MainUI(Tk):
    def __init__(self):
        Tk.__init__(self)
        
        #Sets the main window
        self.resizable(width=False,height=False)
        self.geometry("350x410")
        self.title("Mouse Controller")
        icon = PhotoImage(file="icon.png")
        self.iconphoto(False,icon)
        self.protocol("WM_DELETE_WINDOW", self.stopApplication)
        
        #Main frame container
        self.container = Frame(self)
        self.container.pack(fill=BOTH,expand = True)
        
        try:
            #Intiates the config file
            self.config = Config()
        except Exception as e:
            self.showError(e)
            self.destroy()
        
        #Add main Content
        self.addMainContent()
        #Add Settings Frame
        self.addFrames()
        
        self.__mouseMovement = None
        
    def addMainContent(self):
        #This method setsup the main content of the window.
        #Anything above settings frame
        mainContent = Frame(self.container,pady=10)
        mainContent.pack(side=TOP,anchor="nw")
        
        mainLabel = Label(mainContent,text="Mouse Controller")
        mainLabel.grid(row=0,column=0,sticky="w",padx=20)
        
        self.mainButton = Button(mainContent,text="Start",padx=5,command=self.startStopApplication)
        self.mainButton.grid(row=0,column=1,sticky="e",padx=20)
        
    def addFrames(self):
        #This method adds the Settings Frame to the main Frame/Container
        settingsFrame = SettingsFrame(self,self.container,self.config)
        settingsFrame.pack(fill=X,expand=True)
        
    def showError(self,message):
        messagebox.showerror("Error",message);
        
    def showWarning(self,message):
        messagebox.showwarning("Warning",message)
       
    def startStopApplication(self):
        #Starts or Stops Mouse Movement Application
        #Toogles switch Text accordingly
        if self.mainButton["text"] == "Start":
            try:
                self.__mouseMovement = MouseMovement(self.config)
            except Exception as e:
                track = traceback.format_exc()
                print(track)
                self.showError(e)
            
            self.mainButton["text"] = "Stop"
        else:
            try:
                if self.__mouseMovement != None:
                    self.__mouseMovement.stop()
            except Exception as e:
                track = traceback.format_exc()
                print(track)
                self.showError(e)
                self.mainButton["text"] = "Stop"
            
            self.mainButton["text"] = "Start"
            
    def stopApplication(self):
        #This method Cleans before closing the main Application
        #Called when "Close" Button of Window is pressed
        try:
            if self.__mouseMovement != None:
                self.__mouseMovement.stop()
        except Exception as e:
            pass
        sys.exit()
        
class SettingsFrame(Frame):

    #This class is concerned with the working of Settings Frame
    
    def __init__(self,parent,container,config):
        Frame.__init__(self,container,padx=10,pady=10)
        self.config = config
        self.parent = parent
        
        mainLabel = Label(self,text="Settings",font=("",15))
        mainLabel.pack(anchor="w")
        
        self.createGeneralSettings()
        self.createColorSettings()
        self.changesButton()
    
    def createGeneralSettings(self):
        #This setups the General Settings
        generalFrame = LabelFrame(self,text="General",padx=10)
        generalFrame.pack(fill=X)
        self.generalFrame = generalFrame
        
        cameraLabel = Label(generalFrame,text="Camera")
        #cameraButton = ToggleButton(generalFrame,value=True,padx=5)
        self.cameraButton = ToggleButton(generalFrame,value=self.config.getData("camera"),padx=5)
        
        cameraLabel.grid(row=0,column=0,pady=2,sticky="w")
        self.cameraButton.grid(row=0,column=1,pady=2)
        
        maskLabel = Label(generalFrame,text="Mask")
        self.maskButton = ToggleButton(generalFrame,value=self.config.getData("mask"),padx=5)
        
        maskLabel.grid(row=1,column=0,pady=2,sticky="w")
        self.maskButton.grid(row=1,column=1,pady=2)
        
        leftMouseLabel = Label(generalFrame,text="Left Mouse Click")
        self.leftMouseButton = ToggleButton(generalFrame,value=self.config.getData("leftMouseClick"),padx=5)
        
        leftMouseLabel.grid(row=2,column=0,pady=2,sticky="w")
        self.leftMouseButton.grid(row=2,column=1,pady=2)
        
        rightMouseLabel = Label(generalFrame,text="Right Mouse Click")
        self.rightMouseButton = ToggleButton(generalFrame,value=self.config.getData("rightMouseClick"),padx=5)
        
        rightMouseLabel.grid(row=3,column=0,pady=2,sticky="w")
        self.rightMouseButton.grid(row=3,column=1,pady=2)
        
    def createColorSettings(self):
        #This setups the Color Settings
        colorFrame = LabelFrame(self,text="Colors",padx=10)
        colorFrame.pack(fill=X)
        self.colorFrame = colorFrame
        
        movementLabel = Label(colorFrame,text="Movement")
        self.movementColorButton = ColorRadioButton(colorFrame,self.config.getData("movementColor"))
        
        movementLabel.grid(row=0,column=0,pady=2,sticky="w")
        self.movementColorButton.grid(row=0,column=1,pady=2)
        
        leftMouseColorLabel = Label(colorFrame,text="Left Click")
        self.leftMouseColorButton = ColorRadioButton(colorFrame,self.config.getData("leftMouseColor"))
        
        leftMouseColorLabel.grid(row=1,column=0,pady=2,sticky="w")
        self.leftMouseColorButton.grid(row=1,column=1,pady=2)
        
        rightMouseColorLabel = Label(colorFrame,text="Right Click")
        self.rightMouseColorButton = ColorRadioButton(colorFrame,self.config.getData("rightMouseColor"))
        
        rightMouseColorLabel.grid(row=2,column=0,pady=2,sticky="w")
        self.rightMouseColorButton.grid(row=2,column=1,pady=2)
        
    def changesButton(self):
        #This method setups the settings button
        buttonFrame = Frame(self,pady=10)
        buttonFrame.pack(fill=X)
        self.buttonFrame = buttonFrame
        
        resetChanges = Button(buttonFrame,text="Reset To Default",padx=5,command=self.resetChanges)
        applyChanges = Button(buttonFrame,text="Apply",padx=5,command=self.applyChanges)
        cancelChanges = Button(buttonFrame,text="Cancel",padx=5,command=self.reloadUI)
        
        cancelChanges.pack(side=RIGHT)
        applyChanges.pack(side=RIGHT,padx=10)
        resetChanges.pack(side=RIGHT)
        
    def reloadUI(self):
        #Reloads the complete Settings Frame
        #Specially usefull when settings is changes.(Either Saved or Reset)
        self.generalFrame.destroy()
        self.colorFrame.destroy()
        self.buttonFrame.destroy()
        self.createGeneralSettings()
        self.createColorSettings()
        self.changesButton()
    
    def resetChanges(self):
        #Called when "Reset" Button is Pressed
        self.config.resetToDefault()
        self.reloadUI()
        
    def applyChanges(self):
        #Called when "Apply" Button is Pressed
        #Validates the changes
        #Save the changes to the configuration File
        movementColor = self.movementColorButton.getSelectedColor()
        leftColor = self.leftMouseColorButton.getSelectedColor()
        rightColor = self.rightMouseColorButton.getSelectedColor()
        
        if movementColor == leftColor or movementColor == rightColor or leftColor == rightColor:
            self.parent.showWarning("All 3 colors should be different")
            return False
        
        try:
            self.config.setData("camera",self.cameraButton.getValue())
            self.config.setData("mask",self.maskButton.getValue())
            self.config.setData("leftMouseClick",self.leftMouseButton.getValue())
            self.config.setData("rightMouseClick",self.rightMouseButton.getValue())
            self.config.setData("movementColor",movementColor)
            self.config.setData("leftMouseColor",leftColor)
            self.config.setData("rightMouseColor",rightColor)
            
            self.config.saveConfig()
            
            self.reloadUI()
            
            return True
            
        except Exception as e:
            print(e)
            self.parent.showError("Error in saving Changes.")
            return False
            
if __name__ == "__main__":
    mainUI = MainUI()
    mainUI.mainloop()