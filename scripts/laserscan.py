#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import LaserScan

def scan_callback(data):
    global my_laser
    my_laser = data
    time = rospy.Time.now()
    my_laser.header.stamp = time
    my_laser.header.frame_id = "Turtlebot/LDS_01"
    
rospy.init_node("scan", anonymous=True)
r = rospy.Rate(1)

my_laser = LaserScan()
sub = rospy.Subscriber("/Turtlebot/LDS_01/laser_scan/layer0", LaserScan, scan_callback)
message_pub = rospy.Publisher("scan", LaserScan, queue_size=50)

while not rospy.is_shutdown():
    message_pub.publish(my_laser)
    r.sleep()
