from Constants import N, S, E, W

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

    def printCoordinate(self):
        print("Coordinate X: "+ self.getX() + " Coordinate Y: " + self.getY())
    
    def degreeToDirection(degree):
        if(361.0>degree>359.0 or 1.0>degree>-1.0):
            return E
        elif(271.0>degree>269.0):
            return N
        elif(91.0>degree>89.0):
            return S
        elif(181.0>degree>179.0):
            return W

    def checkDegrees(degree):
        if(degree>=360.0):
                return degree-360.0
        elif(degree<=0):
            return degree+360.0
        else:
            return degree