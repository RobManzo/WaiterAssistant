from controller import Robot
from Devices import LMotor, RMotor, ProximitySensor, Compass, PositionSensor, Camera
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
        self.positioning = Positioning(self.compass)
        self.collisionAvoidance = CollisionAvoidance(self.proximitysensor)
        self.movement = Movement(self.positioning,self.lmotor,self.rmotor,self.collisionAvoidance)
        self.currentblock = 90
        self.counter = 0
        

    def run(self):
        # for each timestep update services
        while self.robot.step(32) != -1:            
            self.updateBlock(self.camera)
            self.movement.update()
            print("Block Counter : " + self.counter.__str__())

    def updateBlock(self, camera):
        self.image = camera.getImage()
        self.nextblock = camera.getGrayScale(self.image, self.camera.getWidth(), 64, 64)
        if self.checkNextBlock(self.currentblock, self.nextblock):
            self.setCurrentBlock(self.nextblock)
            self.counter += 1


    def checkNextBlock(self, currentblock, nextblock):
        if currentblock < 110 and nextblock > 110:
            return True
        elif currentblock > 110 and nextblock < 110:
            return True
        else: return False

    def setCurrentBlock(self, newblock):
        self.currentblock = newblock    