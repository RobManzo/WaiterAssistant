from Constants import M_PI, TIMESTEP
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

    def getMaxVelocity(self):
        return self.lmotor.getMaxVelocity()

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
    
    def getMaxVelocity(self):
        return self.rmotor.getMaxVelocity()

class LDS:
    def __init__(self, robot):
        self.LDS = robot.getDevice('LDS-01')
        self.LDS.enable(TIMESTEP)
        self.LDS.enablePointCloud()
        self.LDS_motor_main = robot.getDevice('LDS-01_main_motor')
        self.LDS_motor_main.setPosition(float('inf'))
        self.LDS_motor_secondary = robot.getDevice('LDS-01_secondary_motor')
        self.LDS_motor_secondary.setPosition(float('inf'))
        
    
    def setLDSVelocity(self, big, small):
        self.LDS_motor_main.setVelocity(big)                 #VELOCITA' MASSIMA MAIN MOTOR LIDAR 40.0
        self.LDS_motor_secondary.setVelocity(small)         #VELOCITA' MASSIMA SECONDARY MOTOR LIDAR 60.0
    
    def getLDSmax(self):
        return self.LDS_motor_main.getMaxVelocity()
    
    def getRangeImage(self):
        return self.LDS.getRangeImage()
    
    def getLayerPointCloud(self):
        return self.LDS.getLayerPointCloud(data_type='list')
    
    def getNumberOfLayers(self):
        return self.LDS.getNumberOfLayers()
    
    def getFOV(self):
        return self.LDS.getFov()


class Compass:
    def __init__(self, robot):
        self.compass_xy = robot.getDevice('compass')
        self.compass_xy.enable(TIMESTEP)

    def getCompass(self):
        self.compassXY = self.compass_xy.getValues()
        return  [self.compassXY[0], self.compassXY[1], self.compassXY[2]]

    def compassToDegree(self):
        north = self.getCompass()
        rad = (math.atan2(north[0], north[1]))
        bearing = ((rad - 1.5708) / M_PI) * 180.0
        if(bearing <= 0):
            bearing += 360.0
        return round(float(bearing), 2)
    
class PositionSensor:
    def __init__(self, robot):
        self.leftpos = robot.getDevice('left wheel sensor')
        self.rightpos = robot.getDevice('right wheel sensor')
        self.leftpos.enable(TIMESTEP)
        self.rightpos.enable(TIMESTEP)

    def getDistanceTraveled(self):
        return self.leftpos.getValue(), self.rightpos.getValue()

class DistanceSensor:
    def __init__(self, robot):
        self.DSensor = robot.getDevice("DSENSOR-SHARP")
        self.DSensor.enable(TIMESTEP)

    def getValue(self):
        return self.DSensor.getValue()

#class Speaker:
#    def __init__(self, robot):
#        self.speaker = robot.getDevice('speaker')
#        self.speaker.setLanguage('it-IT')
#        self.speaker.setEngine('microsoft')
#    
#    def speak(self, text, volume):
#        self.speaker.speak(text, volume)
#    
#    def isSpeaking(self):
#        if self.speaker.isSpeaking():
#            return True
#        else: return False
#