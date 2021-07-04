from Misc import Position
from Constants import SX, SY, WHEEL_RADIUS
import Map
#import Map

class Positioning:
    def __init__(self, compass, positionsensor):
        self.orientation = -123
        self.compass = compass
        self.positionsensor = positionsensor
        self.updateOrientation()
        self.position = Position(SX, SY)
        
    def updateOrientation(self):
        self.orientation = self.compass.compassToDegree()
    
    def getOrientation(self):
        return self.orientation
    
    def setOrientation(self, orientation):
        self.orientation = orientation
    
    def getPosition(self):
        return self.position
    
    def setPosition(self, position):
        x = self.position.getX()
        y = self.position.getY()
        if x > 0 and x < Map.HEIGHT - 1:
            self.position.setX(position.x)
        if y > 0 and y < Map.WIDTH - 1:
            self.position.setY(position.y)
    
    def update(self):
        self.updateOrientation()
        self.updatePosition()
    
    def updateWheelTraveledDistance(self):
        # get radiants from wheel
        radFLW = self.positionsensor.getLeftDistance()
        radFRW = self.positionsensor.getRightDistance()

        # compute distance traveled
        self.leftWheelDistance = radFLW * WHEEL_RADIUS
        self.rightWheelDistance = radFRW * WHEEL_RADIUS

    def updatePosition(self):
        
        speed = self.actuators.getSpeed()

        if speed != 0:
            # get actual float map position
            x = self.position.x
            y = self.position.y

            # 72 = 0.50 m/s * speed/MAX_SPEED [1.8] / 40 step/s / 0.5 m
            # linearMove = ((0.50 * (speed/MAX_SPEED)) / 40) * 2
            linearMove = speed/72

            # compass decimal digits
            precision = 2

            turnCoeficent = 1
            # if turning you need to do less meters in order to change position in the map
            steeringAngle = self.actuators.getAngle()
            if abs(steeringAngle) == 0.57:
                turnCoeficent = 1.2

            # update position    
            newX = x - round(self.compass.getXComponent(), precision) * linearMove * turnCoeficent
            newY = y + round(self.compass.getYComponent(), precision) * linearMove * turnCoeficent
        
            self.setPosition(Position(newX,newY))

    
    
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
