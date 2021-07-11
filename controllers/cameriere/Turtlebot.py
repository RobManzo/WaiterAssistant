from controller import Robot
from Devices import LMotor, RMotor, Compass, DistanceSensor, PositionSensor, Camera, Keyboard
from LineFollower import LineFollower
from Positioning import Positioning
from Movement import Movement
from CollisionAvoidance import CollisionAvoidance
from Constants import TIMESTEP
from ExternalController import ExternalController
from PathPlanner import PathPlanner
import Map

class Turtlebot:

    def __init__(self): 
        self.robot = Robot()
        self.keyboard = Keyboard(self.robot)
        self.externalcontroller = ExternalController(self.keyboard)
        self.externalcontroller.enable()
        self.lmotor = LMotor(self.robot)
        self.rmotor = RMotor(self.robot)
        self.compass = Compass(self.robot)
        self.DSensor = DistanceSensor(self.robot)
        self.camera = Camera(self.robot)
        self.linefollower = LineFollower(self.camera)
        #self.speaker = Speaker(self.robot)
        self.positionsensor = PositionSensor(self.robot)
        self.positioning = Positioning(self.compass, self.positionsensor)
        self.pathplanner=PathPlanner(self.positioning,self.externalcontroller)
        self.collisionAvoidance = CollisionAvoidance(self.DSensor)
        self.movement = Movement(self.pathplanner,self.positioning,self.lmotor,self.rmotor,self.collisionAvoidance,self.linefollower)
        self.goal = None

    def run(self):
        while self.robot.step(TIMESTEP) != -1:
            if(self.externalcontroller.getMotionStatus() == 99):
                print(self.externalcontroller.getTable())
                self.pathplanner.setGoal(self.externalcontroller.getTable())
                self.movement.update()        #self.goal verrà passato al pathplanner, ad ogni update pathplanner verificherà che l'ordine sia stato consegnato # e restituirà true se è ritornato alla postazione di partenza, nel cas
                self.camera.getImageGray()
            else:
                self.externalcontroller.update()