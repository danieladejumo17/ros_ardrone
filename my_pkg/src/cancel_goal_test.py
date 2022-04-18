#! /usr/bin/env python

from os import stat
from telnetlib import DO
import rospy
import time
import actionlib
from ardrone_as.msg import ArdroneAction, ArdroneGoal, ArdroneFeedback, ArdroneResult

nImage = 1

ACTIVE = 1
DONE = 2
WARN = 3
ERROR = 4

def feedback_callback(feedback):
    global nImage
    print("[Feedback] Image n.%d received"%nImage)
    nImage += 1

rospy.init_node("drone_action_client")

client = actionlib.SimpleActionClient("ardrone_action_server", ArdroneAction)

client.wait_for_server()

goal = ArdroneGoal()
goal.nseconds = 10

client.send_goal(goal, feedback_cb=feedback_callback)

rate = rospy.Rate(1)
state_result = client.get_state()

counter = 0
while state_result < DONE:
    rospy.loginfo("Doing some stuff while action is running")
    counter += 1

    """
    Doing some stuff here
    """
    rate.sleep()

    state_result = client.get_state()
    rospy.loginfo("state_result %d"%state_result)

    if counter == 3:
        rospy.logwarn("Cancelling Goal")
        client.cancel_goal()
        rospy.logwarn("Goal Cancelled")
        rospy.loginfo("Update state Result after cancel: %d Counter %d" % (client.get_state(), counter))


rospy.loginfo("[Result] State: %d"%client.get_state())

if state_result == WARN:
    rospy.logwarn("There was a warning while executing the action")
elif state_result == ERROR:
    rospy.logerr("There was an error while executing the actions")
