# Collision Avoidance status
DISABLED = False
ENABLED = True

# class to handle collision avoidance service
class CollisionAvoidance:
    # initialize collision avoidance service
    def __init__(self, distancesensor):
        self.distancesensor = distancesensor
        self.frontsensor = 0.0
        self.status = DISABLED
        self.collision = False
        self.threshold = 2.5 #DA PROVARE

    def isEnabled(self):
        return self.status != DISABLED

    def enable(self):
        self.status = ENABLED

    def disable(self):
        self.status = DISABLED
        self.resetCollision()
        self.frontsensor=0

    # return true is an imminent collision is detected 
    def isCollisionDetected(self):
        return self.collision

    def checkCollision(self):
        if(self.frontsensor > self.threshold):
            return True
        else:
            return False

    # update collision avoidance service
    def update(self):
        if self.status == ENABLED:
            self.updateSensorsValue()
            self.collision = self.checkCollision()
            
    def resetCollision(self):
        self.collision = False

    # update sensors values
    def updateSensorsValue(self):
        self.frontsensor = self.distancesensor.getValue()
        
    # return distance sensors instance
    def getDistanceSensor(self):
        return self.distancesensor
    
    def getSensorValue(self):
        return self.frontsensor