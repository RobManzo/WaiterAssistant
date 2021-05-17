class CollisionAvoidance:
    def __init__(self,proximitysensor):
        self.proximitysensor=proximitysensor
        self.lSensor = 0
        self.lfSensor = 0
        self.fSensor = 0
        self.rfSensor = 0
        self.rSensor = 0        
        self.rbSensor = 0
        self.bSensor = 0
        self.lbSensor = 0
        self.collisionDetected = 0
        self.rotationDegrees = 0
        
    
    def updateSensorsValues(self):
        self.lSensor = self.proximitysensor.lSensor.getValue()
        self.lfSensor = self.proximitysensor.lfSensor.getValue()
        self.fSensor = self.proximitysensor.fSensor.getValue()
        self.rfSensor = self.proximitysensor.rfSensor.getValue()
        self.rSensor = self.proximitysensor.rSensor.getValue()
        self.rbSensor = self.proximitysensor.rbSensor.getValue()
        self.bSensor = self.proximitysensor.bSensor.getValue()
        self.lbSensor = self.proximitysensor.lbSensor.getValue()

    def collisionCheck(self):
        threshold=1.65
        if(self.fSensor<threshold):
            self.collisionDetected=1 #possibile ritornare quale sensore ha dato la collisione
        elif(self.lfSensor<threshold):
            self.collisionDetected=1
        elif(self.rfSensor<threshold):
            self.collisionDetected=1
        else:
            self.collisionDetected=0

    def getCollision(self):
        if (self.collisionDetected):
            return self.collisionDetected

    def update(self):
        self.updateSensorsValues()
        self.collisionCheck()
        print("l:",self.lSensor,"\nlf:",self.lfSensor,"\nf:",self.fSensor,"\nrf:",self.rfSensor,"\nr:",self.rSensor,"\nrb:",self.rbSensor,"\nb:",self.bSensor,"\nlb:",self.lbSensor)