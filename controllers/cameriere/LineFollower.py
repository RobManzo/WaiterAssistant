# Compute steering angle using camera images
from Constants import UNKNOWN
#from Utils import logger

# constants  
NUM_ZONES = 3         # number of vertical zones of the image
MAX_STEERING_ANGLE = 1  # max steering angle allow to line following
MIN_STEERING_ANGLE = -1 # min steering angle allow to line folloving

# compute steering angle step for each zone of the image
STEERING_ANGLE_STEP = ((MAX_STEERING_ANGLE - MIN_STEERING_ANGLE) / NUM_ZONES)

# compute middle zone index
MIDDLE_ZONE = int(NUM_ZONES/2)

# set line reference color and tolerance 
LINE_REFERENCE_COLOR = [0, 0, 0] # black
LINE_COLOR_TOLERANCE = 60

# class to handle line following
class LineFollower:

    def __init__(self, camera):
        # get camera from Altino
        self.camera = camera    

        # get image dimensions
        self.cameraWidth = camera.getWidth()
        self.cameraHeight = camera.getHeight()

        # initialize image zone counters
        self.zones = []
        for i in range(NUM_ZONES):
            self.zones.append(0)

        # compute zone width, the image is dived in NUM_ZONES vertically of zoneSpace width
        self.zoneSpace = self.cameraWidth / NUM_ZONES

        # true if line is lost
        self.lineLost = False

        self.isCrossRoad=False
        
        #speeds
        self.rightSpeed=0

        self.leftSpeed=0
        
        self.adjust=False
        self.crossRoadPass=False

        # angle to be set to follow the line
        self.newSteeringAngle = UNKNOWN

        # index of the last zone with the yellow line detected
        self.lastLineKnownZone = UNKNOWN

    def getAdjust(self):
        return self.adjust
    def getRightSpeed(self):
        return self.rightSpeed
    def getLeftSpeed(self):
        return self.leftSpeed
    def getCrossRoad(self):
        return self.crossRoadPass    
    def setLineLost(self):
        self.lineLost=False
    # process data from camera
    def processCameraImage(self):
        # if no pixel of line reference color is found, the line is lost
        # clear zone's pixel count
        self.crossRoadPass=False
        for i in range(NUM_ZONES):
            self.zones[i] = 0

        # get image from camera
        image = self.camera.getImageArray()

        # scanning column by column
        for i in range(self.cameraWidth):
            for j in range(self.cameraHeight):
                # if pixel is similar to line reference color add pixel to zone count
                if self.colorDifference(image[i][j]) < LINE_COLOR_TOLERANCE:
                    self.zones[int(i / self.zoneSpace)] += 1
        
        # lost line
        

        # find index of greatest zone
        index = self.zones.index(max(self.zones))
        print(index)
        if index != -1:
            self.lastLineKnownZone = index

        # debug
        print(self.zones)

        # if the middle zone is the greatest return 0
        if sum(self.zones) == 0:
            #logger.debug("Last known line: " + str(self.lastLineKnownZone))
            self.lineLost=True
            print("LINE LOST")
        else: 
            self.lineLost=False
            
        if self.zones[0]==0:
            self.leftSpeed=2
            self.rightSpeed=-0.5
            print("left")
            # return angle according to greatest zone
            
        elif self.zones[2]==0:
            print("right")
            self.rightSpeed=2
            self.leftSpeed=-0.5
            # return angle according to greatest zone
        elif self.zones[0]>1500 and self.zones[1]>1500 and self.zones[2]>1500:
            self.isCrossRoad=True
            print("CROSSROAD")
        elif self.isCrossRoad:
            print("Questo else")
            self.leftSpeed=-3.0
            self.rightSpeed=-3.0
            self.isCrossRoad=False
            self.crossRoadPass=True
        elif self.zones[2]-self.zones[0]>100:
            self.leftSpeed=0.2
            print("adj1")
        elif self.zones[0]-self.zones[2]>100:
            self.rightSpeed=0.2    
            print("Adj2")
        #elif abs(self.zones[0]-self.zones[2]<300) and not self.isCrossRoad:
         #   print("ADJUST")
          #  self.adjust=True
        elif index == MIDDLE_ZONE and self.zones[0]<1200 and self.zones[2]<1200 and not self.isCrossRoad:
            self.leftSpeed=0
            self.rightSpeed=0
            print("Normal Behaviour")       
        else:
            print("Final else")
            self.leftSpeed=0
            self.rightSpeed=0
            
    # compute index of greatest value in the array
    def indexOfMax(self, array):
        index = -1
        max = array[0]
        for i in range(1, NUM_ZONES - 1):
            if array[i] > max:
                max = array[i]
                index = i
        
        return index
    
    # compute color difference
    def colorDifference(self, pixelColor):
        difference = 0
        difference += abs(pixelColor[0] - LINE_REFERENCE_COLOR[0])
        difference += abs(pixelColor[1] - LINE_REFERENCE_COLOR[1])
        difference += abs(pixelColor[2] - LINE_REFERENCE_COLOR[2])

        return difference

    # update steering angle
    def update(self):
        self.processCameraImage()
        print("IS CROSSROAD:"+str(self.getCrossRoad()))
        

    # return steereng angle
    def getNewSteeringAngle(self):
        return self.newSteeringAngle

    # return if line is lost
    def isLineLost(self):
        return self.lineLost

    # return steereng angle based on last index where the line appeared, is usually called when line is lost
    def getSteeringAngleLineSearching(self):
        if self.lastLineKnownZone == MIDDLE_ZONE:
            return 0
         
        return (MIN_STEERING_ANGLE + self.lastLineKnownZone * STEERING_ANGLE_STEP) * 1

    # reset last line zone, this allow external control to line search
    def resetLastLineKnownZone(self, angle=0):
        if angle != 0 :
            self.lastLineKnownZone = int((angle - MIN_STEERING_ANGLE) / STEERING_ANGLE_STEP)
        else:
            self.lastLineKnownZone=MIDDLE_ZONE
            
        