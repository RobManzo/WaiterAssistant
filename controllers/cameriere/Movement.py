
import time
from Misc import Position
from Constants import NORTH, SOUTH, EAST, WEST,BASE
from Constants import ROTSPEED, ADJSPEED, SPEED, UNKNOWN, INSERT,MOVING,STOP
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
        self.toLastCrossroad=False
        self.goalReach= False
        self.map = Map.MAP
        self.lastGoal=None
        self.currentPath = []
        self.neworientation=None
        self.nearestintersection=None
        self.backToKitchen=False
        self.status= INSERT
        self.isParking=False
        self.isParked=False

    def getStatus(self):
        return self.status
    def setStatus(self,status):
        self.status=status
        print("Setting status to"+str(status))
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
    def getBackToKitchen(self):
        return self.backToKitchen        
    def movement(self, speed):
        self.rmotor.setVelocity(speed+self.lineFollower.getRightSpeed())
        self.lmotor.setVelocity(speed+self.lineFollower.getLeftSpeed())
    
    def toNewOrientation(self, orientation):
        self.isRotating = True
        if(self.neworientation==None and self.lastGoal.comparePosition(Position(3,4))):
            self.neworientation=0
        if(self.neworientation == NORTH and 270.0 < orientation < 360.0 ):
            if(358.0 < orientation < 360.0 or  0 <= orientation <= 2):
                self.isRotating = False
            else:
                if(self.clockwise):
                    self.rotate(True, ROTSPEED)
                else:
                    self.rotate(False, ROTSPEED)
        else:
            if((self.neworientation - 2.0) < orientation < (self.neworientation + 2.0)): 
                self.isRotating = False
            else:
                if(self.clockwise):
                    self.rotate(True, ROTSPEED)
                else:
                    self.rotate(False, ROTSPEED)
                    
    def setNewOrientation(self, neworientation):
        self.neworientation = neworientation

    def stop(self):
        self.setNewOrientation(NORTH)
        self.toNewOrientation(self.positioning.getOrientation())      



    def rotationDirection(self, orientation):
        print("neworientation:")
        print(self.neworientation)
        print("orientation:")
        print(orientation)
        if(len(self.currentPath)>1):
            self.setNewOrientation(self.currentPath[1])
        if(self.neworientation == NORTH):
            if( 180 <= orientation <= 359.9):
                self.clockwise = False
            elif(0.1 <= orientation < 180):
                self.clockwise = True
        elif(self.neworientation == SOUTH):
            if( 180.1 <= orientation <= 359.9 ):
                self.clockwise = True
            elif( 0 <= orientation <= 179.9 ):
                self.clockwise = False
        elif(self.neworientation == EAST):
            if(0 <= orientation <= 89.9 or 269.9 <= orientation <= 359.9 ):
                self.clockwise = True
            elif( 90 <= orientation <= 270.1):
                self.clockwise = False
        elif(self.neworientation == WEST):
            if( 90.1 <= orientation <= 270):
                self.clockwise = True
            elif( 270.1 <= orientation <= 359.9 or 0 <= orientation <= 89.9):
                self.clockwise = False
            

    def collision(self):
        self.updatePath()
        #backup function in pathplanner

    def uTurn(self, orientation):
        approx = self.positioning.approximateOrientation(orientation)
        if(approx == NORTH):
            return SOUTH
        elif(approx == SOUTH):
            return NORTH
        elif(approx == EAST):
            return WEST
        elif(approx == WEST):
            return EAST    

    def updateGoalStatus(self):
        currentPosition = self.positioning.getPosition()
        goalPosition = self.pathplanner.getGoalPosition()
        print("GOAL UPDATE")
        goalPosition.printCoordinate()
        self.goalReach = goalPosition.comparePosition(currentPosition)

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
        if(self.getStatus()!=STOP):
            self.positioning.update()
            self.pathplanner.update()
            orientation = self.positioning.getOrientation()
            self.position = self.positioning.getPosition()
            self.updateGoalStatus()
            self.collisionAvoidance.update()
            print("parking")
            print(self.isParking)
            print(self.collisionAvoidance.getSensorValue())
            print('Actual Position: ('+str(self.position.getX())+','+str(self.position.getY())+')')            
            print("New Orientation"+str(self.neworientation))
            print("------------\n")
            print("Orientation : ", orientation)
            print('Rotating : ' + str(self.isRotating))
            #print('Crossroad : ' + str(self.lineFollower.getCrossRoad()))
        

            if(self.isParked):
                self.rmotor.setVelocity(0)
                self.lmotor.setVelocity(0)
                self.setStatus(STOP)
            elif(self.isRotating):
                self.toNewOrientation(orientation)
            elif(self.isParking and self.position.comparePosition(Position(3,4))):
                if(358.0 < orientation < 360.0 or  0 <= orientation <= 2):
                    self.isRotating = False
                    self.isParking=False
                    self.isParked=True
                else:
                    self.rotate(True,ROTSPEED)
                print("parking if")
            elif(self.backToKitchen):
                self.movement(0)
                self.positioning.setPosition(self.lastGoal)
                self.backToKitchen=False
            elif(self.goalReach):
                self.movement(0)
                self.lineFollower.disable()
                print("GOAL RAGGIUNTO") 
                self.pathplanner.setGoalPosition(Position(3,4))
                self.isParking=True
                self.lastGoal=self.positioning.getPosition()
                
                print("lastGoal:")
                self.lastGoal.printCoordinate()
                print("Consegna in corso...")
                time.sleep(5)
                
                variable=self.positioning.getOrientation()
                self.setNewOrientation(Position.degreeToDirection(self.uTurn(variable)))
                self.toNewOrientation(orientation)
                self.goalReach=False
                self.backToKitchen=True

            elif(self.lineFollower.getCrossRoad() and not self.isRotating):
                #○print("prossima direzione"+str(self.currentPath[1]))
                if(self.nearestintersection!=-1):
                    self.positioning.setPosition(self.nearestintersection)
                print("Posizione incrocio settata")
                self.positioning.resetDistanceTraveled() #posizione incrocio settata
                self.rotationDirection(orientation)
                self.toNewOrientation(orientation)

            elif(self.lineFollower.isLineLost() and not self.isRotating):
                print("MOv lost")
                variable=self.positioning.getOrientation()
                print("variable"+str(variable))
                self.setNewOrientation(self.uTurn(variable))
                self.toNewOrientation(orientation)
            
            elif(self.collisionAvoidance.isCollisionDetected() and not self.isRotating):
                x = self.position.getX()
                y = self.position.getX()
                if(orientation == NORTH):
                    self.positioning.setNewObstacle(Position(x+1, y))
                elif(orientation == SOUTH):
                    self.positioning.setNewObstacle(Position(x-1, y))
                elif(orientation == WEST):
                    self.positioning.setNewObstacle(Position(x, y+1))
                elif(orientation == EAST):
                    self.positioning.setNewObstacle(Position(x, y-1))
                self.updatePath()
                approxxorientation = self.positioning.approximateOrientation(orientation)
                if(approxxorientation == NORTH):
                    self.setNewOrientation(SOUTH)
                elif(approxxorientation == SOUTH):
                    self.setNewOrientation == NORTH
                elif(approxxorientation == WEST):
                    self.setNewOrientation == EAST
                elif(approxxorientation == EAST):
                    self.setNewOrientation == WEST
                self.isRotating = True
        

            elif(not self.isRotating):
                print("Movement to " + str(Position.degreeToDirection(self.positioning.getOrientation())))
                self.movement(SPEED)
                self.lineFollower.enable()
                self.distance = self.positioning.getDistanceTraveled()
                if(self.distance!=0.0):
                    self.tiles = self.distance % 0.4 
                    self.nearestintersection = Map.findNearestIntersection(self.position,self.currentPath[0])
                    print(Position.degreeToDirection(self.positioning.getOrientation()))
                    if(self.nearestintersection!=-1):
                        print("NEAREST INTERSECTION:")
                        self.nearestintersection.printCoordinate()
                self.currentPath = self.pathplanner.getFastestRoute(0)
                if(self.tiles < 0.0062 and self.distance!=0):
                    self.positioning.updatePosition(orientation)
                    if(len(self.currentPath)>1):
                        self.setNewOrientation(self.currentPath[1]) 
                print("currentpath:")
                print(str(self.currentPath))

                   
                print('Caselle percorse: '+ str(self.tiles))
                print('Distance traveled: ' + str(self.distance))    

            self.lineFollower.update()
        else:
            print("ciao")
            