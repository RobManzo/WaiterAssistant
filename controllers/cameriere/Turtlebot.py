from controller import Robot
from Devices import LMotor, RMotor, LDS, Compass, DistanceSensor, PositionSensor, Camera
from LineFollower import LineFollower
from Positioning import Positioning
from Movement import Movement
from CollisionAvoidance import CollisionAvoidance
from Constants import TIMESTEP

class Turtlebot:

    def __init__(self): 
        self.robot = Robot()
        self.lmotor = LMotor(self.robot)
        self.rmotor = RMotor(self.robot)
        self.LDS = LDS(self.robot)
        self.compass = Compass(self.robot)
        self.DSensor = DistanceSensor(self.robot)
        self.positionsensor = PositionSensor(self.robot)
        self.camera = Camera(self.robot)
        self.linefollower = LineFollower(self.camera)
        #self.speaker = Speaker(self.robot)
        self.positioning = Positioning(self.compass)
        self.collisionAvoidance = CollisionAvoidance(self.DSensor, self.LDS)
        self.movement = Movement(self.positioning,self.lmotor,self.rmotor,self.collisionAvoidance)

    def run(self):
        while self.robot.step(TIMESTEP) != -1:
            self.movement.update()
            print(self.LDS.getRangeImage())