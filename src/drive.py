#!/usr/bin/python

import rospy
from std_msgs.msg import Float64, String
import numpy

global command
command= 's'

def drive_callback(data):
	global command
	command = data.data

def loop():
	state()

def stop_motors():
	global left_motor, right_motor
	left_motor.publish(0)
	right_motor.publish(0)

def state():
	global command, left_motor, right_motor
	if command == 's':
		left_motor.publish(0)
		right_motor.publish(0)
	if command == 'cw':
		left_motor.publish(.5)
		right_motor.publish(.5)
	if command == 'ccw':
		left_motor.publish(-.5)
		right_motor.publish(-.5)
	if command == 'cwf':
		left_motor.publish(1)
		right_motor.publish(1)
	if command == 'ccwf':
		left_motor.publish(-1)
		right_motor.publish(-1)
	if command == 'f':
		left_motor.publish(4)
		right_motor.publish(-4)
	if command == 'ff':
		left_motor.publish(10000)
		right_motor.publish(-10000)
	if command == 'r':
			left_motor.publish(-2)
			right_motor.publish(2)
		

def drive():
	rospy.init_node("drive")

	rate = rospy.Rate(60)	
	
	rospy.Subscriber("/out/drive", String, drive_callback)
	
	global left_motor, right_motor
	left_motor = rospy.Publisher("/left_motor/command",Float64)
	right_motor= rospy.Publisher("/right_motor/command",Float64)	

	rospy.on_shutdown(stop_motors)

	while not rospy.is_shutdown():
		loop()
		rate.sleep()

drive()
