#!/usr/bin/env python
"""This is implemented to move the ball using commands. 

The ball disapears when the user command becomes DISAPPEAR and the ball 
moves to some random position when the user command becomes MOVE. 
""" 


"""Imports the neccessary libraries and headers"""
import rospy
import time
import random
import actionlib
from geometry_msgs.msg import PoseStamped
import exp_assignment2.msg

"""This is a variable used to describe the action client """
client_action = None

"""The desired position is fed to this variable """
pos = PoseStamped()


def user_command():
    """The funcction is used to randomly select the user command from  the choices MOVE and DISAPPEAR """
    ## random choice between search for the ball or go to sleep 
    return random.choice(['move','disappear'])

# Randomly perfoms one of the two available commands.
def change_ball_position():
    """This function is used to change the ball's position from its current location based on the user commads received from user_command()"""
	
    
    while not rospy.is_shutdown():

        """To call the function for receiving the commands """
        command= user_command()

        if command=='move':
            
            print("\nCommand given for the ball : MOVE ")
            x = random.randint(-7, 0)
            y = random.randint(0,7)
            pos.pose.position.x = x
            pos.pose.position.y = y
            pos.pose.position.z = 0.20
            """ Create the goal position"""
            goal = exp_assignment2.msg.PlanningGoal()
            goal.target_pose= pos
            print("\nThe ball is now at position [%d, %d].\n" %(x, y))
            """ Send the goal """
            client_action.send_goal(goal)
            # Wait until the ball has reached the destination
            client_action.wait_for_result()
            time.sleep(20)
        elif command=='disappear':
			print( "\nCommand given for the ball : DISAPPEAR ")
			#disappearBall()
			pos.pose.position.x = 0
			pos.pose.position.y = 0
			pos.pose.position.z = -1
			""" Create the goal position"""
			goal = exp_assignment2.msg.PlanningGoal()
			goal.target_pose= pos
			print("\nThe ball has now disappeared.\n")
	
			""" Send the goal """
			client_action.send_goal(goal)

			"""It waits for the robot to reach goal"""
			client_action.wait_for_result()

			time.sleep(18)
			
		


if __name__ == "__main__":
    try:
        """To initialise this node"""
        rospy.init_node('move_ball')

        """Describing the sction client """
        client_action = actionlib.SimpleActionClient("ball/reaching_goal", exp_assignment2.msg.PlanningAction)
        client_action.wait_for_server()
        """Calls the function to move the ball according to the command """
        change_ball_position()

        
    except rospy.ROSInterruptException:
        pass
