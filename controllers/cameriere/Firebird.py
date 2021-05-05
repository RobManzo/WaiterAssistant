from controller import Robot
from Devices import LMotor, RMotor, ProximitySensor, Compass

class Firebird:

    def __init__(self): 
        self.robot = Robot()
        self.lmotor = LMotor(self.robot)
        self.rmotor = RMotor(self.robot)
        self.proximitysensor = ProximitySensor(self.robot)
        self.compass = Compass(self.robot)

    def run(self):
        # for each timestep update services
        while self.robot.step(64) != -1:
            self.lmotor.setVelocity(5.0)
            self.rmotor.setVelocity(5.0)
            print(self.proximitysensor.getDistance())
            print(self.compass.compassToDegree())
            if(self.proximitysensor.getDistance() < 2.0):
                print("AO")
                while(self.compass.compassToDegree() < 179.9 or self.compass.compassToDegree() > 180.1 ):
                    print("WHILE")
                    self.lmotor.setVelocity(1.0)
                    self.rmotor.setVelocity(-1.0)
