#! /usr/bin/env python

import imp
from pydoc import cli
import rospy
import time
import actionlib
from geometry_msgs.msg import Twist
from ardrone_as.msg import ArdroneAction, ArdroneGoal, ArdroneFeedback, ArdroneResult

nImage = 1

ACTIVE = 1
DONE = 2
WARN = 3
ERROR = 4

def feedback_callback(feedback):
    global nImage
    rospy.loginfo("[Feedback] Image n.%d received"%nImage)
    nImage += 1


rospy.init_node("drone_action_client")

pub = rospy.Publisher("cmd_vel", Twist, queue_size=1)
twist_cmd = Twist()
twist_cmd.linear.x = 0.5
twist_cmd.linear.z = 0.5
twist_cmd.angular.z = 0.1

client = actionlib.SimpleActionClient("ardrone_action_server", ArdroneAction)
client.wait_for_server()
goal = ArdroneGoal()
goal.nseconds = 10
client.send_goal(goal, feedback_cb=feedback_callback)

rate = rospy.Rate(1)
state_result = client.get_state()

while state_result < DONE:
    pub.publish(twist_cmd)
    state_result = client.get_state()
    rospy.loginfo("state_result %d"%state_result)
pub.publish(Twist())

rospy.loginfo("[Result] State: %d"%client.get_state())

if state_result == WARN:
    rospy.logwarn("There was a warning while executing the action")
elif state_result == ERROR:
    rospy.logerr("There was an error while executing the actions")
