class Movement:
    def __init__(self,positioning,lmotor,rmotor,collisionAvoidance):
        self.positioning = positioning
        self.lmotor = lmotor
        self.rmotor = rmotor
        self.positioning.update()
        self.collisionAvoidance = collisionAvoidance
        self.collisionAvoidance.update()
        self.isRotating = 0
        self.tolerance=0.2
        self.finalDegree=None

    def rotate(self):
        self.rmotor.setVelocity(-1.00)
        self.lmotor.setVelocity(1.00)
    
    def checkDegrees(self,degree):
        if(degree>=360.0):
                return degree-360.0
        elif(degree<0):
               return degree+360.0
        else:
            return degree
    
    def adjustOrientation(self,finalDegree):
        if(self.positioning.getOrientation()>finalDegree+self.tolerance):
            self.rmotor.setVelocity(0.02)
            self.lmotor.setVelocity(-0.05)
            print("adjust1")
        elif(self.positioning.getOrientation()<finalDegree+self.tolerance):
            self.rmotor.setVelocity(-0.05)
            self.lmotor.setVelocity(0.05)
            print("adjust2")
    def movement(self):
        self.rmotor.setVelocity(6.00)   # 13.75 cm/s ????
        self.lmotor.setVelocity(6.00)
    
    def update(self):
        print(self.positioning.getOrientation())
        self.collisionAvoidance.update()
        if(self.collisionAvoidance.getCollision() and not self.isRotating):
            self.finalDegree=round(self.positioning.getOrientation()+180.0)
            self.finalDegree=self.checkDegrees(self.finalDegree)    
            print("final degree=",self.finalDegree)
            self.isRotating = 1
            self.rotate()
            print(self.isRotating,"collision")
            
        elif(self.isRotating and self.finalDegree+1>self.positioning.getOrientation()>self.finalDegree-1 ):
            self.isRotating = 0
        elif(not self.isRotating and self.finalDegree!= None and not (self.finalDegree+self.tolerance>self.positioning.getOrientation()>self.finalDegree-self.tolerance)):
            self.adjustOrientation(self.checkDegrees(self.finalDegree))
        elif(not self.isRotating):
            print(self.isRotating,"movement")
            self.movement()
        