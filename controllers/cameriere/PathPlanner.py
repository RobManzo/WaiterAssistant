import Map
from Misc import Position
from Constants import UNKNOWN, NORTH, SOUTH, EAST, WEST, FORWARD, LEFT, RIGHT, U_TURN
import Astar
# MAP DIMENSIONS
#WIDTH = 15          # map width
#HEIGHT = 15         # map height
#MAP_RESOLUTION = 0.4 # map resolution

# MAP CONSTANS
#B = WALL    # map border
#K = WALL    # kitchen
#F = 0       # floor
#S = -1      # start tile
#C = 66      # curve

# --- MAP ---
# F-----> Y      ^ N
# |              | 
# |        W <-- F --> E
# v X            |
#                v S
#                                       
#      Y  0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16     X    map[X][Y]
#MAP =  [[B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B], # 0
#        [B, K, K, K, K, F, F, F, F, F, F, F, F, F, F, F, B], # 1
#        [B, K, K, K, K, F, F, F, 1, 1, F, F, F, 2, 2, F, B], # 2
#        [B, K, K, K, K, F, F, F, F, F, F, F, F, F, F, F, B], # 3
#        [B, S, F, F, F, F, C, F, F, F, F, C, F, F, F, F, B], # 4
#        [B, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, B], # 5
#        [B, F, F, 3, 3, F, F, F, 4, 4, F, F, F, 5, 5, F, B], # 6
#        [B, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, B], # 7
#        [B, C, F, F, F, F, C, F, F, F, F, C, F, F, F, F, B], # 8
#        [B, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, B], # 9
#        [B, F, F, 6, 6, F, F, F, 7, 7, F, F, F, 8, 8, F, B], # 10
#        [B, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, B], # 11
#        [B, C, F, F, F, F, C, F, F, F, F, C, F, F, F, F, B], # 12
#        [B, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, B], # 13
#        [B, F, F, 9, 9, F, F, F, 10, 10, F, F, F, 11, 11, F, B], # 14
#        [B, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, B], # 15
#        [B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B]] # 16

class PathPlanner:
    def __init__(self, positioning,externalcontroller):
        self.map = Map.MAP
        self.externalcontroller=externalcontroller
        self.positioning = positioning
        self.robotPosition = positioning.getPosition()
        self.robotOrientation = positioning.getOrientation()
        self.goalPositions = UNKNOWN
    
    # update path planning service
    def setGoal(self):
        self.goalPositions=Map.tablePositions(self.externalcontroller.getTable())
        print("Goal Positions"+ str(self.goalPositions))
        
    def update(self):
        self.robotPosition = self.positioning.getPosition()
        self.robotOrientation = self.positioning.getOrientation()

    # update map to improve path planning when obstacle are found
    def updateMap(self):
        self.map = Map.MAP

    
    # return array containing a turn for each intersection in the path between robot position and goal
    def getFastestRoute(self):

        # update map status, this ensure new obstacles are detected
        self.updateMap()

        #logger.debug("Path from: " + str(self.robotPosition) + " to " + str(self.goalPosition) + " Initial Orientation: " + str(self.robotOrientation))
        # get fastest route from AStar giving map, start position and goal position
        route = Astar.findPath(self.map, self.robotPosition.getPositionArray(), self.goalPosition.getPositionArray())

        # if no route was found, return UNKNOWN path
        if route == None:
            return UNKNOWN

        # get only intersection nodes from AStar route
        intersections = self.getIntersectionNodesFromRoute(route)

        # get cardinal points directions based on intersection nodes
        directions = self.getDirectionsFromIntersections(intersections)
        
        #logger.debug(directions)

        # get turns based on robot directions and robot orientation
        turns = self.getTurnsFromDirections(directions)

        #logger.debug(turns)

        # remove curve turns
        turns = self.removeCurves(turns, intersections)

        # return the turns
        return turns

    #set goal position in the map
    def setGoalPosition(self, position):
        x = position.getX()
        y = position.getY()

        if x > 0 and x < Map.HEIGHT - 1:
            if y > 0 and y < Map.WIDTH - 1:
                self.goalPosition.setY(y)
                self.goalPosition.setX(x)
                return
        self.goalPosition = UNKNOWN
    
    def getGoalPosition(self):
        return self.goalPosition

    # return first, last and intersection nodes from AStar route
    def getIntersectionNodesFromRoute(self, route):
        intersections = []
        #if self.map[route[0][0]][route[0][1]] == I:
            # get first node
        if route != None:
            intersections.append(route[0])

            # get intersection nodes
            for node in route[1:-1]:
                if self.map[node[0]][node[1]] == Map.I or self.map[node[0]][node[1]] == Map.C: #FORSE BASTA LASCIARE C
                    intersections.append(node)

            # get last node
            intersections.append(route[-1]) 
            
            # return intersections
            return intersections

    # return cardinal points direction from one intersection to another
    def getDirectionsFromIntersections(self, intersections):
        directions = []

        # for each cople of nodes compute cardinal points direction between them
        prevNode = intersections[0]
        for currentNode in intersections[1:]:
            # check if X has changed
            if currentNode[0] > prevNode[0]:
                directions.append(NORTH)
            elif currentNode[0] < prevNode[0]:
                directions.append(SOUTH)
            # check if Y has changed
            elif currentNode[1] > prevNode[1]:
                directions.append(WEST)
            elif currentNode[1] < prevNode[1]:
                directions.append(EAST)
            else:
                print("Invalid intersetions")
            # go to next couple of node
            prevNode = currentNode
        
        return directions

    # contains a list of turns (RIGHT, LEFT, FORWARD, U_TURN) for each intersection based on robot orientation and next direction
    def getTurnsFromDirections(self, directions):
        turns = []

        # get actual robot orientation
        actualDirection = self.robotOrientation
        
        # for each cardinal point direction compute turn based on robot current and future orientation [E SE INVECE DI GIRARE A DESTRA O SX GLI PASSASSIMO SOLAMENTE L'ORIENTAZIONE N-S-E-W?]
        for direction in directions:
            # FORWARD case
            if actualDirection == direction:
                turns.append(FORWARD)
            # EST cases
            elif actualDirection == EAST and direction == SOUTH:
                turns.append(RIGHT)
            elif actualDirection == EAST and direction == NORTH:
                turns.append(LEFT)
            elif actualDirection == EAST and direction == WEST:
                turns.append(U_TURN)
            # WEST cases
            elif actualDirection == WEST and direction == SOUTH:
                turns.append(LEFT)
            elif actualDirection == WEST and direction == NORTH:
                turns.append(RIGHT)
            elif actualDirection == WEST and direction == EAST:
                turns.append(U_TURN)
            # NORTH cases
            elif actualDirection == NORTH and direction == EAST:
                turns.append(RIGHT)
            elif actualDirection == NORTH and direction == WEST:
                turns.append(LEFT)
            elif actualDirection == NORTH and direction == SOUTH:
                turns.append(U_TURN)
            # SOUTH cases
            elif actualDirection == SOUTH and direction == EAST:
                turns.append(LEFT)
            elif actualDirection == SOUTH and direction == WEST:
                turns.append(RIGHT)
            elif actualDirection == SOUTH and direction == NORTH:
                turns.append(U_TURN)
            # change actual direction 
            actualDirection = direction

        return turns

    # remove curves from turns
    def removeCurves(self, turns, intersections):
        newTurns = [turns[0]]
        for i in range(1, len(intersections) - 1):
            node = intersections[i]
            if self.map[node[0]][node[1]] != Map.C:
                newTurns.append(turns[i])
        return newTurns

    # print actual status
    def printStatus(self):
        robotPosition = self.robotPosition
        goalPosition = self.goalPosition
        robotOrientation = "UNKNOWN"
        if self.robotOrientation == NORTH:
            robotOrientation = "NORTH"
        if self.robotOrientation == EAST:
            robotOrientation = "EST"    
        if self.robotOrientation == SOUTH:
            robotOrientation = "SOUTH"
        if self.robotOrientation == WEST:
            robotOrientation = "WEST"
        
        print("Navigation Status: ")
        print("Robot Position: " + "(X: " + str(robotPosition.getX()) + ", Y: " + str(robotPosition.getY()) +")")
        print("Robot Orientation: " + str(robotOrientation))
        print("Goal Position: " + "(X: " + str(goalPosition.getX()) + ", Y: " + str(goalPosition.getY()) +")")
        return self.goalPosition



