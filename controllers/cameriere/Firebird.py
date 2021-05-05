from controller import Robot
from Devices import LMotor, RMotor, ProximitySensor, Compass
from Positioning import Positioning
from Movement import Movement
class Firebird:

    def __init__(self): 
        self.robot = Robot()
        self.lmotor = LMotor(self.robot)
        self.rmotor = RMotor(self.robot)
        self.proximitysensor = ProximitySensor(self.robot)
        self.compass = Compass(self.robot)
        self.positioning = Positioning(self.compass)
        self.movement= Movement(self.positioning,self.lmotor,self.rmotor)

    def run(self):
        # for each timestep update services
        while self.robot.step(64) != -1:            
            self.positioning.update()
            self.movement.update()
