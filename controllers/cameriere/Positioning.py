#from Misc import Position
from Constants import SX, SY
#import Map

class Positioning:
    def __init__(self, compass, camera):
        self.orientation = -123
        self.currentblock = 130             #Starting Block
        self.nextblock = 130
        self.counter = 0                    #Block Counter
        self.compass = compass
        self.camera = camera
        self.updateOrientation()
        #self.position = Position(SX, SY)
        
    def updateOrientation(self):
        self.orientation = self.compass.compassToDegree()
    
    def getOrientation(self):
        return self.orientation
    
    def setOrientation(self, orientation):
        self.orientation = orientation
        
    def updateBlock(self):
        self.image = self.camera.getImage()
        self.nextblock = self.camera.getGrayScale(self.image, self.camera.getWidth(), 64, 126)
        if self.checkNextBlock(self.nextblock):
            self.setCurrentBlock(self.nextblock)
            self.counter += 1
    
    def checkNextBlock(self, nextblock):
        if self.currentblock <= 110 and nextblock >= 110:
            return True
        elif self.currentblock >= 110 and nextblock <= 110:
            return True
        else: return False
    
    def setCurrentBlock(self, newblock):
        self.currentblock = newblock    
    
    def update(self):
        self.updateOrientation()
    
    def resetCounter(self):
        self.counter = 0
    
    def getCounter(self):
        return self.counter
    
    def restartBlockCount(self):
        self.resetCounter()
        if(self.currentblock <= 110):
            self.setCurrentBlock(90)
        elif(self.currentblock >= 110):
            self.setCurrentBlock(110)

    
    
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
