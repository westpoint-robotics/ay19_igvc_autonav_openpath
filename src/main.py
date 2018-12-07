#!/usr/bin/python

import rospy
from sensor_msgs.msg import LaserScan
import matplotlib.pyplot as plt
import numpy

global urg_list
urg_list = []

def urg_callback(data):
	global urg_list
	urg_list = data.ranges

def loop():
	plt.clf()

	print urg_list

	for i in range(0,len(urg_list)):
		plt.plot(i,urg_list[i],'bo')

	plt.draw()
	plt.pause(0.0001)

def main():
	rospy.init_node("stembot")

	#rate = rospy.Rate(5)	
	
	rospy.Subscriber("/scan", LaserScan, urg_callback)
	
	plt.show()
	plt.pause(0.0001)

	while not rospy.is_shutdown():
		loop()
		#rate.sleep()

main()
