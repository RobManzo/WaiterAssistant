import Devices

class Positioning:
    def __init__(self,compass):
        self.orientation=-123
        self.compass = compass
        self.updateOrientation()

    def updateOrientation(self):
        self.orientation=self.compass.compassToDegree()
    
    def getOrientation(self):
        return self.orientation

    def update(self):
        self.updateOrientation()