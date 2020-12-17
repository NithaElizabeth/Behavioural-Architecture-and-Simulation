#!/usr/bin/env python
"""This is the state machine that switches between the three states

This node is a satate machine that is implemented in position of command
manager in the whole architecture.This state machine is implemented in 
smach.It switches between three nodes sleep, normal and play.

"""

import roslib
import rospy
import smach
import smach_ros
import time
import random

import actionlib
import cv2
import imutils
import math
import numpy as np

from scipy.ndimage import filters
from actionlib_msgs.msg import GoalStatus
from geometry_msgs.msg import Pose,PoseStamped, Twist
from std_msgs.msg import String, Float64
from sensor_msgs.msg import CompressedImage
from geometry_msgs.msg import Point
from std_msgs.msg import String

import exp_assignment2.msg


VERBOSE = False

"""The parameters x_lim and y_lim  corresponds to the boundary limit of the descrete 2D envirionment of the robot."""
#x_lim = rospy.get_param('x_limit')
#y_lim = rospy.get_param('y_limit')
x_lim = 7
y_lim = 7



"""The parameters home_position_x and home_position_y extracts the location of the home as described in the launch file"""
#home_position_x = rospy.get_param('home_x')
#home_position_y= rospy.get_param('home_y')
#home_position_x = 4 
#Shome_position_y= 4


"""Initialisation of global variables used in this node"""
client_action = None
pos = Pose()
is_ball_found = False
camera_sub = None
counter_time = 0
robotStopped = False
velPub =None
headJointPub = None

def move_robot(location): 
	
    global client_action 

    """Assigning the goal """
    goal = exp_assignment2.msg.PlanningGoal()
    goal.target_pose= location

    """The goal position is sent to the action server """
    client_action.send_goal(goal) 
 
    client_action.wait_for_result() 




def search_ball(self, ros_data):
    global is_ball_found
    if VERBOSE:
            print ('received image of type: "%s"' % ros_data.format)

    np_arr = np.frombuffer(ros_data.data, np.uint8)
    image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    greenLower = (50, 50, 20)
    greenUpper = (70, 255, 255)

    blurred = cv2.GaussianBlur(image_np, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    if len(cnts) > 0:
        # The robot has seen the ball
        is_ball_found = True 


def follow_ball(ros_data):
    global is_ball_found
    global robotStopped
    global velPub

    if robotStopped == True:
        return
    
    np_arr = np.frombuffer(ros_data.data, np.uint8)
    image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    greenLower = (50, 50, 20)
    greenUpper = (70, 255, 255)

    blurred = cv2.GaussianBlur(image_np, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    if len(cnts) > 0:
        # The robot has seen the ball
        is_ball_found = True

        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        if radius > 10:
			#cv2.circle(image_np, (int(x), int(y)), int(radius),(0, 255, 255), 2)
			#cv2.circle(image_np, center, 5, (0, 0, 255), -1)
            vel = Twist()
            vel.angular.z = 0.002*(center[0]-400)
            vel.linear.x = -0.01*(radius-100)
            
            
            if (abs(vel.linear.x) <= 0.1) and (abs(vel.angular.z) <= 0.1):
                """The robot has a negligible speed """
                vel.angular.z = 0
                vel.linear.x = 0
                robotStopped = True
                return
            velPub.publish(vel)

    else:
        # The robot doesn't see the ball
        is_ball_found = False
    cv2.imshow('window', image_np)
	cv2.waitKey(2)
    


def user_action():
    """This function choses randomly a state from the 3 states:"sleep","normal","play" """
    return random.choice(['sleep','normal', 'play'])

# define state Sleep
class Sleep(smach.State):
    """This class defines the state Sleep
	
    This is the state in which robots return to home position and does 
    not indulge in any activities.
    
    Methods
    ----------
    _init_(self)
		This methods initialises all the attributes of the class
    execute(self,userdata)
		This methods executes the sleep state
    Sleep_callback(self,arg)
		This method is the subscriber callback function for the topic 'position'.
		The loaction of the home is assigned to the topic /position
	
    """
    def __init__(self):
		smach.State.__init__(self, outcomes=['goto_NORMAL_state'])
		#rospy.Subscriber('position',Point,self.Sleep_callback)
		#self.home_position = Point()
	
    #def Sleep_callback(self,arg):
		#rospy.set_param('position_x',home_position_x)
		#rospy.set_param('position_y',home_position_y)
                             
        
    def execute(self, userdata):
        	#rospy.set_param('current','sleep')
        	rospy.loginfo('_______________________Executing state SLEEP ________________________')
        	
        	#Sets the home position"""
        	#self.home_position.x=4
        	#self.home_position.y=4
        	global pos
        	global client_action
        	pos.pose.position.x = 4
        	pos.pose.position.y = 4
        	move_robot(pos)
        	print('SLEEP state: The robot has arrived home.\n')
        	
        	rospy.loginfo('Robot reached HOME position')
        	time.sleep(10)
        	sleepCounter = 0
        	return 'goto_NORMAL_state'
		

    

class Normal(smach.State):
    """This class defines the state Normal
    
    This is the state in which robots moves randomly and is willing to 
    listen to its operators commands.
    	
    Methods
    ----------
    _init_(self)
	This methods initialises all the attributes of the class
    execute(self,userdata)
	This methods executes the normal state
    Normal_callback(self,arg)
	Thsi is the callback function for the subscribed topic 
	position.
    Normal_callback1(self,arg)
	Thsi is the callback function for the subscribed topic 
	voice_command.
    Normal_callback2(self,arg)
	Thsi is the callback function for the subscribed topic 
	voice_commands_sleep.	
    """	
    def __init__(self):
		smach.State.__init__(self,outcomes=['goto_SLEEP_state','goto_PLAY_state'])
        self.sleepThreshold = 5		
        
    def execute(self, userdata):
		rospy.loginfo('______________________Executing state NORMAL _______________________')
		global is_ball_found
		global client_action
		global camera_sub
		global counter_time
		#while (rospy.get_param('current')=='normal' and not rospy.is_shutdown()): 
		camera_sub = rospy.Subscriber("camera1/image_raw/compressed",CompressedImage, search_ball,  queue_size=1)
		#while (not rospy.is_shutdown()): 
		while counter_time < self.sleepThreshold:
			
			pos.pose.position.x = random.randrange(1,x_lim,1)
			pos.pose.position.y = random.randrange(1,y_lim,1)
			move_robot(pos)
			#Create the goal
			#goal = exp_assignment2.msg.PlanningGoal(target_pose=pos)
			print("The robot randomly moves to a location [%d, %d].\n" %(pos.pose.position.x, pos.pose.position.y))
			# Send the goal
			#client_action.send_goal(goal)
			#while True
			if is_ball_found == True :
					is_ball_found = False
					client_action.cancel_goal()
					# Unsubscribe to the image topic
					camera_sub.unregister()
					# Go into the PLAY state
					print('The Robot is switching its state to PLAY from NORMAL.\n')
					return 'goto_PLAY_state'
			else :
					move_robot(pos)
			
			counter_time +=  1
		camera_sub.unregister()
        time.sleep(30)
		#state= user_action()
		#if(state == 'sleep'):
		return 'goto_SLEEP_state'


class Play(smach.State):
    """This class defines the state Play
    
    This is the state in which robots moves according to the operators 
    will. When in this state , it first moves to the location of the operator 
    and then moves to the position to which the operator points.
    
    Methods
    ----------
    _init_(self)
	This methods initialises all the attributes of the class
    execute(self,userdata)
	This methods executes the normal state
    Play_callback_gesture(self,arg)
	Thsi is the callback function for the subscribed topic 
    	pointed_position.
    
    """	
    def __init__(self):
		smach.State.__init__(self, outcomes=['goto_NORMAL_state'])



    def execute(self, userdata):
		#rospy.set_param('current','play')
		#pub = rospy.Publisher("robot_control",Point,queue_size=1)
		rospy.loginfo('______________________Executing state PLAY _______________________')
		global counter_time
		global client_action
		global is_ball_found
		global robotStopped
		global camera_sub
		global headJointPub
		global velPub
		#while (not rospy.is_shutdown()):  
		camera_sub = rospy.Subscriber("robot/camera1/image_raw/compressed", CompressedImage, follow_ball)
		while True:
			if robotStopped == True:
				vel = Twist()
                vel.angular.z = 0
                vel.linear.x = 0
                velPub.publish(vel)
             
                angle = Float64()
                angle.data = 0.0

                print("Camera rotated to left.\n")

                """To Move the head to the left as ball was not detected """
                while angle.data < (math.pi/4):
                    angle.data = angle.data + 0.2
                    headJointPub.publish(angle)
                    time.sleep(2)
                time.sleep(2)
                while angle.data != 0:
                    angle.data = angle.data - 0.2
                    headJointPub.publish(angle)
                    time.sleep(2)
                time.sleep(2)
				
                print("Camera rotated to right.\n")

                """To move the head to the right as ball was not detected"""
                while angle.data > -(math.pi/4):
                    angle.data = angle.data - 0.2
                    headJointPub.publish(angle)
                    time.sleep(2)
                time.sleep(2)
                while angle.data != 0:
                    angle.data = angle.data +0.2
                    headJointPub.publish(angle)
                    time.sleep(2)
                time.sleep(2)

                robotStopped = False
                sleepCounter += 1
                # imageSub = rospy.Subscriber("robot/camera1/image_raw/compressed", CompressedImage, trackBall)

		time.sleep(1)

			

        
def main():
    """This class is the main class
	
    This class defines the relation of each state parameters to corresponding 
    states.From the sleep state , the robot moves to Normal state.From the 
    normal state the robot can move to either Sleep state or PLay state.And 
    from the Play state the robot moves back to normal state.
		
    """	

    rospy.init_node('state_machine')
    global client_action
    global headJointPub
    global velPub
    
    # Create the action client and wait for the server 
    
    client_action = actionlib.SimpleActionClient("robot/reaching_goal", exp_assignment2.msg.PlanningAction)
    client_action.wait_for_server()

    # Initialize the two publishers
    headJointPub = rospy.Publisher("robot/joint1_position_controller/command", Float64, queue_size=1)
    velPub = rospy.Publisher("robot/cmd_vel", Twist, queue_size=1)

    # Create a SMACH state machine
    sm = smach.StateMachine(outcomes=[])
    #sm.userdata.sm_counter = 0

    # Open the container
    with sm:
        # Add states to the container
        smach.StateMachine.add('SLEEP', Sleep(), 
                               transitions={'goto_NORMAL_state':'NORMAL'})
        smach.StateMachine.add('NORMAL', Normal(), 
                               transitions={'goto_SLEEP_state':'SLEEP', 
                                            'goto_PLAY_state':'PLAY'})
        smach.StateMachine.add('PLAY', Play(), 
                               transitions={'goto_NORMAL_state':'NORMAL'})


    # Create and start the introspection server for visualization
    sis = smach_ros.IntrospectionServer('server_name', sm, '/SM_ROOT')
    sis.start()

    # Execute the state machine
    outcome = sm.execute()

    # Wait for ctrl-c to stop the application
    rospy.spin()
    sis.stop()


if __name__ == '__main__':
    main()
