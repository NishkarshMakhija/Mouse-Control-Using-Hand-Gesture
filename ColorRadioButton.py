from tkinter import *
#from tkinter.ttk import *

class ColorRadioButton(Frame):

    colorRed = "red"
    colorBlue = "blue"
    colorGreen = "green"
    colorYellow = "yellow"
    colorPurple = "purple"
    
    def __init__(self,parent,color):
        Frame.__init__(self,parent)
        
        self.__colors = [self.colorRed,self.colorBlue,self.colorGreen,self.colorYellow,self.colorPurple]
        self.__activeColors = ["pink","light blue","light green","yellow","purple"]
        
        self.setSelectedColor(color)
        
        for index,color in enumerate(self.__colors):
            r = Radiobutton(self,text="",value = color,variable = self.__selectedColor,background=color,selectcolor=self.__activeColors[index],indicator=0)
            r.pack(side=LEFT,ipady=5,ipadx=12)
       
    def getSelectedColor(self):
        return self.__selectedColor.get()
        
    def setSelectedColor(self,color):
        if color not in self.__colors:
            raise Exception("Invalid Color")
        
        self.__selectedColor = StringVar(self,color)
            


# if __name__ == "__main__":
#     root = Tk()
    
#     root.geometry("300x300")
    
#     f = ColorRadioButton(root,ColorRadioButton.colorBlue)
#     f.pack()
    
#     root.mainloop()