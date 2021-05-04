from controller import Robot
from Devices import LMotor, RMotor, ProximitySensor

class Firebird:

    def __init__(self): 
        self.robot = Robot()
        self.lmotor = LMotor(self.robot)
        self.rmotor = RMotor(self.robot)
        self.ProximitySensor = ProximitySensor(self.robot)

    def run(self):
        # for each timestep update services
        while self.robot.step(64) != -1:
            self.lmotor.setVelocity(5.0)
            self.rmotor.setVelocity(5.0)
            print(self.ProximitySensor.getDistance())
            if(self.ProximitySensor.getDistance() < 2.0):
                self.lmotor.setVelocity(0.0)
                self.rmotor.setVelocity(0.0)


            

