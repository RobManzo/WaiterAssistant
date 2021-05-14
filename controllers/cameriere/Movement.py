from Constants import N,S,W,E

class Movement:
    def __init__(self,positioning,lmotor,rmotor,collisionAvoidance):
        self.positioning = positioning
        self.lmotor = lmotor
        self.rmotor = rmotor
        self.positioning.update()
        self.collisionAvoidance = collisionAvoidance
        self.collisionAvoidance.update()
        self.isRotating = 0
        self.tolerance=0.05
        self.finalDegree=None

    def rotate(self,speed): #velocità positiva senso orario
        self.rmotor.setVelocity(-speed)
        self.lmotor.setVelocity(speed)
    
    def checkDegrees(self,degree):
        if(degree>=360.0):
                return degree-360.0
        elif(degree<=0):
               return degree+360.0
        else:
            return degree
    def degreeToDirection(self,degree):
        if(361.0>degree>359.0):
            return E
        elif(1.0>degree>-1.0):
            return E
        elif(271.0>degree>269.0):
            return N
        elif(91.0>degree>89.0):
            return S
        elif(181.0>degree>179.0):
            return W

    def adjustOrientation(self,finalDegree):
        orientation=self.positioning.getOrientation()
        finalDegree=self.degreeToDirection(finalDegree)
        diff=finalDegree-orientation
        print(diff)
        if(diff>-0.051 or diff<-360):
            self.rotate(0.08)
        else:
            self.rotate(-0.08)
            
    def movement(self,speed):
        self.rmotor.setVelocity(speed)
        self.lmotor.setVelocity(speed)
    
    def toNewOrientation(self, ):
        self.isRotating=1
        self.startDegree=self.positioning.getOrientation()
        self.finalDegree=self.degreeToDirection(self.checkDegrees(self.startDegree+90.0)) #finalDegree verrà scelto dal PathPlanner
        self.diff=self.startDegree-self.finalDegree
        self.diff=self.checkDegrees(self.diff)
        if(self.diff>180.0):
            self.rotate(1.0)
        else:
            self.rotate(-1.0)

    def update(self):
        print("Orientation:",self.positioning.getOrientation())
        print("final:",self.finalDegree)
        self.collisionAvoidance.update()
        self.positioning.updateBlock(self.positioning.camera)
        print("Block Counter : " + self.positioning.counter.__str__())
        if(self.collisionAvoidance.getCollision() and not self.isRotating):
            self.toNewOrientation()
            print("final degree=",self.finalDegree)
            print(self.isRotating,"collision")            
        elif(self.isRotating and self.finalDegree+1>self.positioning.getOrientation()>self.finalDegree-1 ):
            self.isRotating = 0
        elif(not self.isRotating and self.finalDegree!= None and not (self.finalDegree+self.tolerance>self.positioning.getOrientation()>self.finalDegree-self.tolerance)):
            self.adjustOrientation(self.checkDegrees(self.finalDegree))
        elif(not self.isRotating):
            print(self.isRotating,"movement")
            self.movement(6.0)
        