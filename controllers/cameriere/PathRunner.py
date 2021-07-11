from Misc import Position
from Constants import UNKNOWN, NORTH, SOUTH, EAST, WEST, SPEED
from Map import Map

DISABLED = 0
FOLLOW_LINE = 1
TURN = 2
SEARCH_LINE = 3
STOP = 4
U_TURN = 55

# class to handle path running service
class PathRunner:

    # initialize path running service
    def __init__(self, positioning, pathPlanner, lineFollower, distanceSensors):
        self.positioning = positioning
        self.pathPlanner = pathPlanner
        self.lineFollower = lineFollower
        self.distanceSensors = distanceSensors

        self.status = DISABLED
        self.prevStatus = UNKNOWN

        self.uTurnStatus = UNKNOWN
        self.uTurnGoalOrientation = UNKNOWN
        self.uTurnStartingMeter = UNKNOWN
        self.actualTurn = 0
        self.currentPath = UNKNOWN
        self.goalReach = False
        self.speed = SPEED

        self.collisionImminent = False

    def isEnabled(self):
        return self.status != DISABLED

    def enable(self):
        self.status = FOLLOW_LINE

    def disable(self):
        self.status = DISABLED

    def isUTurning(self):
        return self.status == U_TURN

    def setCollisionImminent(self, value):
        self.collisionImminent = value

    def setPrevStatus(self):
        tempStatus = self.prevStatus
        self.prevStatus = self.status
        self.status = tempStatus

    def setStatus(self, status):
        if self.status != status:
            self.prevStatus = self.status
            self.status = status

    # update path running service
    def update(self):
        if self.status != DISABLED:
            self.updateSpeedAndAngle() #ADAPT
            self.updateGoalStatus()
        

    # get new fastest path from actual position to goal if set
    def updatePath(self):
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
                Map.setNewObstacle(Position(x - 1, y))
            if o == EAST:
                Map.setNewObstacle(Position(x, y + 1))
            if o == SOUTH:
                Map.setNewObstacle(Position(x + 1, y))
            if o == WEST:
                Map.setNewObstacle(Position(x, y - 1))
            
            #if DEBUG:
            #    Map.printMap()

            self.currentPath = self.pathPlanner.getFastestRoute()
            self.actualTurn = 0

    # check if robot have reached goal
    def updateGoalStatus(self):
        currentPosition = self.positioning.getPosition()
        goalPosition = self.pathPlanner.getGoalPosition()

        self.goalReach = currentPosition == goalPosition
    
    # update speed and angle of the robot
    def updateSpeedAndAngle(self):
        isLineLost = self.lineFollower.isLineLost()
        currentPath = self.currentPath

        print("Current Status: " + str(self.status) + " prev Status: " + str(self.prevStatus))

        lineFollowerAngle = self.lineFollower.getNewSteeringAngle()

        if currentPath != UNKNOWN and self.actualTurn == 0:
            if self.currentPath[self.actualTurn] == U_TURN:
                self.setStatus(U_TURN)
            self.actualTurn += 1
        
        elif self.status == FOLLOW_LINE :

            self.steeringAngle = lineFollowerAngle
            if self.isGoalReach():
                self.setStatus(STOP)

            if isLineLost and currentPath == UNKNOWN:
                self.speed = 0.0
            elif isLineLost and currentPath != UNKNOWN and Map.findNearestIntersection(self.positioning.getPosition(), 1) != -1:
                #if self.prevStatus != SEARCH_LINE:
                self.setStatus(TURN)
            elif isLineLost and Map.findNearestIntersection(self.positioning.getPosition()) == -1:
                self.setStatus(SEARCH_LINE)
            
        elif self.status == TURN:
            if  currentPath != UNKNOWN and self.actualTurn < len(currentPath):
                
                turn = currentPath[self.actualTurn]
                
                self.steeringAngle = 0.57 * turn
            else:
                self.currentPath = UNKNOWN
            
            if not isLineLost:
                self.actualTurn += 1
                self.setStatus(FOLLOW_LINE)

        elif self.status == SEARCH_LINE:
            self.steeringAngle = self.lineFollower.getSteeringAngleLineSearching()

            if not isLineLost:
                logger.debug("Line was lost and i found it!")
                self.setStatus(FOLLOW_LINE)

            threshold = 500
            angle = 0.5
            logger.debug("FRONT LEFT: ")
            if self.distanceSensors.frontLeft.getValue() > threshold:
                self.lineFollower.resetLastLineKnownZone(angle)
            elif self.distanceSensors.frontRight.getValue() > threshold:
                self.lineFollower.resetLastLineKnownZone(- angle)
        
        elif self.status == STOP :
            self.speed = 0.0
            logger.info("Destination Reached")

            
        # logger.debug("Steerign angle: " + str(self.steeringAngle) + " STATUS: " + str(self.status))
        elif self.isGoalReach() and isLineLost and currentPath == UNKNOWN:
            self.speed = 0.0

        elif not isLineLost:
            self.steeringAngle = self.lineFollower.getNewSteeringAngle()
            # self.actualTurn += 1

        elif isLineLost and currentPath != UNKNOWN:
            if self.actualTurn < len(currentPath):
                turn = currentPath[self.actualTurn]
                self.steeringAngle = 0.5 * turn
                # what if U_TURN? Return it to motion to make u_turn?
            else:
                currentPath = UNKNOWN

        elif isLineLost and currentPath == UNKNOWN:
            # self.speed = 0.0
            pass

    # get current steering angle setted by path runner [NON CREDO CI SERVI]
    def getSteeringAngle(self):
        return self.steeringAngle

    # get current speed setted by path runner
    def getSpeed(self):
        return self.speed

    # return if goal has been reached
    def isGoalReach(self):
        return self.goalReach

    # set goal
    def goTo(self, goal):
        self.pathPlanner.setGoalPosition(goal)
        self.currentPath = self.pathPlanner.getFastestRoute()
        logger.debug("Current Path to Goal: " + str(self.currentPath))