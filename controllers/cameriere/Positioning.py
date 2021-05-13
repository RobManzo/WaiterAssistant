import Devices
#from Misc import Position
from Constants import SX, SY
#import Map

class Positioning:
    def __init__(self,compass):
        self.orientation=-123
        self.compass = compass
        self.updateOrientation()
        #self.position = Position(SX, SY)
        

    def updateOrientation(self):
        self.orientation=self.compass.compassToDegree()
    
    def getOrientation(self):
        return self.orientation
    
    def setOrientation(self, orientation):
        self.orientation = orientation

    def update(self):
        self.updateOrientation()
    
    
    #def setPosition(self, position):
    #    x = position.getX()
    #    y = position.getY()
    #    if x > 0 and x < Map.Height - 1:
    #        self.position.setX(position.x)
    #    if y > 0 and y < Map.Width - 1:
    #        self.position.setY(position.y)
#
    #def getPosition(self):
    #    return self.position
