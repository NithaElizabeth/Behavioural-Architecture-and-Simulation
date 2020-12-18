# Experimental Robotics Laboratory - Assignment 2
#### Behavioural Architecture and its Simulations
## Intoduction
This repository contains the Assignment 2 of Experimental Robotics Lab.The aim of this assignment is to implement a behavioural architecure for a robot that moves in a discrete 2D envirionment.The architecture involves nodes for changing the location of the ball, a finite state machine as the command manager and components for changing the position of the Robot and Ball to the desired goal locations.\
The project was developed on ROS-kinetic and Python and state machine is implemented on Smach. 
## Software Architecture
![expro_arch2](https://user-images.githubusercontent.com/47361086/98937966-9ed63c00-2500-11eb-920e-5707efc8079d.PNG)
The picture above is the component diagram of the implemented system.The major components of the system are :
* Verbal Interaction
* Gesture Interaction
* State Machine
* Control
#### Verbal Interaction Component
This component is responsible for obtaining the verbal orders from the operator(person).This is used to receive the voice commands of the person and then to process it . Once processed, it will be passed on to the state machine to initiate the corresponding behavior. In this project, it is assumed that the operator says a command of type string (eg. "play" ) and it is processed and send to to the state machine.
#### Gesture Interaction
This component is responsible for obtaining the gestures from the operator(person). This components will recieve the cordinates of the location pointed by the operator and it is published to the state machine so that if the robot is in state "play" it should move the location pointed by the operator.
#### State Machine
This acts as the command manager.It switches between three states i.e. "sleep", "normal", "play". "Sleep" being the initial state, the robot rest in its home location. At "normal" state, the robot wanders randomly throughout the envirionment. In the "play" state , the robot moves to the location of the operator and then follows the operators gestures and move toward the position pointed by the operator.
#### Control
This component is responsible for the robot motion and control. After obtaining the location or commands from the previous components, the robot moves to that position respectively.This component also publishes its current location via topic /position.
## State Diagram
This section explains how the states are decided. As illustrated in the state diagram below, there are three states : "sleep", "normal", "play".
![Untitled Document (1)](https://user-images.githubusercontent.com/47361086/98930126-a0e6cd80-24f5-11eb-8624-acb703c2cd10.png)

The state "sleep" is the initial state. In the "sleep" , the robot returns to its home position and rests.From the "sleep" state the robot switches to the "normal" behaviour.In the "normal" behaviour the robot moves randomly at location within its constrainted envirionment. In the "normal" behaviour, the robot will be willing to listen to the verbal commands and all the verbal commands will be registered. From the state "normal", it can switch to either "sleep" or "play".In the "play", the robot initially moves to position where the operator (person) is and then follows the operators instruction and moves to the location pointed by the operator.
## Package and File List
The file tree shows the various packages in this project.

![tree1](https://user-images.githubusercontent.com/47361086/98941699-60438000-2506-11eb-945e-3f5ad7b48c23.PNG)

The **docs** folder contains the documentations obtained from doxgen.The **index.html** contains the html documentation of all the scripts used in this project.The **launch folder** has the **launch fil**e to run the project. The scripts are all contained inside the **src folder**.
## Installation and Running Procedure
Clone this github repository into the ROS workspace
```
git clone https://github.com/NithaElizabeth/Behavioural-Architecture_-EXPRO-1-
```
Next the scripts had to made executable.For that navigate to the src folder of this repositiory.
```
cd Behavioural-Architecture_-EXPRO-1--master/src
```
```
chmod +x state_machine.py
```
```
chmod +x verbal_interaction.py
```
```
chmod +x gesture_interaction.py
```
```
chmod +x control.py
```
After this. in another terminal run the roscore.
```
roscore
```
Once the roscore is run,then the launch file must be run.
```
cd ..
roslaunch assignment1 assignment1.launch
```
## Working Hypothesis 
Throughout this project, it was assumed that the robot moves in discrete 2D envirionment.It implies that the position of robot at any instant will be a point with x and y coordinates only. The finite state machine was built under the hypothesis that the transition between the state will be strictly like that shown in the state diagram figure given above. It was also assumed that the position of the person will be constant for an iteration of the program. The verbal interaction node assumes that the operator commands will be of type string and will only say "play". It is also assumed that throughout the program that the robot will process only one operation at a time and all other operation that that point will be queued and only processed after the execution of the current task (if still in the same behaviour).
## Systems Features
The system provides a well implemented behavioural architecture. This system is capable of transiting from one state to the other. When in "normal" state , the robot can move through random positions.The robot is capable of identifiying the voice commands and moving to prescribed locations. The system checks whether the location ordered by the operator is within the bound of the envirionment that was predecided. 
## Systems Limitation
The system was not realised in practical scenerio, hence most of the operations are randomised and assumed inclding the time to wait. The system is only capable of processing the voice command "play". From "play" the robot automaticaly switches to "normal" state even without being invoked which may not be ideal in real scenerio.The robot movement was not simulated as this project concentrates mostly on the higher level, i.e finite state machine. The system adheres to the predefined working scenerios and hypothesis but it has flaws and would not be fully functional in real scenerio with lot of uncertainities.
## Possible Improvements
The system could be more rondomised so as to work in the worldly scenerio with ot of ambiguities.Rather than fixing the operator's position, it can be made random.Similarly the the envirionment can me remodelled.  Also it could be reprogrammed in such a way that the verbal interaction node can possibly processes several voice commands rather than "play" alone.Finally, The simulation could be visualised in a simulator.
## Author
The system was developed by Nitha Elizabeth John under the guidance of Prof.Luca Buoncompagni and Prof.Carmine Recchiuto\
Author  : Nitha Elizabeth John\
Contact : nithaelizabethjohn@gmail.com
