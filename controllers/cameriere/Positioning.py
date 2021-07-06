from Misc import Position
from Constants import SX, SY, WHEEL_RADIUS
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
    
    def getPosition(self):
        return self.position
    
    def updateWheelTraveledDistance(self):
        self.distancetravelled = self.positionsensor.getDistanceTraveled()
    
    def positionOnLandmark(self):
        nearestIntersection = Map.findNearestIntersection(self.position)
        offset = 0.25
        if nearestIntersection != -1:
            x = nearestIntersection.getX()
            y = nearestIntersection.getY()
            if self.orientation == Orientation.NORD:
                nearestIntersection.setX(x + offset)
            if self.orientation == Orientation.EAST:
                nearestIntersection.setY(y - offset)
            if self.orientation == Orientation.SOUTH:
                nearestIntersection.setX(x - offset)
            if self.orientation == Orientation.WEST:
                nearestIntersection.setY(y + offset)
            
            self.position = nearestIntersection

        else:
            print('No intersection nearby')
    
    def setPosition(self, position):
        x = self.position.getX()
        y = self.position.getY()
        if x > 0 and x < Map.HEIGHT - 1:
            self.position.setX(position.x)
        if y > 0 and y < Map.WIDTH - 1:
            self.position.setY(position.y)
    
    def update(self):
        self.updateOrientation()
        #self.updatePosition()
    
    
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
