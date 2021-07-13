from Constants import NORTH,SOUTH,EAST,WEST

class Position:
    def __init__(self, x, y):
        self.x = 0
        self.y = 0
        self.setX(x)
        self.setY(y)

    def setX(self, x):
        self.x = x
    
    def setY(self, y):
        self.y = y
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y

    def getPositionArray(self):
        return (self.getX(), self.getY())    

    def printCoordinate(self):
        print("Coordinate X: "+ str(self.getX()) + " Coordinate Y: " + str(self.getY()))
    
    def degreeToDirection(degree):
        if(355.0 < degree < 360.0 or 0.0 < degree < 5.0):
            return NORTH
        elif(265.0<degree<275.0):
            return EAST
        elif(85.0<degree<95.0):
            return WEST
        elif(175.5<degree<185.0):
            return SOUTH
        print("Degree to direction: " + str(degree))
    def comparePosition(self,position):
        if(self.x==position.x and self.y == position.y):
            return True
        return False
    def checkDegrees(degree):
        if(degree>=360.0):
                return degree-360.0
        elif(degree<=0):
            return degree+360.0
        else:
            return degree