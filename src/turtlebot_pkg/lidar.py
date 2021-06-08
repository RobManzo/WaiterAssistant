#!/usr/bin/env python3

import rospy
import tiago_pkg.utils as Utils
from sensor_msgs.msg import Image

class Lidar(object):

    image = Image()

    def __init__(self):
        self.enable_lidar()
        self.image_sub = rospy.Subscriber(Utils.robot_name + "/Hokuyo_UTM_30LX/range_image", Image, self.image_callback)
            
    def enable_lidar(self):
        Utils.call_service('Hokuyo_UTM_30LX', 'enable', 1)
        Utils.call_service('Hokuyo_UTM_30LX', 'enable_point_cloud', True)

    def get_info(self):
        resp = Utils.call_service('Hokuyo_UTM_30LX', 'get_info', 1)
        lidar_width = resp.horizontalResolution
        lidar_max_range = resp.maxRange
        return (lidar_width, lidar_max_range)
    
    def image_callback(self, data):
        self.image = data
        
    def get_image_data(self):
        return self.image.data
