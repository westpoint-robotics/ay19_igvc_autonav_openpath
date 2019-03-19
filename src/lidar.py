#!/usr/bin/python

import rospy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String, Float64
import matplotlib.pyplot as plt
import numpy

global urg_list
urg_list = []

def urg_callback(data):
	global urg_list
	urg_list = list(data.ranges)
	#for i in range(0,len(urg_list)):
	#	urg_list[i] = urg_list[i]

def mode_callback(data):
	global mode
	mode= data.data

def loop():
	#plt.clf()
	global sign, angle

	#print urg_list

	pw=1.3 #width of the robot

	ranges=[] #initialize array to store maximum distance that
			  #robot can travel at each beam
	beam_cut=1

	#rospy.loginfo(len(urg_list))
	#rospy.loginfo(urg_list)
	if len(urg_list)>0: #only run once a beam array has been recieved
		num_beams = len(urg_list)
		for i in range(0,len(urg_list),beam_cut):
			ran =  urg_list[i] #range for path checking
			if ran==float("Inf"):
				ran=15.0
			if ran==float("NaN"):
				ran=0.0
			if ran<0.01:
				ran=.05
			max_dist = urg_list[i] #this variable will be used to store the
								   #max distance that the robot can travel
			check = True
			for k in range (0,20):
				if check:
					#how many degrees should be checked for the given range
					ran2= k * (ran/20)
					width = 2 * numpy.degrees(numpy.arctan(pw/2))/ran2
					width = 3*(width)/ 2 #resolution of hokuyo is .25 degrees, so
										   #there are four array elements per degree

					lower_width=width #differentiate width for array bounds checking
					if (i+width)>num_beams:
						width = num_beams-i #if the width will exceed the max of the array
									   #then only check until the end of the array
					if (i-lower_width)<0:
						lower_width=i  #same concept for lower bound of array
					#check if any ranges are closer in the path of the robot
					for j in range (i-int(lower_width),i+int(width)):
						if urg_list[j]<ran2:
							max_dist= urg_list[j]
							if(max_dist>.1):
								check=False
					#add maximum distance the robot can travel for this beam to array
			ranges.append(max_dist)

		global drive

		#rospy.loginfo(str(ranges))

		#if the most open path is outside of 16 degrees in front of robot, steer

		if(ranges[int((num_beams/2)/beam_cut)]>.01):
			#rospy.loginfo(num_beams)
			if ranges[int((num_beams/2)/beam_cut)]>2:
				drive.publish('ff')
				angle=3.2
			elif ranges[int((num_beams/2)/beam_cut)]>1.0:
				drive.publish('f')
				angle=3.3
			elif max(ranges)<.5:
				drive.publish('cwf')
			elif ranges.index(max(ranges)) < 0+((num_beams/beam_cut)/3):
				drive.publish('cwf')
			elif ranges.index(max(ranges)) < ((num_beams/2)/beam_cut)-((10)/beam_cut):
				drive.publish('cw')
			elif ranges.index(max(ranges)) > ((num_beams/2)/beam_cut)+((10)/beam_cut):
				drive.publish('ccw')
			elif ranges.index(max(ranges)) > (num_beams/beam_cut)-(num_beams/beam_cut)/3:
				drive.publish('ccwf')
			else:
				drive.publish('f')


#plt.plot([i*.25+width/2,i*.25-width/2],[ran,ran],'b-')

def main():
	rospy.init_node("lidar")

	rate = rospy.Rate(30)

	rospy.Subscriber("/scan", LaserScan, urg_callback)
	rospy.Subscriber("/out/mode",String, mode_callback)

	global drive

	drive = rospy.Publisher("/out/drive",String)

	#plt.show()
	#plt.pause(0.0001)
	global mode
	mode='stop'
	while not rospy.is_shutdown():
		if mode == 'lidar':
			loop()
		rate.sleep()

main()
