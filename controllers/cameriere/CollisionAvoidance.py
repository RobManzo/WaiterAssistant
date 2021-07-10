class CollisionAvoidance:
    def __init__(self, dsensor):
        self.proximitysensor = dsensor
        self.collisionDetected = False
        self.rotationDegrees = 0
        
    def updateSensorsValues(self):
        self.proximitysensor.getValue()

    #def collisionCheck(self):
    #    threshold=2.0
    #    if(self.proximitysensor.getValue()>threshold):
    #        self.collisionDetected=True
    #    else:
    #        self.collisionDetected=False

    def getCollision(self):
        if (self.collisionDetected):
            return self.collisionDetected
    
    #def checkSector(self, sector):
    #    if(sector[0]/45 < 1.5):
    #        print('a collision')
    #    if(sector[1]/45 < 1):
    #        print('b collision')
    #    if(sector[2]/45 < 1):
    #        print('c collision')
    #    if(sector[3]/45 < 1):
    #        print('d collision')
    #    if(sector[4]/45 < 1):
    #        print('e collision')
    #    if(sector[5]/45 < 1):
    #        print('f collision')
    #    if(sector[6]/45 < 1):
    #        print('g collision')
    #    if(sector[7]/45 < 1):
    #        print('h collision')
            


    def update(self):
        print("\n --- Distance Sensor --- \n  Value: " + str(self.proximitysensor.getValue())) 
