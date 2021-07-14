from Misc import Position
from Constants import NORTH, SOUTH, EAST, WEST
from Constants import SX, SY , WHEEL_RADIUS
import Map

class Positioning:
    def __init__(self, compass, positionsensor):
        self.orientation = -123
        self.compass = compass
        self.positionsensor = positionsensor
        self.leftpos = positionsensor.leftpos
        self.rightpos = positionsensor.rightpos
        #self.updateOrientation()
        self.position = Position(SX, SY)
        self.distancetravelled = 0.0
        self.error=0
        self.distance=0
        self.psstep = 0
        #self.i=1

    def updateOrientation(self):
        self.orientation = self.compass.compassToDegree()
    
    def getOrientation(self):
        return self.orientation
    
    def setOrientation(self, orientation):
        self.orientation = orientation
    
    def getDistanceTraveled(self):
        self.distance=float((self.positionsensor.getLeftSensor()*WHEEL_RADIUS + self.positionsensor.getRightSensor()*WHEEL_RADIUS)/4)
        return self.distance-self.error
    
    def resetDistanceTraveled(self):
        #self.i+=self.i
        self.error = self.distance
    
    def resetDistance(self):
        self.distance = 0

    def approximateOrientation(self, orientation):
        if( 315.0 <= orientation <= 360.0 or 0.0 <= orientation <= 45.0):
            return NORTH
        elif(135.0 <= orientation <= 225.0):
            return SOUTH
        elif(225.0 < orientation < 315.0):
            return EAST
        elif(45.0 < orientation < 135.0): 
            return WEST

    def getPosition(self):
        return self.position
    
    def setPosition(self, position):
        x = self.position.getX()
        y = self.position.getY()
        if x >= 1 and x < Map.HEIGHT - 1:
            self.position.setX(position.x)
        if y >= 1 and y < Map.WIDTH - 1:
            self.position.setY(position.y)
       
    
    def updatePosition(self, orientation):
        actualpos = self.getPosition()
        x = actualpos.getX()
        y = actualpos.getY()
        if(self.approximateOrientation(self.orientation) == NORTH):
            x += 1
        elif(self.approximateOrientation(self.orientation) == SOUTH):
            x -= 1
        elif(self.approximateOrientation(self.orientation) == EAST):
            y -= 1
        elif(self.approximateOrientation(self.orientation) == WEST):
            y += 1
        self.setPosition(Position(x,y))
    
    def update(self):
        self.updateOrientation()
    
    def setNewObstacle(self, obstacle):
        Map.setNewObstacle(obstacle)
        print("setting new obstacle at:")
        obstacle.printCoordinate()