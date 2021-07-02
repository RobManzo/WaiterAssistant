
from Constants import NORTH, SOUTH, WEST, EAST
from Misc import Position
from Constants import ROTSPEED, ADJSPEED, SPEED

class Movement:
    def __init__(self, positioning, lmotor, rmotor, collisionAvoidance,lineFollower):
        self.positioning = positioning
        self.lmotor = lmotor
        self.rmotor = rmotor
        self.lineFollower=lineFollower
        self.positioning.update()
        self.collisionAvoidance = collisionAvoidance
        self.collisionAvoidance.update()
        self.isRotating = 0
        self.tolerance = 0.02
        self.finalDegree = None

    def rotate(self, clockwise, speed): #velocità positiva senso orario
        if clockwise:
            self.rmotor.setVelocity(-speed)
            self.lmotor.setVelocity(speed)
        else: 
            self.rmotor.setVelocity(speed)
            self.lmotor.setVelocity(-speed)

    def adjustOrientation(self, finalDegree):
        orientation = self.positioning.getOrientation()
        finalDegree = Position.degreeToDirection(finalDegree)
        diff = finalDegree-orientation
        print('Diff' + str(diff))
        if(diff>-0.051 or diff<-360.0):
            self.rotate(ADJSPEED, True)
        else:
            self.rotate(ADJSPEED, False)
            
    def movement(self, speed):
        self.rmotor.setVelocity(speed+self.lineFollower.getRightSpeed())
        self.lmotor.setVelocity(speed+self.lineFollower.getLeftSpeed())
    
    def toNewOrientation(self, actualorientation):                      #Generalizzare
        self.isRotating = 1
        self.startDegree = self.positioning.getOrientation()
        self.setFinalDegree(round(float(actualorientation + 180.0), 0))
        self.diff  = self.startDegree-self.finalDegree
        self.diff = Position.checkDegrees(self.diff)
        if(not(self.finalDegree - 2)<self.diff<(self.finalDegree + 2)):
            self.rotate(ROTSPEED, True)
        if(not(self.finalDegree - self.tolerance)<self.diff<(self.finalDegree + self.tolerance)):
            self.rotate(ADJSPEED, True)

    def setFinalDegree(self, fdegree):
        self.finalDegree = Position.checkDegrees(fdegree)
    
    def collision(self):
        self.toNewOrientation()
        #backup function in pathplanner
    
    def update(self, status):
        if status==99:
            print("------------\n")
            print("Orientation:", self.positioning.getOrientation())
            print("Final target degree:", self.finalDegree)
            self.collisionAvoidance.update()
            self.positioning.update() 
            self.lineFollower.update()


   
            if(self.collisionAvoidance.getCollision() and not self.isRotating):       #Collisione
                self.toNewOrientation(self.positioning.getOrientation())
                print("final degree=", self.finalDegree)
                print(self.isRotating, "collision")            
   
            elif(self.isRotating and self.finalDegree + self.tolerance > self.positioning.getOrientation() > self.finalDegree - self.tolerance ):  #rotazione 
                self.isRotating = 0
           
            #elif(self.lineFollower.getAdjust()):
             #   print("MOVEMENT ADJ ")
              #  self.adjustOrientation(90)

            elif(not self.isRotating):
                print(self.isRotating, "movement to " + Position.degreeToDirection(self.positioning.getOrientation()).__str__()) #counter to a direction
                self.movement(SPEED)

        elif status==0:
            self.movement(0)
            print('// Stopped //')