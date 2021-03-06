from Misc import Position
from Constants import NORTH, SOUTH, EAST, WEST, BMAP
# MAP DIMENSIONS
WIDTH = 17          # map width
HEIGHT = 17        # map height
MAP_RESOLUTION = 0.4 # map resolution
# MAP CONSTANS
B = -123    # arena border
K = -123    # kitchen
F = -123       # floor
S = -1      # start tile
C = 66      # intersection
O = -123          # obstacle
L = 0 
# --- MAP ---
# F-----> Y      ^ S
# |              | 
# |        E <-- F --> W
# v X            |
#                v N
#                                       
#      Y  0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18   X    map[X][Y]
MAP =   [[B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B], # 0
         [B, K, K, K, K, K, B, B, B, B, B, B, B, B, B, B, B, B, B], # 1
         [B, K, K, K, K, K, F, F, F, F, F, F, F, F, F, F, F, B, B], # 2
         [B, K, K, K, K, K, F, C, 1, B, B, 1, C, 2, B, B, B, B, B], # 3
         [B, K, K, K, K, S, F, L, F, F, F, F, L, F, F, 2, F, B, B], # 4
         [B, B, C, L, L, C, L, C, L, L, L, L, C, L, L, C, F, B, B], # 5
         [B, B, L, F, F, F, F, L, F, F, F, F, L, F, F, F, F, B, B], # 6
         [B, B, C, 3, B, B, 3, C, 4, B, B, 4, C, 5, B, B, F, B, B], # 7
         [B, B, L, F, F, F, F, L, F, F, F, F, L, F, F, 5, F, B, B], # 8
         [B, B, C, L, L, L, L, C, L, L, L, L, C, L, L, C, F, B, B], # 9
         [B, B, L, F, F, F, F, L, F, F, F, F, L, F, F, 8, F, B, B], # 10
         [B, B, C, 6, B, B, 6, C, 7, B, B, 7, C, 8, B, B, F, B, B], # 11
         [B, B, L, F, F, F, F, L, F, F, F, F, L, F, F, F, F, B, B], # 12
         [B, B, C, L, L, L, L, C, L, L, L, L, C, L, L, C, F, B, B], # 13
         [B, B, L, F, F, F, F, L, F, F, F, F, L, F, F, 11, F, B, B], # 14
         [B, B, C, 9, B, B, 9, C, 10, B, B, 10, C, 11, B, B, F, B, B], # 15
         [B, B, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, B, B], # 16
         [B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B], # 17
         [B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B]] # 18

class Map:
    def __init__(self):
        self.MAP = MAP

    def resetMap(self):
        self.MAP = BMAP
    
    def getMap(self):
        return self.MAP

    #return positions of goals x table
    def tablePositions(self, table):
        print("TABLE:"+str(table))
        list=[]
        for i in range(19):
            for j in range(19):
                    if self.MAP[i][j] == table:
                        list.append(Position(i, j))
        return list

    # return map value in postion
    def getValue(self, position):
        return self.MAP[position.getX()][position.getY()]

    # Ritorna TRUE se la posizione individuata ?? calpestabile
    def isWalkable(self, position):
        x = position.getX()
        y = position.getY()
        if x < HEIGHT and x > 0 and y < WIDTH and y > 0:
            value = self.MAP[x][y]
            return value == F or value == C or value == L
        return False

    # set new 
    def setNewObstacle(self, position):
        x = position.getX()
        y = position.getY()
        if x> 0 and x < HEIGHT:
            if y > 0 and y < WIDTH:
                self.MAP[x][y] = O
        print("OBSTACLE SET IN "+str(x)+","+str(y))
        #printMap()

    def findNearestIntersection(self, position,orientation): #ADAPT
        radius = 1
        list=[]
        x = position.getX()
        y = position.getY()
        for i in range(x-radius, x+radius +1):
            for j in range(y-radius, y+radius +1):
                if i < HEIGHT and i > 0 and j < WIDTH and j > 0:
                    if self.MAP[i][j] == C:
                        list.append(Position(i, j))
        print("LISTA incroci")
        for x in list:
            x.printCoordinate()
        if len(list):
            if(orientation==NORTH or orientation==WEST):
                return list[-1]
            else:
                return list[0]
        return None

    def getNearestWalkablePosition(self, position, orientation):
        if not self.isWalkable(position):
            print("Actual position non walkable. " + str(position) + " is unwalkable")
            x = position.getX()
            y = position.getY()
            print("ORIENTATION: " + str(orientation))
            if orientation == NORTH or orientation == SOUTH:
                p = Position(x, y - 1)
                if self.isWalkable(p):
                    return p
                p = Position(x, y + 1)
                if self.isWalkable(p):
                    return p
            elif orientation == EAST or orientation == WEST:
                p = Position(x - 1, y)
                if self.isWalkable(p):
                    return p
                p = Position(x + 1, y)
                if self.isWalkable(p):
                    return p
        else:
            return position

    def printMap(self):
        for F in range(HEIGHT):
            for j in range(WIDTH):
                if F>= 0 and F < HEIGHT:
                    if j >= 0 and j < WIDTH:
                        print("%2d" % self.MAP[F][j], end=" ")
            print()




