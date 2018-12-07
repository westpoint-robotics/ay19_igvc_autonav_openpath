#!/usr/bin/python

import os
import rospy
from std_msgs.msg import String
import sys
from PyQt4 import QtGui, QtCore

def start():
	global mode
	mode.publish('lidar')

def stop():
	global mode
	mode.publish('stop')

def joy():
	global mode
	mode.publish('joy')

def kill():
	os.system("shutdown now")
	

def shutdown():
	QtCore.QCoreApplication.instance().quit()

def init():
	rospy.init_node("gui")
	app = QtGui.QApplication(sys.argv)

	global mode
	mode = rospy.Publisher("/out/mode", String)

	w = QtGui.QWidget()
	w.setWindowTitle("Control")
	w.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
	w.resize(120,400)
	w.move(680,40)	
	

	btn=QtGui.QPushButton('Start',w)
	btn.clicked.connect(start)
	btn.resize(100,100)
	btn.move(10,10)

	btn2=QtGui.QPushButton('Stop',w)
	btn2.clicked.connect(stop)
	btn2.resize(100,100)
	btn2.move(10,120)

	btn3=QtGui.QPushButton('Joy',w)
	btn3.clicked.connect(joy)
	btn3.resize(100,100)
	btn3.move(10,230)
	
	btn4=QtGui.QPushButton('I/O',w)
	btn4.clicked.connect(kill)
	btn4.resize(50,50)
	btn4.move(35,340)
	
	w.show()
	
	rospy.on_shutdown(shutdown)
	sys.exit(app.exec_())
	while not rospy.is_shutdown():
		pass

init()
