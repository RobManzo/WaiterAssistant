from Constants import UNKNOWN
import time

START = 99
#PARKING = 2
#COLLISION_AVOIDANCE = 3
#MANUAL = 4

class ExternalController:

    def __init__(self, keyboard):
        self.keyboard = keyboard
        self.status = False
        self.motionStatus = UNKNOWN

    
    def update(self):
        self.updateCommands()

    def getMotionStatus(self):
        return self.motionStatus

    def updateCommands(self):
        self.keyboard.update()
        # get current key
        currentKey = self.keyboard.getKey()

        # Start
        if self.keyboard.isKeyPressed(currentKey, 's'):
            print("Pressed S.")
            self.motionStatus = 99
        
        # Stop
        elif self.keyboard.isKeyPressed(currentKey, 'p'):
            print("Pressed P.")
            self.motionStatus = 0
        
        elif self.keyboard.isKeyPressed(currentKey, 'm'):
            print ('Going Manual.')
            self.motionStatus = 66

        # return current key to allow other controls 
        return currentKey

    
    def isEnabled(self):
            return self.status != 0

    def enable(self):
        self.status = True

    def disable(self):
        self.status = False
