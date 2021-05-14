import Devices
#from Misc import Position
from Constants import SX, SY
#import Map

class Positioning:
    def __init__(self,compass, camera):
        self.orientation = -123
        self.compass = compass
        self.camera = camera
        self.updateOrientation()
        #self.position = Position(SX, SY)
        self.currentblock = 130             #Starting Block
        self.counter = 0                    #Block Counter
        

    def updateOrientation(self):
        self.orientation=self.compass.compassToDegree()
    
    def getOrientation(self):
        return self.orientation
    
    def setOrientation(self, orientation):
        self.orientation = orientation

    def update(self):
        self.updateOrientation()
    
    def updateBlock(self, camera):
        self.image = camera.getImage()
        self.nextblock = camera.getGrayScale(self.image, self.camera.getWidth(), 64, 126)
        if self.checkNextBlock(self.currentblock, self.nextblock):
            self.setCurrentBlock(self.nextblock)
            self.counter += 1
    
    def checkNextBlock(self, currentblock, nextblock):
        if currentblock < 110 and nextblock > 110:
            return True
        elif currentblock > 110 and nextblock < 110:
            return True
        else: return False
    
    def setCurrentBlock(self, newblock):
        self.currentblock = newblock    
    

    
    
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
