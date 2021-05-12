M_PI = 3.14
import math

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

        self.lSensor.enable(32)
        self.lfSensor.enable(32)
        self.fSensor.enable(32)
        self.rfSensor.enable(32)
        self.rSensor.enable(32)
        self.rbSensor.enable(32)
        self.bSensor.enable(32)
        self.lbSensor.enable(32)

class Compass:
    def __init__(self, robot):
        self.compass_xy = robot.getDevice('compassXY_01')
        self.compass_z = robot.getDevice('compassZ_01')
        self.compass_xy.enable(32)
        self.compass_z.enable(32)

    def getCompass(self):
        self.compassXY = self.compass_xy.getValues()
        self.compassZ = self.compass_z.getValues()
        return  [self.compassXY[0], self.compassXY[1], self.compassZ[2]]

    def compassToDegree(self):
        north = self.getCompass()
        rad = math.atan2(north[0], north[2])
        bearing = (rad - 1.5708) / M_PI * 180.0
        if(bearing < 0):
            bearing += 360.0
        return round(float(bearing), 6)
    
class PositionSensor:
    def __init__(self, robot):
        self.leftpos = robot.getDevice('left wheel sensor')
        self.rightpos = robot.getDevice('right wheel sensor')
        self.leftpos.enable(32)
        self.rightpos.enable(32)

    def getDistanceTraveled(self):
        return self.leftpos.getValue(), self.rightpos.getValue()

class Camera:
    def __init__(self, robot):
        self.camera = robot.getDevice('camera')
        self.camera.enable(32)
        self.camera.recognitionEnable(32)
    
    def getFov(self):
        return self.camera.getFov()