
from math import nan
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
        self.isRotating = False
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
    
    def toNewOrientation(self, orientation):
        self.isRotating = True
        if((self.neworientation - 4.0) < orientation < (self.neworientation + 4.0)):
            self.isRotating = False
            self.setNewOrientation(nan)
        else:
            self.rotate(True, ROTSPEED)
        
    def setNewOrientation(self, neworientation):
        self.neworientation = neworientation

    
    def collision(self):
        self.toNewOrientation()
        #backup function in pathplanner
    
    def update(self, status):
        if status==99:
            self.positioning.update() 
            orientation = self.positioning.getOrientation()
            print("------------\n")
            print("Orientation : ", orientation)
            print('Rotating : ' + str(self.isRotating))
            print('Crossroad : ' + str(self.lineFollower.getCrossRoad()))
            #self.collisionAvoidance.update()
            
            if(self.isRotating):
                self.toNewOrientation(orientation)  

            elif(self.lineFollower.getCrossRoad() and not self.isRotating):
                self.setNewOrientation(NORTH)
                self.toNewOrientation(orientation)  
           
            #elif(self.lineFollower.getAdjust()):
             #   print("MOVEMENT ADJ ")
              #  self.adjustOrientation(90)

            elif(not self.isRotating):
                print("Movement to " + str(Position.degreeToDirection(self.positioning.getOrientation())))
                self.movement(SPEED)

            self.lineFollower.update()

        elif status==0:
            self.movement(0)
            print('// Stopped //')