
# MAP DIMENSIONS
WIDTH = 15          # map width
HEIGHT = 15         # map height
MAP_RESOLUTION = 0.4 # map resolution

# MAP CONSTANS
B = -123    # arena border
K = -123    # kitchen
F = 0       # floor
S = -1      # start tile
C = 66      # curve
O = 99      # obstacle

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
         [B, K, K, K, K, F, F, F, 1, 1, F, F, F, 2, 2, F, B], # 2
         [B, K, K, K, K, F, F, F, F, F, F, F, F, F, F, F, B], # 3
         [B, S, F, F, F, F, C, F, F, F, F, C, F, F, F, F, B], # 4
         [B, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, B], # 5
         [B, F, F, 3, 3, F, F, F, 4, 4, F, F, F, 5, 5, F, B], # 6
         [B, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, B], # 7
         [B, C, F, F, F, F, C, F, F, F, F, C, F, F, F, F, B], # 8
         [B, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, B], # 9
         [B, F, F, 6, 6, F, F, F, 7, 7, F, F, F, 8, 8, F, B], # 10
         [B, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, B], # 11
         [B, C, F, F, F, F, C, F, F, F, F, C, F, F, F, F, B], # 12
         [B, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, B], # 13
         [B, F, F, 9, 9, F, F, F, 10, 10, F, F, F, 11, 11, F, B], # 14
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

def printMap():
    for F in range(HEIGHT):
        for j in range(WIDTH):
            if F>= 0 and F < HEIGHT:
                if j >= 0 and j < WIDTH:
                    print("%2d" % MAP[F][j], end=" ")
        print()




