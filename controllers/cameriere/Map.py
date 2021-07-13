from Misc import Position
from Constants import NORTH, SOUTH, EAST, WEST
# MAP DIMENSIONS
WIDTH = 15          # map width
HEIGHT = 15         # map height
MAP_RESOLUTION = 0.4 # map resolution

# MAP CONSTANS
B = -123    # arena border
K = -123    # kitchen
F = -123       # floor
S = -1      # start tile
C = 66      # intersection
O = 99      # obstacle
L = 0 
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
         [B, K, K, K, K, F, C, 1, B, B, 1, C, 2, B, B, B, B], # 2
         [B, K, K, K, S, F, L, F, F, F, F, L, F, F, F, F, B], # 3
         [B, C, L, L, C, L, C, L, L, L, L, C, F, F, F, F, B], # 4
         [B, L, F, F, F, F, L, F, F, F, F, L, F, F, F, F, B], # 5
         [B, C, 3, B, B, 3, C, 4, B, B, 4, C, 5, B, B, F, B], # 6
         [B, L, F, F, F, F, L, F, F, F, F, L, F, F, F, F, B], # 7
         [B, C, L, L, L, L, C, L, L, L, L, C, F, F, F, F, B], # 8
         [B, L, F, F, F, F, L, F, F, F, F, L, F, F, F, F, B], # 9
         [B, C, 6, B, B, 6, C, 7, B, B, 7, C, 8, B, B, F, B], # 10
         [B, L, F, F, F, F, L, F, F, F, F, L, F, F, F, F, B], # 11
         [B, C, L, L, L, L, C, L, L, L, L, C, F, F, F, F, B], # 12
         [B, L, F, F, F, F, L, F, F, F, F, L, F, F, F, F, B], # 13
         [B, C, 9, B, B, 9, C, 10, B, B, 10, C, 11, B, B, F, B], # 14
         [B, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, B], # 15
         [B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B]] # 16


#return positions of goals x table
def tablePositions(table):
    print("TABLE:"+str(table))
    list=[]
    for i in range(17):
        for j in range(17):
                if MAP[i][j] == table:
                    list.append(Position(i, j))
    return list

# return map value in postion
def getValue(position):
    return MAP[position.getX()][position.getY()]

# Ritorna TRUE se la posizione individuata è calpestabile
def isWalkable(position):
    x = position.getX()
    y = position.getY()
    if x < HEIGHT and x > 0 and y < WIDTH and y > 0:
        value = MAP[x][y]
        return value == F or value == C or value == L
    return False

# set new 
def setNewObstacle(position):
    x = position.getX()
    y = position.getY()
    if x> 0 and x < HEIGHT:
        if y > 0 and y < WIDTH:
            MAP[x][y] = O

def findNearestIntersection(position,orientation): #ADAPT
    radius = 1
    list=[]
    x = position.getX()
    y = position.getY()
    for i in range(x-radius, x+radius +1):
        for j in range(y-radius, y+radius +1):
            if i < HEIGHT and i > 0 and j < WIDTH and j > 0:
                if MAP[i][j] == C:
                    list.append(Position(i, j))
    print("LISTA incroci")
    for x in list:
        x.printCoordinate()
    if len(list):
        if(orientation==NORTH or orientation==WEST):
            return list[-1]
        else:
            return list[0]
    return -1

def getNearestWalkablePosition(position, orientation):
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




