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