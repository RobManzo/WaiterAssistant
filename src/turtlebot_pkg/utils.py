#!/usr/bin/env python3

import rospy
import rosservice
import math

# Caratteristiche robot
robot_name = 'Turtlebot'
max_speed = 2.84 #rad/s
#laser_range = ?? #m
height = 0.384 #m
weight = 15 #kg
#footprint = ?? #m
wheel_distance = 0.32 #m
wheel_radius = 0.066 #m
wheel_circum = 2 * math.pi * wheel_radius #m

timestep = 32

def call_service(device_name, service_name, *args):
	service_string = "/%s/%s/%s" % (robot_name, device_name, service_name)
	rospy.loginfo(service_string)
	rospy.wait_for_service(service_string)
	try:
		service = rospy.ServiceProxy(service_string, rosservice.get_service_class_by_name(service_string))
		response = service(*args)
		rospy.loginfo("Service %s called" % service_string)
		return response
	except rospy.ServiceException as e:
		rospy.logerr("Service call failed: %s" % e)