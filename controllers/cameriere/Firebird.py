from controller import Robot
from Devices import Devices
from Constants import Constants

RUN = 1
STOP = 2

class Firebird:

    def __init__(self):
        self.status = STOP
        self.robot = Robot()
        self.lmotor = Devices.LMotor(robot)
        self.rmotor = Devices.RMotor(robot)

    def run(self):
        logger.info("Firebird è pronto.")
        self.status = RUN
        # for each timestep update services
        while self.robot.step(64) != -1 and self.status == RUN:
            self.lmotor.setVelocity(5.0)
            self.rmotor.setVelocity(5.0)

