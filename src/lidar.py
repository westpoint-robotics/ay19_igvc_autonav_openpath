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
	urg_list = data.ranges

def mode_callback(data):
	global mode
	mode= data.data

def loop():
	#plt.clf()
	global sign, angle

	#print urg_list
	
	pw=.47 #width of the robot	
		
	ranges=[] #initialize array to store maximum distance that
			  #robot can travel at each beam
	beam_cut=1
	if len(urg_list)>0: #only run once a beam array has been recieved	
		for i in range(0,len(urg_list),beam_cut):		
			ran =  urg_list[i] #range for path checking
			max_dist = urg_list[i] #this variable will be used to store the
								   #max distance that the robot can travel
			check = True
			for k in range (0,20):
				if check: 				
					#how many degrees should be checked for the given range
					ran2= k * (ran/20)			
					width = 2 * numpy.degrees(numpy.arctan(pw/2))/ran2
					width = (width * 4)/ 2 #resolution of hokuyo is .25 degrees, so
										   #there are four array elements per degree
							
					lower_width=width #differentiate width for array bounds checking
					if (i+width)>1080:
						width = 1080-i #if the width will exceed the max of the array
									   #then only check until the end of the array
					if (i-lower_width)<0:
						lower_width=i  #same concept for lower bound of array
					#check if any ranges are closer in the path of the robot
					for j in range (i-int(lower_width),i+int(width)):
						if urg_list[j]<ran2:
							max_dist= urg_list[j]
							check=False		
					#add maximum distance the robot can travel for this beam to array
			ranges.append(max_dist)

		global drive

		#rospy.loginfo(str(ranges))
		
		#if the most open path is outside of 16 degrees in front of robot, steer
		angle=3.1416
		if ranges[((1080/2)/beam_cut)]>2.3:
			drive.publish('ff')
			angle=3.2		
		elif ranges[((1080/2)/beam_cut)]>1.5:
			drive.publish('f')
			angle=3.3
		elif max(ranges)<.5:
			drive.publish('cwf')
		elif ranges.index(max(ranges)) < 0+((1080/beam_cut)/3):
			drive.publish('cwf')
		elif ranges.index(max(ranges)) < ((1080/2)/beam_cut)-((5*4)/beam_cut):
			drive.publish('cw')
		elif ranges.index(max(ranges)) > ((1080/2)/beam_cut)+((5*4)/beam_cut):
			drive.publish('ccw')
		elif ranges.index(max(ranges)) > (1080/beam_cut)-(1080/beam_cut)/3:
			drive.publish('ccwf')
		else:
			drive.publish('f')	
		
		hok_ang.publish(angle)
#plt.plot([i*.25+width/2,i*.25-width/2],[ran,ran],'b-')
		
def main():
	rospy.init_node("lidar")

	rate = rospy.Rate(30)	
	
	rospy.Subscriber("/scan", LaserScan, urg_callback)
	rospy.Subscriber("/out/mode",String, mode_callback)	

	global drive

	drive = rospy.Publisher("/out/drive",String)
	
	global hok_ang, sign, angle
	hok_ang = rospy.Publisher("/hokuyo_motor/command", Float64)
	
	hok_ang.publish("3.1416")
	sign = 1
	angle = 3.1416

	#plt.show()
	#plt.pause(0.0001)
	global mode
	mode='stop'
	while not rospy.is_shutdown():		
		if mode == 'lidar':		
			loop()
		rate.sleep()

main()
