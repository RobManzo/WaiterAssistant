from controller import Robot
from Devices import LMotor, RMotor, ProximitySensor, Compass, PositionSensor, Camera, Speaker
from Positioning import Positioning
from Movement import Movement
from CollisionAvoidance import CollisionAvoidance
class Firebird:

    def __init__(self): 
        self.robot = Robot()
        self.lmotor = LMotor(self.robot)
        self.rmotor = RMotor(self.robot)
        self.proximitysensor = ProximitySensor(self.robot)
        self.compass = Compass(self.robot)
        self.positionsensor = PositionSensor(self.robot)
        self.camera = Camera(self.robot)
        self.speaker = Speaker(self.robot)
        self.positioning = Positioning(self.compass, self.camera)
        self.collisionAvoidance = CollisionAvoidance(self.proximitysensor)
        self.movement = Movement(self.positioning,self.lmotor,self.rmotor,self.collisionAvoidance)

    def run(self):
        # for each timestep update services
        while self.robot.step(32) != -1:            
            self.movement.update(self.speaker)
            