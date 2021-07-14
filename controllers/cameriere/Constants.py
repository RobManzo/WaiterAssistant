from math import nan
STOP=-100
INSERT = 100
MOVING = 200
BASE=0
WAITING = 305
UNKNOWN = nan
MAX_SPEED = 6.50
SPEED = 3.0
ROTSPEED = 4.0
ADJSPEED = 0.20
WHEEL_RADIUS = 0.132
M_PI = 3.14
SX = 4
SY = 5
TIMESTEP = 32
B = -123    # arena border
K = -123    # kitchen
F = -123       # floor
S = -1      # start tile
C = 66      # intersection
O = -123          # obstacle
L = 0 
MAP =   [[B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B], # 0
         [B, K, K, K, K, K, B, B, B, B, B, B, B, B, B, B, B, B, B], # 1
         [B, K, K, K, K, K, F, F, F, F, F, F, F, F, F, F, F, B, B], # 2
         [B, K, K, K, K, K, F, C, 1, B, B, 1, C, 2, B, B, B, B, B], # 3
         [B, K, K, K, K, S, F, L, F, F, F, F, L, F, F, F, F, B, B], # 4
         [B, B, C, L, L, C, L, C, L, L, L, L, C, F, F, F, F, B, B], # 5
         [B, B, L, F, F, F, F, L, F, F, F, F, L, F, F, F, F, B, B], # 6
         [B, B, C, 3, B, B, 3, C, 4, B, B, 4, C, 5, B, B, F, B, B], # 7
         [B, B, L, F, F, F, F, L, F, F, F, F, L, F, F, F, F, B, B], # 8
         [B, B, C, L, L, L, L, C, L, L, L, L, C, F, F, F, F, B, B], # 9
         [B, B, L, F, F, F, F, L, F, F, F, F, L, F, F, F, F, B, B], # 10
         [B, B, C, 6, B, B, 6, C, 7, B, B, 7, C, 8, B, B, F, B, B], # 11
         [B, B, L, F, F, F, F, L, F, F, F, F, L, F, F, F, F, B, B], # 12
         [B, B, C, L, L, L, L, C, L, L, L, L, C, F, F, F, F, B, B], # 13
         [B, B, L, F, F, F, F, L, F, F, F, F, L, F, F, F, F, B, B], # 14
         [B, B, C, 9, B, B, 9, C, 10, B, B, 10, C, 11, B, B, F, B, B], # 15
         [B, B, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, B, B], # 16
         [B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B], # 17
         [B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B, B]] # 18

NORTH = 0.0
SOUTH = 180.0
EAST = 270.0
WEST =  90.0