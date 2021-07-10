from math import nan
from Misc import Position
from Constants import NORTH, SOUTH, EAST, WEST
from Constants import ROTSPEED, ADJSPEED, SPEED
import Map


class Movement:
    def __init__(self, positioning, lmotor, rmotor, collisionAvoidance, lineFollower):
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
        self.tiles = 0
        self.clockwise = True
        self.map = Map.MAP

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
        if(self.neworientation == NORTH and 270.0 < orientation < 360.0 ):
            if(4.0 < orientation < 354.0):
                self.isRotating = False
                self.setNewOrientation(nan)
            else:
                if(self.clockwise):
                    self.rotate(False, ROTSPEED)
                else:
                    self.rotate(True, ROTSPEED)
        else:
            if((self.neworientation - 4.0) < orientation < (self.neworientation + 4.0)):
                self.isRotating = False
                self.setNewOrientation(nan)
            else:
                if(self.clockwise):
                    self.rotate(False, ROTSPEED)
                else:
                    self.rotate(True, ROTSPEED)
                    
    def setNewOrientation(self, neworientation):
        self.neworientation = neworientation
    
    def rotationDirection(self, orientation):
        if((self.neworientation - orientation) < 0.0 or (self.neworientation - orientation) > 180.0 ):
            self.clockwise = False
        else:
            self.clockwise = True

    def collision(self):
        self.toNewOrientation()
        #backup function in pathplanner
    
    def update(self, positionsensor, goal):
            self.positioning.update()
            orientation = self.positioning.getOrientation()
            self.position = self.positioning.getPosition()
            print('Goal Table: ' + str(goal))
            print('Actual Position: ('+str(self.position.getX())+','+str(self.position.getY())+')')
            
              #NUMERO BLOCCHI SPOSTATI, 1 BLOCCO = 0.4m [mi conta due blocchi? Due volte resto zero? Troppo lento?]
            
            
            print("------------\n")
            print("Orientation : ", orientation)
            #print('Rotating : ' + str(self.isRotating))
            #print('Crossroad : ' + str(self.lineFollower.getCrossRoad()))
            #self.collisionAvoidance.update()
            
            if(self.isRotating):
                self.toNewOrientation(orientation)  

            elif(self.lineFollower.getCrossRoad() and not self.isRotating):
                self.setNewOrientation(NORTH)
                self.positioning.setPosition(self.nearestintersection)
                print("Posizione incrocio settata")
                positionsensor.resetDistanceTraveled() #posizione incrocio settata
                self.rotationDirection(orientation)
                self.toNewOrientation(orientation)
            elif(self.lineFollower.isLineLost() and not self.isRotating):
                print("MOv lost")
                variable=self.positioning.getOrientation()
                print("variable"+str(variable))
                self.setNewOrientation(variable+180.0)
                self.toNewOrientation(orientation) 
           
            #elif(self.lineFollower.getAdjust()):
             #   print("MOVEMENT ADJ ")
              #  self.adjustOrientation(90)

            elif(not self.isRotating):
                print("Movement to " + str(Position.degreeToDirection(self.positioning.getOrientation())))
                self.movement(SPEED)
                self.distance = positionsensor.getDistanceTraveled()
                if(self.distance!=0.0):
                    self.tiles = self.distance % 0.4 
                    self.nearestintersection = Map.findNearestIntersection(self.position)
                    if(self.nearestintersection!=-1):
                        self.nearestintersection.printCoordinate()
                if(self.tiles < 0.006 and self.distance!=0):
                    self.positioning.updatePosition(orientation)
                print('Caselle percorse: '+ str(self.tiles))
                print('Distance traveled: ' + str(self.distance))    

            self.lineFollower.update()