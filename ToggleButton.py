from tkinter import *

class ToggleButton(Button):
    
    def __init__(self,parent,value=True,padx=0,pady=0):
        self.value = value
        if value:
            Button.__init__(self,parent,text="YES",fg="white",padx=padx,pady=pady,command=self.toggle)
        else:
            Button.__init__(self,parent,text="NO",fg="white",padx=padx,pady=pady,command=self.toggle)
            
        self.__changeColor()
        
    def toggle(self):
        if self.value:
            self["text"]="NO"
        else:
            self["text"]="YES"
            
        self.value = not self.value
        self.__changeColor()
        
    def __changeColor(self):
        if self.value:
            self["bg"] = "green"
            
        else:
            self["bg"] = "red"
            
    def getValue(self):
        return self.value


''''
if __name__ == "__main__":
    
    root = Tk()
    
    root.geometry("200x100")
    
    toggleButton = ToggleButton(root,value=False,padx=10)
    toggleButton.pack()
    
    root.mainloop()
    
'''