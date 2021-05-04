from Constants import Constants

#Classe per gestire il motore della ruota sinistra
class LMotor:
    def __init__(self, robot):
        self.lmotor = robot.getDevice('left wheel motor')
        self.lmotor.setVelocity(0.0)
    
    def setVelocity(self, speed):
        self.lmotor.setVelocity = speed
    
    def getVelocity(self):
        return self.lmotor.getVelocity()

#Classe per gestire il motore della ruota destra
class RMotor:
    def __init__(self, robot):
        self.rmotor = robot.getDevice('right wheel motor')
        self.rmotor.setVelocity(0.0)
    
    def setVelocity(self, speed):
        self.rmotor.setVelocity = speed
    
    def getVelocity(self):
        return self.rmotor.getVelocity()

