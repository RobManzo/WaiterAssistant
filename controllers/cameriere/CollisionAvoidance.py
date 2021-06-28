class CollisionAvoidance:
    def __init__(self, dsensor, lidar):
        self.proximitysensor = dsensor
        self.lidar = lidar
        self.collisionDetected = False
        self.rotationDegrees = 0
        self.lidarvector = []
        
    def updateSensorsValues(self):
        self.proximitysensor.getValue()
    
    def updateLidarValues(self):
        self.lidarvector = self.lidar.getRangeImage()

    #def collisionCheck(self):
    #    threshold=2.0
    #    if(self.proximitysensor.getValue()>threshold):
    #        self.collisionDetected=True
    #    else:
    #        self.collisionDetected=False

    def collisionCheck(self):
        sector = [0,0,0,0,0,0,0,0]
        if(self.lidarvector):
            i=0
            for x in self.lidarvector:
                if(0 <= i <=45 and x!=float('inf')):
                    sector[0] += x
                if(46 <= i <= 90 and x!=float('inf')):
                    sector[1] += x
                if(91 <= i <= 135 and x!=float('inf')):
                    sector[2] += x
                if(136 <= i <= 180 and x!=float('inf')):
                    sector[3] += x
                if(181 <= i <= 225 and x!=float('inf')):
                    sector[4] += x
                if(226 <= i <= 270 and x!=float('inf')):
                    sector[5] += x
                if(271 <= i <= 315 and x!=float('inf')):
                    sector[6] += x 
                if(316 <= i <= 360 and x!=float('inf')):
                    sector[7] += x
                i += 1
        self.checkSector(sector)

    def getCollision(self):
        if (self.collisionDetected):
            return self.collisionDetected
    
    def checkSector(self, sector):
        if(sector[0]/45 < 1.5):
            print('a collision')
        if(sector[1]/45 < 1):
            print('b collision')
        if(sector[2]/45 < 1):
            print('c collision')
        if(sector[3]/45 < 1):
            print('d collision')
        if(sector[4]/45 < 1):
            print('e collision')
        if(sector[5]/45 < 1):
            print('f collision')
        if(sector[6]/45 < 1):
            print('g collision')
        if(sector[7]/45 < 1):
            print('h collision')
            


    def update(self):
        self.updateLidarValues()
        self.collisionCheck()
        print("\n --- Distance Sensor --- \n  Value: " + str(self.proximitysensor.getValue())) 
