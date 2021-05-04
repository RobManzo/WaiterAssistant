
#Classe per gestire il motore della ruota sinistra
class LMotor:
    def __init__(self, robot):
        self.lmotor = robot.getDevice('left wheel motor')
        self.lmotor.setVelocity(0.0)
        self.lmotor.setPosition(float('inf'))
    
    def setVelocity(self, speed):
        self.lmotor.setVelocity(speed)
    
    def getVelocity(self):
        return self.lmotor.getVelocity()

#Classe per gestire il motore della ruota destra
class RMotor:
    def __init__(self, robot):
        self.rmotor = robot.getDevice('right wheel motor')
        self.rmotor.setVelocity(0.0)
        self.rmotor.setPosition(float('inf'))
    
    def setVelocity(self, speed):
        self.rmotor.setVelocity(speed)
    
    def getVelocity(self):
        return self.rmotor.getVelocity()

class ProximitySensor:
    def __init__(self, robot):
        # l: left   r: right    f: front    b: back
        self.lSensor = robot.getDevice('ps0')
        self.lfSensor = robot.getDevice('ps1')
        self.fSensor = robot.getDevice('ps2')
        self.rfSensor = robot.getDevice('ps3')
        self.rSensor = robot.getDevice('ps4')
        self.rbSensor = robot.getDevice('ps5')
        self.bSensor = robot.getDevice('ps6')
        self.lbSensor = robot.getDevice('ps7')

        self.lSensor.enable(64)
        self.lfSensor.enable(64)
        self.fSensor.enable(64)
        self.rfSensor.enable(64)
        self.rSensor.enable(64)
        self.rbSensor.enable(64)
        self.bSensor.enable(64)
        self.lbSensor.enable(64)

    def getDistance(self):
        return self.fSensor.getValue()

