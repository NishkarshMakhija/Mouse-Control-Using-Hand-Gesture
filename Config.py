import json
from ColorRadioButton import ColorRadioButton

class Config:
    
    def  __init__(self):
        self.__readDataFromFile()
        
    def __readDataFromFile(self):
        try:
            with open("config.json") as f:
                self.data = json.load(f)
            
            self.__verifyData()
        except:
            self.resetToDefault()
            
    def __verifyData(self):
        if self.data == None or len(self.data)!=7:
            raise Exception("Invalid Data")
        
        keys = ["camera","mask","leftMouseClick","rightMouseClick","movementColor","leftMouseColor","rightMouseColor"]
        for key in keys:
            if key not in self.data:
                raise Exception("Invalid Data")
        
        return True
                
            
    def resetToDefault(self):
        
        self.data = {}
        self.data["camera"] = True
        self.data["mask"] = False
        self.data["leftMouseClick"] = True
        self.data["rightMouseClick"] = False
        self.data["movementColor"] = ColorRadioButton.colorRed
        self.data["leftMouseColor"] = ColorRadioButton.colorBlue
        self.data["rightMouseColor"] = ColorRadioButton.colorGreen
        
        self.saveConfig()

    def saveConfig(self):
        try:
            with open("config.json","w") as json_file:
                json.dump(self.data,json_file)
        except:
            raise Exception("Error in creating Config File")
            
    def setData(self,key,value):
        if key in self.data:
            self.data[key] = value
        else:
            raise Exception("Invalid Key")
            
    def getData(self,key):
        if key in self.data:
            return self.data[key]
        else:
            raise Exception("Invalid Key")

'''
if __name__ =="__main__":
    
    c = Config()
'''