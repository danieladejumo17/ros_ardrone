#! /usr/bin/env python

import rospy
import time
import actionlib
from ardrone_as.msg import ArdroneAction, ArdroneGoal, ArdroneFeedback, ArdroneResult

nImage = 1

def feedback(feedback):
    global nImage
    print("[Feedback] Image n.%d received"%nImage)
    nImage += 1

rospy.init_node("drone_action_client")

client = actionlib.SimpleActionClient("ardrone_action_server", ArdroneAction)

client.wait_for_server()

goal = ArdroneGoal()
goal.nseconds = 10

client.send_goal(goal, feedback_cb=feedback)

client.wait_for_result()

print("[Result] State: %d"%client.get_state())
