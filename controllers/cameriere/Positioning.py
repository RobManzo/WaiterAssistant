from Misc import Position
from Constants import NORTH, SOUTH, EAST, WEST
from Constants import SX, SY
import Map
#import Map

class Positioning:
    def __init__(self, compass, positionsensor):
        self.orientation = -123
        self.compass = compass
        self.positionsensor = positionsensor
        self.leftpos = positionsensor.leftpos
        self.rightpos = positionsensor.rightpos
        self.updateOrientation()
        self.position = Position(SX, SY)
        self.distancetravelled = 0.0

    def updateOrientation(self):
        self.orientation = self.compass.compassToDegree()
    
    def getOrientation(self):
        return self.orientation
    
    def setOrientation(self, orientation):
        self.orientation = orientation
    
    def approximateOrientation(self, orientation):
        if( 330.0 < orientation < 360.0 or 0.0 < orientation < 30.0):
            return NORTH
        elif(150.0 < orientation < 210.0):
            return SOUTH
        elif(240.0 < orientation < 310.0):
            return EAST
        elif(60.0 < orientation < 120.0):
            return WEST

    def getPosition(self):
        return self.position
    
    def updateWheelTraveledDistance(self):
        self.distancetravelled = self.positionsensor.getDistanceTraveled()
    
    #def positionOnLandmark(self):
    #    nearestIntersection = Map.findNearestIntersection(self.position)
    #    offset = 0.25
    #    if nearestIntersection != -1:
    #        x = nearestIntersection.getX()
    #        y = nearestIntersection.getY()
    #        if self.orientation == NORTH:
    #            nearestIntersection.setX(x + offset)
    #        if self.orientation == EAST:
    #            nearestIntersection.setY(y - offset)
    #        if self.orientation == SOUTH:
    #            nearestIntersection.setX(x - offset)
    #        if self.orientation == WEST:
    #            nearestIntersection.setY(y + offset)
    #        
    #        self.position = nearestIntersection
#
    #    else:
    #        print('No intersection nearby')
    
    def setPosition(self, position):
        x = self.position.getX()
        y = self.position.getY()
        if x > 0 and x < Map.HEIGHT - 1:
            self.position.setX(position.x)
        if y > 0 and y < Map.WIDTH - 1:
            self.position.setY(position.y)
    
    def updatePosition(self, orientation):      #Da richiamare ogni volta che si ci sposta di 0.4m
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
