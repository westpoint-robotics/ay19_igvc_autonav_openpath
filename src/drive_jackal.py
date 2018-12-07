#!/usr/bin/python

import rospy
from geometry_msgs.msg import Twist
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
	global move_cmd, cmd_vel
	move_cmd.linear.x=0
	move_cmd.angular.z=0
	cmd_vel.publish(move_cmd)

def state():
	global command, move_cmd, cmd_vel
	if command == 's':
		move_cmd.linear.x=0
		move_cmd.angular.z=0
	if command == 'cw':
		move_cmd.linear.x=0
		move_cmd.angular.z=-.5
	if command == 'ccw':
		move_cmd.linear.x=0
		move_cmd.angular.z=.5
	if command == 'cwf':
		move_cmd.linear.x=0
		move_cmd.angular.z=-1
	if command == 'ccwf':
		move_cmd.linear.x=0
		move_cmd.angular.z=1
	if command == 'f':
		move_cmd.linear.x=.2
		move_cmd.angular.z=0
	if command == 'ff':
		move_cmd.linear.x=.4
		move_cmd.angular.z=0
	if command == 'r':
			move_cmd.linear.x=-.1
			move_cmd.angular.z=0
	cmd_vel.publish(move_cmd)
	rospy.loginfo("I published "+str(move_cmd))
		

def drive():
	rospy.init_node("drive")

	rate = rospy.Rate(60)	
	
	rospy.Subscriber("/out/drive", String, drive_callback)
	
	global cmd_vel,move_cmd
	cmd_vel = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
	
	move_cmd = Twist()

	rospy.on_shutdown(stop_motors)

	while not rospy.is_shutdown():
		loop()
		rate.sleep()

drive()
