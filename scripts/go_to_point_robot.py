#! /usr/bin/env python

## @package go_to_point_robot
# Implements an action server that moves the robot.

# Import ros stuff
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist, Point, Pose
from nav_msgs.msg import Odometry
from tf import transformations
import math
import actionlib
import actionlib.msg
import exp_assignment2.msg 

# Robot state variables
position_ = Point()
pose_ = Pose()
yaw_ = 0

# Machine state
state_ = 0

# Goal
desired_position_ = Point()
desired_position_.z = 0

# Parameters
yaw_precision_ = math.pi / 9 # +/- 20 degree allowed
yaw_precision_2_ = math.pi / 90 # +/- 2 degree allowed
dist_precision_ = 0.1
kp_a = 3.0
kp_d = 0.5
ub_a = 0.6
lb_a = -0.5
ub_d = 0.6

# Publisher
pub = None

# Action_server
act_s = None

# Callbacks
def clbk_odom(msg):
    global position_
    global pose_
    global yaw_
    
    # Position
    position_ = msg.pose.pose.position
    pose_ = msg.pose.pose
    
    # Yaw
    quaternion = (
        msg.pose.pose.orientation.x,
        msg.pose.pose.orientation.y,
        msg.pose.pose.orientation.z,
        msg.pose.pose.orientation.w)
    euler = transformations.euler_from_quaternion(quaternion)
    yaw_ = euler[2]

def change_state(state):
    global state_
    state_ = state
    print('Robot: state changed to [%s]' %state_)

def normalize_angle(angle):
    if(math.fabs(angle) > math.pi):
        angle = angle - (2 * math.pi * angle) / (math.fabs(angle))
    return angle

def fix_yaw(des_pos):
    global yaw_, pub, yaw_precision_2_, state_
    desired_yaw = math.atan2(des_pos.y - position_.y, des_pos.x - position_.x)
    err_yaw = normalize_angle(desired_yaw - yaw_)
    # rospy.loginfo(err_yaw)
    
    twist_msg = Twist()
    if math.fabs(err_yaw) > yaw_precision_2_:
        twist_msg.angular.z = kp_a * err_yaw 
        if twist_msg.angular.z > ub_a:
            twist_msg.angular.z = ub_a
        elif twist_msg.angular.z < lb_a:
            twist_msg.angular.z = lb_a
    
    pub.publish(twist_msg)
    
    # State change conditions
    if math.fabs(err_yaw) <= yaw_precision_2_:
        print('Robot: yaw error [%s]' %err_yaw)
        change_state(1)

def go_straight_ahead(des_pos):
    global yaw_, pub, yaw_precision_, state_
    desired_yaw = math.atan2(des_pos.y - position_.y, des_pos.x - position_.x)
    err_yaw = desired_yaw - yaw_
    err_pos = math.sqrt(pow(des_pos.y - position_.y, 2) + pow(des_pos.x - position_.x, 2))
    err_yaw = normalize_angle(desired_yaw - yaw_)
    # rospy.loginfo(err_yaw)
	
    if err_pos > dist_precision_:
        twist_msg = Twist()
        twist_msg.linear.x = 0.6
        # twist_msg.linear.x = kp_d * (des_pos.x-position_.x)
        if twist_msg.linear.x > ub_d:
            twist_msg.linear.x = ub_d
        
        twist_msg.angular.z = kp_a*err_yaw
        pub.publish(twist_msg)
    else:
        print('Robot: position error [%s]' %err_pos)
        change_state(2)
    
    # state change conditions
    if math.fabs(err_yaw) > yaw_precision_:
        print('Robot: yaw error [%s]' %err_yaw)
        change_state(0)

def done():
    twist_msg = Twist()
    twist_msg.linear.x = 0
    twist_msg.angular.z = 0
    pub.publish(twist_msg)
    
def planning(goal):
	
	global state_,desired_position_
	global act_s
	
	desired_position_.x = goal.target_pose.pose.position.x
	desired_position_.y = goal.target_pose.pose.position.y
	
	state_ = 0
	rate = rospy.Rate(20)
	success = True
	
	feedback = exp_assignment2.msg.PlanningFeedback()
	result = exp_assignment2.msg.PlanningResult()
	
	while not rospy.is_shutdown():
		if act_s.is_preempt_requested():
			print('Robot: goal was preempted')
			act_s.set_preempted()
			success = False
			break
		elif state_ == 0:
			feedback.stat = "Fixing the yaw"
			feedback.position = pose_
			act_s.publish_feedback(feedback)
			fix_yaw(desired_position_)
		elif state_ == 1:
			feedback.stat = "Angle aligned"
			feedback.position = pose_
			act_s.publish_feedback(feedback)
			go_straight_ahead(desired_position_)
		elif state_ == 2:
			feedback.stat = "Target reached!"
			feedback.position = pose_
			act_s.publish_feedback(feedback)
			done()
			break
		else:
		    rospy.logerr('Unknown state!')
		
		rate.sleep()
	if success:
		print('Robot: goal succeeded!')
		act_s.set_succeeded(result)

def main():
    global pub, act_s
    rospy.init_node('go_to_point_robot')
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    sub_odom = rospy.Subscriber('odom', Odometry, clbk_odom)
    act_s = actionlib.SimpleActionServer('reaching_goal', exp_assignment2.msg.PlanningAction, planning, auto_start = False)
    act_s.start()
    
    rate = rospy.Rate(20)
    
    while not rospy.is_shutdown():
        rate.sleep()

if __name__ == '__main__':
    main()
