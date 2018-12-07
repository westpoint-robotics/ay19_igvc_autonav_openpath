#!/usr/bin/python

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Joy
import numpy

global buttons, axes
buttons= [0,0,0,0,0,0,0,0,0,0,0]
axes=[0,0,0,0,0,0,0,0]

def joy_callback(data):
	global buttons, axes
	buttons = data.buttons
	axes = data.axes

def mode_callback(data):
	global mode
	mode= data.data

def loop():
	state()

def state():
	global buttons, axes, drive
	if axes[1] > .8:
		drive.publish('ff')
	elif buttons[3] == 1 or axes[1] > .3:
		drive.publish('f')
	elif buttons[0] == 1 or axes[1] < -.3:
		drive.publish('r')
	elif buttons[2] == 1 or axes[0]>.3:
		drive.publish('ccwf')
	elif buttons[1] == 1 or axes[0]<-.3:
		drive.publish('cwf')
	else:
		drive.publish('s')


def drive():
	rospy.init_node("joy_control")

	rate = rospy.Rate(60)	
	
	rospy.Subscriber("/joy", Joy, joy_callback)
	rospy.Subscriber("/out/mode",String,mode_callback)
	
	global drive
	drive = rospy.Publisher("/out/drive",String)	
	global mode_pub
	mode_pub = rospy.Publisher("/out/mode",String)	
	global mode
	mode='stop'
	while not rospy.is_shutdown():
		if mode == 'joy':		
			loop()
		elif mode == 'stop':
			drive.publish('s')
		global buttons
		if (not mode =='joy') and buttons[8]:
			mode_pub.publish("joy")
			buttons=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		elif buttons[8]:
			mode_pub.publish("lidar")
			buttons=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		rate.sleep()

drive()
