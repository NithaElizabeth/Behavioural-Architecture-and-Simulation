#!/usr/bin/env python

## @package person
# Mimics the behaviour of a person controlling the robot.
# The person can move the ball to a certain goal position or can make 
# it disappear.

import rospy
import time
import random
import actionlib
from geometry_msgs.msg import PoseStamped
import exp_assignment2.msg

# Action client
client_action = None

# Goal pose
new_pos = Pose()

##
# Sends a goal to the ball's action server to move it to a random 
# position. After the ball has reached the destination the person
# wait some time before issuing another command.
def move_ball_position():

	global client_action
    x = random.randint(-7, 0)
    y = random.randint(0, 7)
	condition = random.randint(-1, 1)
	if condition > 0 :
		new_pos.pose.position.x = x
		new_pos.pose.position.y = y
		new_pos.pose.position.z = 0.01
	else :
		new_pos.pose.position.x = x
		new_pos.pose.position.y = y
		new_pos.pose.position.z = -1

    # Create the goal
    goal = exp_assignment2.msg.PlanningGoal()
    goal.target_pose = new_pos

    # Print a feedback message
    print("\n The ball moves to the new location :  [%d, %d].\n" %(x, y))

    # Send the goal
    client_action.send_goal(goal)

    # Wait until the ball has reached the destination
    client_action.wait_for_result()

    time.sleep(10)



if __name__ == "__main__":
    try:
        # Initialize the node
        rospy.init_node('move_ball')

        # Create the action client and wait for the server
        client_action = actionlib.SimpleActionClient("ball/reaching_goal", exp_assignment2.msg.PlanningAction)
        client_action.wait_for_server()

        move_ball_position()
        
    except rospy.ROSInterruptException:
        pass
