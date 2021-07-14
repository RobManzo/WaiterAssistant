from controller import Robot
from Devices import LMotor, RMotor, Compass, DistanceSensor, PositionSensor, Camera, Keyboard
from LineFollower import LineFollower
from Positioning import Positioning
from Movement import Movement
from CollisionAvoidance import CollisionAvoidance
from Constants import TIMESTEP,INSERT,MOVING,BASE,STOP
from ExternalController import ExternalController
from PathPlanner import PathPlanner

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
        self.positionsensor = PositionSensor(self.robot)
        self.positioning = Positioning(self.compass, self.positionsensor)
        self.pathplanner=PathPlanner(self.positioning,self.externalcontroller)
        self.collisionAvoidance = CollisionAvoidance(self.DSensor)
        self.movement = Movement(self.pathplanner,self.positioning,self.lmotor,self.rmotor,self.collisionAvoidance, self.linefollower, self.externalcontroller)

    def run(self):
        print("inserire Tavolo")
        while self.robot.step(TIMESTEP) != -1:
            if(self.externalcontroller.getMotionStatus() and self.movement.getStatus() == STOP):
                
                self.movement.setStatus(INSERT)
            elif(self.movement.getStatus() == INSERT):
                
                self.pathplanner.setGoal(self.externalcontroller.getTable())
                self.movement.setStatus(MOVING)
            elif(self.externalcontroller.getMotionStatus() and self.movement.getStatus() == MOVING):                    
                self.movement.update() 
                self.camera.getImageGray()
            else:
                self.externalcontroller.update()