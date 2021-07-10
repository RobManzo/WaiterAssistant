from Misc import Position
from Constants import NORTH, SOUTH, EAST, WEST
# MAP DIMENSIONS
WIDTH = 15          # map width
HEIGHT = 15         # map height
MAP_RESOLUTION = 0.4 # map resolution

# MAP CONSTANS
B = -123    # arena border
K = -123    # kitchen
F = 0       # floor
S = -1      # start tile
C = 66      # intersection
O = 99      # obstacle

# --- MAP ---
# F-----> Y      ^ S
# |              | 
# |        E <-- F --> W
# v X            |
#                v N
#                                       
#      Y  0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16     X    map[X][Y]
MAP =   [[B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B], # 0
         [B, K, K, K, K, F, F, F, F, F, F, F, F, F, F, F, B], # 1
         [B, K, K, K, K, F, F, F, 1, 1, F, C, F, 2, 2, F, B], # 2
         [B, K, K, K, K, F, F, F, F, F, F, F, F, F, F, F, B], # 3
         [B, S, F, F, F, F, C, F, F, F, F, C, F, F, F, F, B], # 4
         [B, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, B], # 5
         [B, C, F, 3, 3, F, C, F, 4, 4, F, C, F, 5, 5, F, B], # 6
         [B, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, B], # 7
         [B, C, F, F, F, F, C, F, F, F, F, C, F, F, F, F, B], # 8
         [B, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, B], # 9
         [B, C, F, 6, 6, F, C, F, 7, 7, F, C, F, 8, 8, F, B], # 10
         [B, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, B], # 11
         [B, C, F, F, F, F, C, F, F, F, F, C, F, F, F, F, B], # 12
         [B, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, B], # 13
         [B, C, F, 9, 9, F, C, F, 10, 10, F, C, F, 11, 11, F, B], # 14
         [B, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, B], # 15
         [B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B]] # 16


# return map value in postion
def getValue(position):
    return MAP[position.getX()][position.getY()]

# Ritorna TRUE se la posizione individuata è calpestabile
def isWalkable(position):
    x = position.getX()
    y = position.getY()
    if x < HEIGHT and x > 0 and y < WIDTH and y > 0:
        value = MAP[x][y]
        return value == F or value == C
    return False

# set new 
def setNewObstacle(position):
    x = position.getX()
    y = position.getY()
    if x> 0 and x < HEIGHT:
        if y > 0 and y < WIDTH:
            MAP[x][y] = O

def findNearestIntersection(position): #ADAPT
    radius = 1
    list=[]
    x = position.getX()
    y = position.getY()
    for i in range(x-radius, x+radius +1):
        for j in range(y-radius, y+radius +1):
            if i < HEIGHT and i > 0 and j < WIDTH and j > 0:
                if MAP[i][j] == C:
                    list.append(Position(i, j))
    if len(list):
        return list[-1]
    return -1

def getNearestWalkablePosition(position, orientation): #ADAPT
    if not isWalkable(position):
        print("Actual position non walkable. " + str(position) + " is unwalkable")
        x = position.getX()
        y = position.getY()
        print("ORIENTATION: " + str(orientation))
        if orientation == NORTH or orientation == SOUTH:
            p = Position(x, y - 1)
            if isWalkable(p):
                return p
            p = Position(x, y + 1)
            if isWalkable(p):
                return p
        elif orientation == EAST or orientation == WEST:
            p = Position(x - 1, y)
            if isWalkable(p):
                return p
            p = Position(x + 1, y)
            if isWalkable(p):
                return p
    else:
        return position

def printMap():
    for F in range(HEIGHT):
        for j in range(WIDTH):
            if F>= 0 and F < HEIGHT:
                if j >= 0 and j < WIDTH:
                    print("%2d" % MAP[F][j], end=" ")
        print()




