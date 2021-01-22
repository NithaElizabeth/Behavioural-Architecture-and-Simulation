# Experimental Robotics Laboratory - Assignment 2
#### Behavioural Architecture and its Simulations
## Intoduction
This repository contains the Assignment 2 of Experimental Robotics Lab.The aim of this assignment is to implement a model based simulation for the behavioural architecure's state machine that was completed as assignment 1, for a pet (dog-like) robot that moves in a discrete 2D envirionment.The architecture involves nodes for changing the location of the ball, a finite state machine as the command manager and components for changing the position of the Robot and Ball to the desired goal locations.\
The project was developed on ROS-kinetic and Python and state machine is implemented on Smach. 
## Software Architecture
![env](https://user-images.githubusercontent.com/47361086/102724337-de304d80-4334-11eb-80b7-3033d7e5e08a.PNG) \
The picture above is the simulated envirionment of the implemented system along with the modelled robot.
![robot](https://user-images.githubusercontent.com/47361086/102724371-22bbe900-4335-11eb-93fb-55086402a386.PNG) \
The pet robot has a head of type sphere attached to a cylindrical neck.The head-neck setup is attached to the wheeled robot provided. \
The major components of the system are :
* State Machine
* Move_Ball
* Go to point -Robot
* Go to point -Ball
#### State Machine
This acts as the command manager.It switches between three states i.e. "sleep", "normal", "play". "Sleep" being the initial state, the robot rest in its home location. At "normal" state, the robot wanders randomly throughout the envirionment until it sees a green ball. On detecting the green ball, the robot changes its state to "play". In the "play" state , the robot moves to the location of the ball and then follows the green ball until stops.
#### The Move Ball Component
This component is responsible for giving pos for moving and changing the position and mode of the Green ball used in this simulation.This node assumes that the operators(user operating this robot) gives one out of two commands : MOVE , DISAPPEAR at a time. Hence it randomly chooses either MOVE or Disappear as user command. Based on this user command the ball navigates and changes its position. If the user command is MOVE, the ball moves to some random position and if the user command DISAPPEAR , the ball will no longer be seen on the 2D world. In this node, the action client uses the ball/reaching_goal topic to move the ball.
#### Go to point -Robot
This component is responsible for making the pet robot navigate in the modelled world based on the pos(target position) it receives.
#### Go to point -Ball
This component is responsible for making the green ball navigate in the modelled world based on the pos(target position) it receives.

## State Diagram
This section explains how the states are decided. As illustrated in the state diagram below, there are three states : "sleep", "normal", "play".
![Untitled Document (1)](https://user-images.githubusercontent.com/47361086/98930126-a0e6cd80-24f5-11eb-8624-acb703c2cd10.png)

The state "sleep" is the initial state. In the "sleep" , the robot returns to its home position and rests.From the "sleep" state the robot switches to the "normal" behaviour after some time.In the "normal" behaviour the robot moves randomly at location within its constrainted envirionment. In the "normal" behaviour, the robot will be checking for the presence of a Green ball.The robot contains in movement in the world to some random positions until it detects a green ball in front of it. If the robot detects a green ball while being in the "normal" state, it switches its state to the next state, which is "play". The detections are done with the help of a camera unit mounted on top of its head. From the state "normal", it can switch to either "sleep" or "play".In the "play", the robot initially moves to position where the ball is and continue to track the movement of the ball until the ball is not visible again.If the movement of the ball is stopped, then the robot will shake its head by moving the head to right and left in 45 degrees and returning back to the center position. The robot will switch back to the "normal" state if it does not see the green ball for some time.
## Package and File List
The file tree shows the various packages in this project.

![download](https://user-images.githubusercontent.com/47361086/102724044-990b1c00-4332-11eb-87cb-15f261c86792.png)

The **docs** folder contains the documentations obtained from doxgen.The **index.html** contains the html documentation of all the scripts used in this project.The **launch folder** has the **launch fil**e to run the project. The scripts are all contained inside the **src folder**.
## Installation and Running Procedure
Clone this github repository into the ROS workspace src folder
```
git clone https://github.com/NithaElizabeth/Behavioural-Architecture-and-Simulation-of-Robot-EXPRO2
```
Next the scripts had to made executable.For that navigate to the src folder of this repositiory.
```
cd Behavioural-Architecture-and-Simulation-of-Robot-EXPRO2--master/src
```
```
chmod +x state_machine.py
```
```
chmod +x move_ball.py
```
```
chmod +x go_to_point_robot.py
```
```
chmod +x go_to_point_ball.py
```
After this navigate to the launch directory from clonned folder
```
cd launch
```
```
roslaunch gazebo_world.launch
```
## Working Hypothesis 
Throughout this project, it was assumed that the robot moves in discrete 2D envirionment.It implies that the position of robot at any instant will be a point with x and y coordinates only. The finite state machine was built under the hypothesis that the transition between the state will be strictly like that shown in the state diagram figure given above. It was also assumed that the robot will not move over or through the ball. The move_ball node assumes that the operator commands will be of type string and will only say "DISAPPEAR" or "MOVE" to the ball. It is also assumed that throughout the program that the robot will process only one operation at a time and all other operation that that point will be queued and only processed after the execution of the current task (if still in the same behaviour).
## Systems Features
The system provides a well implemented behavioural architecture. This system is capable of transiting from one state to the other. When in "normal" state , the robot can move through random positions.The ball is capable of identifiying the voice commands and moving to prescribed locations or state. The system checks whether the location ordered by the operator is within the bound of the envirionment that was predecided. 
## Systems Limitation
The system was not realised in practical scenerio, hence most of the operations are randomised and assumed inclding the time to wait. The system is only capable of processing the voice command "DISAPPEAR" and "MOVE".The ball at times collide with the Human model, this happens as no obstacle avoidance is incorporated with the program. Most of the time, by the time Robot process the detection of the ball in front of it , the ball might have already disappeared from the scene. Hence the "play" state is rarely active.The robot continous in its random motion for most of the time. The system adheres to the predefined working scenerios and hypothesis but it has flaws and would not be fully functional in real scenerio with lot of uncertainities.
## Possible Improvements
The system could be more rondomised so as to work in the worldly scenerio with ot of ambiguities.Rather than fixing the operator's position, it can be made random.Similarly the the envirionment can me remodelled.  Also it could be reprogrammed in such a way that the verbal move_ball node can possibly processes several voice commands rather than the one mentioned alone.Finally, the obstacle avoidance could also be implemented in the system so that the robot never passes through the ball or collide with the human dummy.
## Author
The system was developed by Nitha Elizabeth John under the guidance of Prof.Luca Buoncompagni and Prof.Carmine Recchiuto\
Author  : Nitha Elizabeth John\
Contact : nithaelizabethjohn@gmail.com
