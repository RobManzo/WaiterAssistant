from Constants import M_PI, TIMESTEP, UNKNOWN, WHEEL_RADIUS
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
        
    def setLDSVelocity(self, big, small):
        self.LDS_motor_main.setVelocity(big)                 #VELOCITA' MASSIMA MAIN MOTOR LIDAR 40.0
        self.LDS_motor_secondary.setVelocity(small)         #VELOCITA' MASSIMA SECONDARY MOTOR LIDAR 60.0
    
    def getLDSmax(self):
        return self.LDS_motor_main.getMaxVelocity()
    
    def getRangeImage(self):
        return self.LDS.getRangeImage()
    
    def getLayerPointCloud(self):
        return self.LDS.getLayerPointCloud(0)
    
    def getNumberOfLayers(self):
        return self.LDS.getNumberOfLayers()

    def getLayerRangeImage(self):
        return self.LDS.getLayerRangeImage(0)
    
    def getRangeImage(self):
        return self.LDS.getRangeImage()

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
        self.error=0
        self.i=1

    def getDistanceTraveled(self):
        self.distance=float((self.getLeftSensor()*WHEEL_RADIUS + self.getRightSensor()*WHEEL_RADIUS)/4)     #Multiply rad/s * wheel radius in order to obtain mean distance travelled, rotation not affected
        return self.distance-self.error

    def resetDistanceTraveled(self):
        self.error=self.distance
        
    def getLeftSensor(self):
        return self.leftpos.getValue()
    
    def getRightSensor(self):
        return self.rightpos.getValue()
        
class DistanceSensor:
    def __init__(self, robot):
        self.DSensor = robot.getDevice("DSENSOR-SHARP-FRONT")
        self.DSensor.enable(TIMESTEP)

    def getValue(self):
        return self.DSensor.getValue()

class Camera:
    def __init__(self, robot):
        self.camera = robot.getDevice("camera")
        self.camera.enable(TIMESTEP)
    
    # return camera image in array form
    def getImageArray(self):
        return self.camera.getImageArray()      

    def getImageGray(self):
        image=self.camera.getImage()
        red=self.camera.imageGetRed(image,self.getWidth(),128,55)
        green=self.camera.imageGetGreen(image,self.getWidth(),128,55)
        blue=self.camera.imageGetBlue(image,self.getWidth(),128,55)
        #print(red)
        #print(green)
        #print(blue)

    def getWidth(self):
        return self.camera.getWidth()
    
    def getHeight(self):
        return self.camera.getHeight()

class Keyboard:
    def __init__(self, robot):
        self.keyboard = robot.getKeyboard()
        self.keyboard.enable(64)
        self.pressedKey = UNKNOWN

    def getKey(self):
        return self.pressedKey

    def update(self):
        self.pressedKey = self.keyboard.getKey()

    # return true if char key or his uppercase is pressed
    def isKeyPressed(self, key, char):
        return key == ord(char) or key == ord(char.upper())


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