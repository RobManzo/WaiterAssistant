class CollisionAvoidance:
    def __init__(self, dsensor):
        self.proximitysensor = dsensor
        self.collisionDetected = False
        self.rotationDegrees = 0
        
    
    def updateSensorsValues(self):
        self.proximitysensor.getValue()

    def collisionCheck(self):
        threshold=2.0
        if(self.proximitysensor.getValue()>threshold):
            self.collisionDetected=True
        else:
            self.collisionDetected=False

    def getCollision(self):
        if (self.collisionDetected):
            return self.collisionDetected

    def update(self):
        self.updateSensorsValues()
        self.collisionCheck()
        print("\n --- Distance Sensor --- \n  Value: " + str(self.proximitysensor.getValue())) 