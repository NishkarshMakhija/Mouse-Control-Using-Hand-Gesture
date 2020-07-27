import numpy as np

class Util:
    #for red color we need two masks
    redMask = [{
                #For Lower Red
                "lower" : np.array([0,120,70]),
                "upper" : np.array([10,255,255])
                },
                {
                #For upper Red
                "lower" : np.array([170,120,70]),
                "upper" : np.array([180,255,255])
                }
               ]
               
    blueMask = [{
                 # define range of blue color in HSV
                 "lower" : np.array([50,100,70]), #S can be 60
                 "upper" : np.array([130,255,255])
                }
               ]
               
    yellowMask = [{
                 # define range of yellow color in HSV
                 "lower" : np.array([20,140,100]), #S can be 60
                 "upper" : np.array([30,255,255])
                }
               ]
               
    purpleMask = [{
                 # define range of purple color in HSV
                 "lower" : np.array([115,40,50]), #S can be 60
                 "upper" : np.array([130,255,255])
                }
               ]
               
    greenMask = [{
                 # define range of green color in HSV
                 "lower" : np.array([40,86,50]), #S can be 60
                 "upper" : np.array([65,255,255])
                }
               ]
               
    
    def getMaskFromColor(color):
        if color == "red":
            return Util.redMask
        elif color == "blue":
            return Util.blueMask
        elif color == "yellow":
            return Util.yellowMask
        elif color == "purple":
            return Util.purpleMask
        elif color == "green":
            return Util.greenMask
        else:
            raise Exception("Invalid Color")
               

     