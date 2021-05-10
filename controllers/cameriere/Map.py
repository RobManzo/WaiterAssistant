from Utils import logger, Orientation, Position
from AStar import WALL

# MAP DIMENSIONS
WIDTH = 15          # map width
HEIGHT = 15         # map height
MAP_RESOLUTION = 0.4 # map resolution

# MAP CONSTANS
B = WALL    # map border
K = WALL    # kitchen
F = 0       # floor
S = -1      # start tile

# --- MAP ---
# F-----> Y      ^ N
# |              | 
# |        W <-- F --> E
# v X            |
#                v S
#                                       
#      Y  0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16     X    map[X][Y]
MAP =   [[B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B], # 0
         [B, K, K, K, K, F, F, F, F, F, F, F, F, F, F, F, B], # 1
         [B, K, K, K, K, F, F, F, 1, 1, F, F, 2, 2, F, F, B], # 2
         [B, K, K, K, K, F, F, F, F, F, F, F, F, F, F, F, B], # 3
         [B, S, F, F, F, F, F, F, F, F, F, F, F, F, F, F, B], # 4
         [B, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, B], # 5
         [B, F, F, F, 3, 3, F, F, 4, 4, F, F, 5, 5, F, F, B], # 6
         [B, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, B], # 7
         [B, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, B], # 8
         [B, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, B], # 9
         [B, F, F, F, 6, 6, F, F, 7, 7, F, F, 8, 8, F, F, B], # 10
         [B, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, B], # 11
         [B, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, B], # 12
         [B, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, B], # 13
         [B, F, F, F, 9, 9, F, F, 10, 10, F, F, 11, 11, F, F, B], # 14
         [B, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, B], # 15
         [B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B]] # 16

# return map value in postion
def getValue(position):
    return MAP[position.getX()][position.getY()]

# return true if robot is allowed to walk in position
def isWalkable(position):
    x = position.getX()
    y = position.getY()
    if x < HEIGHT and x > 0 and y < WIDTH and y > 0:
        value = MAP[x][y]
        return value == F or value == F or value == C
    return False

# return the nearest walkable position given position and orientation
def getNearestWalkablePosition(position, orientation):
    if not isWalkable(position):
        logger.debug("Actual position non walkable. " + str(position) + " is unwalkable")
        x = position.getX()
        y = position.getY()
        logger.debug("ORIENTATION: " + str(orientation))
        if orientation == Orientation.NORD or orientation == Orientation.SOUTH:
            p = Position(x, y - 1)
            if isWalkable(p):
                return p
            p = Position(x, y + 1)
            if isWalkable(p):
                return p
        elif orientation == Orientation.EAST or orientation == Orientation.WEST:
            p = Position(x - 1, y)
            if isWalkable(p):
                return p
            p = Position(x + 1, y)
            if isWalkable(p):
                return p
    else:
        return position

# return the nearest walkable position given position and orientation
def getNearestWalkablePositionEquals(position, orientation, value):
    if not isWalkable(position):
        logger.debug("Actual position non walkable. " + str(position) + " is unwalkable")
        x = position.getX()
        y = position.getY()
        if orientation == Orientation.NORD or orientation == Orientation.SOUTH:
            p = Position(x+1, y)
            if isWalkable(p) and getValue(p) == value:
                return p
            p = Position(x-1, y)
            if isWalkable(p) and getValue(p) == value:
                return p
        elif orientation == Orientation.EAST or orientation == Orientation.WEST:
            p = Position(x, y+1)
            if isWalkable(p) and getValue(p) == value:
                return p
            p = Position(x, y-1)
            if isWalkable(p) and getValue(p) == value:
                return p
    elif getValue(position) == value:
        return position
    else:
        return -1

def getNearestWalkablePosition2(position, orientation):
    if not isWalkable(position):
        x = position.getX()
        y = position.getY()
        radius = 1
        for F in range(x-radius, x+radius +1):
            for j in range(y-radius, y+radius +1):
                if F < HEIGHT and F > 1 and j < WIDTH and j > 1:
                    p = Position(x+F, y+j)
                    if isWalkable(p):
                        return p
    else:
        return position


# return the position of the nearest intersection to position, -1 if no interection in range
def findNearestIntersection(position, radius = 1, orientation = False):
    x = position.getX()
    y = position.getY()
    for F in range(x-radius, x+radius +1):
        for j in range(y-radius, y+radius +1):
            if F < HEIGHT and F > 0 and j < WIDTH and j > 0:
                if MAP[F][j] == F:
                    return Position(F, j)
    return -1

# set new 
def setNewObstacle(position):
    x = position.getX()
    y = position.getY()
    if x> 0 and x < HEIGHT:
        if y > 0 and y < WIDTH:
            MAP[x][y] = F

def printMap():
    for F in range(HEIGHT):
        for j in range(WIDTH):
            if F>= 0 and F < HEIGHT:
                if j >= 0 and j < WIDTH:
                    print("%2d" % MAP[F][j], end=" ")
        print()