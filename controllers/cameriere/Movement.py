from math import nan
from Misc import Position
from Constants import NORTH, SOUTH, EAST, WEST
from Constants import ROTSPEED, ADJSPEED, SPEED, UNKNOWN
import Map


class Movement:
    def __init__(self,pathplanner, positioning, lmotor, rmotor, collisionAvoidance, lineFollower):
        self.pathplanner=pathplanner
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
        self.goalReach= False
        self.map = Map.MAP
        self.currentPath = UNKNOWN
        self.neworientation=90
        self.nearestintersection=Position(4,1)

    def rotate(self, clockwise, speed): #velocità positiva senso orario
        if clockwise:
            self.rmotor.setVelocity(-speed)
            self.lmotor.setVelocity(speed)
        else: 
            self.rmotor.setVelocity(speed)
            self.lmotor.setVelocity(-speed)

    def adjustOrientation(self, finalDegree):           #Deprecated?
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
                self.setNewOrientation(self.currentPath[0])
            else:
                if(self.clockwise):
                    self.rotate(False, ROTSPEED)
                else:
                    self.rotate(True, ROTSPEED)
        else:
            if((self.neworientation - 4.0) < orientation < (self.neworientation + 4.0)):
                self.isRotating = False
                self.setNewOrientation(self.currentPath[0])
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
        self.updatePath()
        #backup function in pathplanner

    def updateGoalStatus(self):
        currentPosition = self.positioning.getPosition()
        goalPosition = self.pathPlanner.getGoalPosition()

        self.goalReach = currentPosition == goalPosition

    def updatePath(self): #get new route after setting obstacle in map
        if self.isEnabled():
            print("Computing new path..")
            p = self.positioning.getPosition()
            o = self.positioning.getOrientation()
            nearest = Map.getNearestWalkablePosition(p, o)
            if nearest != None:
                p = nearest
            x = p.getX()
            y = p.getY()
            if o == NORTH:
                Map.setNewObstacle(Position(x + 1, y))
            if o == EAST:
                Map.setNewObstacle(Position(x, y - 1))
            if o == SOUTH:
                Map.setNewObstacle(Position(x - 1, y))
            if o == WEST:
                Map.setNewObstacle(Position(x, y + 1))
            
            #if DEBUG:
            #    Map.printMap()s

            self.currentPath = self.pathPlanner.getFastestRoute(0) #Ricordare di avere 2 goal per tavolo

    def update(self): #Goal da mettere nel path planner
            self.positioning.update()
            self.pathplanner.update()
            orientation = self.positioning.getOrientation()
            self.position = self.positioning.getPosition()
            self.currentPath = self.pathplanner.getFastestRoute(0)
            print(str(self.currentPath))
            print('Actual Position: ('+str(self.position.getX())+','+str(self.position.getY())+')')            
            print("New Orientation"+str(self.neworientation))
            print("------------\n")
            print("Orientation : ", orientation)
            #print('Rotating : ' + str(self.isRotating))
            #print('Crossroad : ' + str(self.lineFollower.getCrossRoad()))
            #self.collisionAvoidance.update()
            
            if(self.isRotating):
                self.toNewOrientation(orientation)

            elif(self.goalReach):
                self.movement(0)
                print("GOAL RAGGIUNTO") 

            elif(self.lineFollower.getCrossRoad() and not self.isRotating):
                #○print("prossima direzione"+str(self.currentPath[1]))
                self.positioning.setPosition(self.nearestintersection)
                print("Posizione incrocio settata")
                self.positioning.resetDistanceTraveled() #posizione incrocio settata
                self.rotationDirection(orientation)
                self.toNewOrientation(orientation)
            elif(self.lineFollower.isLineLost() and not self.isRotating):
                print("MOv lost")
                variable=self.positioning.getOrientation()
                print("variable"+str(variable))
                self.setNewOrientation(variable+180.0)
                self.toNewOrientation(orientation) 
           

            elif(not self.isRotating):
                print("Movement to " + str(Position.degreeToDirection(self.positioning.getOrientation())))
                self.movement(SPEED)
                self.distance = self.positioning.getDistanceTraveled()
                if(self.distance!=0.0):
                    self.tiles = self.distance % 0.4 
                    self.nearestintersection = Map.findNearestIntersection(self.position,Position.degreeToDirection(self.positioning.getOrientation()))   
                    if(self.nearestintersection!=-1):
                        print("NEAREST INTERSECTION:")
                        self.nearestintersection.printCoordinate()
                if(self.tiles < 0.006 and self.distance!=0):
                    self.positioning.updatePosition(orientation)
                    if(len(self.currentPath)>1):
                        self.setNewOrientation(self.currentPath[1])    
                print('Caselle percorse: '+ str(self.tiles))
                print('Distance traveled: ' + str(self.distance))    

            self.lineFollower.update()