from Constants import N,S,W,E
from Misc import Position
from Constants import ROTATION_SPEED, ADJUSTMENT_SPEED, SPEED

class Movement:
    def __init__(self, positioning, lmotor, rmotor, collisionAvoidance):
        self.positioning = positioning
        self.lmotor = lmotor
        self.rmotor = rmotor
        self.positioning.update()
        #self.positioning.updateBlock()
        self.collisionAvoidance = collisionAvoidance
        self.collisionAvoidance.update()
        self.isRotating = 0
        self.tolerance=0.05
        self.finalDegree=None

    def rotate(self, speed, clockwise): #velocità positiva senso orario
        if clockwise:
            self.rmotor.setVelocity(-speed)
            self.lmotor.setVelocity(speed)
        else: 
            self.rmotor.setVelocity(speed)
            self.lmotor.setVelocity(-speed)

    def adjustOrientation(self, finalDegree):
        orientation = self.positioning.getOrientation()
        finalDegree = Position.degreeToDirection(finalDegree)
        diff=finalDegree-orientation
        print(diff)
        if(diff>-0.051 or diff<-360):
            self.rotate(ADJUSTMENT_SPEED, True)
        else:
            self.rotate(ADJUSTMENT_SPEED, False)
            
    def movement(self, speed):
        self.rmotor.setVelocity(speed)
        self.lmotor.setVelocity(speed)
    
    def toNewOrientation(self, fdegree):
        self.isRotating = 1
        self.startDegree = self.positioning.getOrientation()
        self.setFinalDegree(fdegree)
        self.diff  = self.startDegree-self.finalDegree
        self.diff = Position.checkDegrees(self.diff)
        if(self.diff > 180.0):
            self.rotate(ROTATION_SPEED, True)
        else:
            self.rotate(ROTATION_SPEED, False)
        self.positioning.restartBlockCount()

    def setFinalDegree(self, fdegree):
        self.finalDegree = fdegree
    
    def collision(self):
        self.toNewOrientation()
        #backup function in pathplanner
    
    def update(self, speaker):
        print("------------\n")
        while not(speaker.isSpeaking()):
            speaker.speak('Stall', 1)
        print("Orientation:", self.positioning.getOrientation())
        print("Final target degree:", self.finalDegree)
        self.collisionAvoidance.update()
        self.positioning.update()
        print("Block Counter : " + self.positioning.getCounter().__str__())

        if(self.positioning.getCounter() == 5):                                     #pathplanner decide di quanto spostare nella direzione corrente(?)
            self.toNewOrientation(180.0)
            print("final degree=", self.finalDegree)
            print(self.isRotating,"collision")   

        elif(self.collisionAvoidance.getCollision() and not self.isRotating):       #Collisione
            self.toNewOrientation(180.0)
            print("final degree=", self.finalDegree)
            print(self.isRotating, "collision")            

        elif(self.isRotating and self.finalDegree+1 > self.positioning.getOrientation() > self.finalDegree-1):  #rotazione 
            self.isRotating = 0

        elif(not self.isRotating and self.finalDegree != None and not (self.finalDegree + self.tolerance > self.positioning.getOrientation() > self.finalDegree-self.tolerance)): #adjust orientation
            self.adjustOrientation(Position.checkDegrees(self.finalDegree))

        elif(not self.isRotating):
            print(self.isRotating, "movement to " + Position.degreeToDirection(self.positioning.getOrientation()).__str__()) #counter to a direction
            self.movement(SPEED)
            self.positioning.updateBlock()