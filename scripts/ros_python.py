#!/usr/bin/env python3

import rospy
import time
import os
import turtlebot_pkg.utils as Utils
from turtlebot_pkg.lidar import Lidar

rospy.init_node('my_robot', anonymous=True)

HOST = os.popen('whoami').read().strip('\n')
#PATH = f"/home/{HOST}/catkin_ws/src/webots_ros/config/"

#f = open(f"{PATH}info.json", "r")
#data = json.load(f)
#f.close()

if __name__ == '__main__':
    try:
        lidar = Lidar()
        time.sleep(3)
        i = 0
    except rospy.ROSInterruptException:
        pass

