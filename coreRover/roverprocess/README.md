Post URC 2016
=============
Some notes on the state of the rover modules:


ArmProcess
----------
The controls were threwn together the hour before the competition,
and while joystick input from the game pad seems to work, the buttons do not.
I2C packets seem to send properly and are recieved by the Arduino on the other end.
The arduino code for comunications is also buggy; see /embedModules/README.md for details.

Camera, Drill, StorageBin Process
---------------------------------
All of these work the same way: Messages defined in CanServer define translation from the state dictonary to CAN packets. Communication is one-way and message names are really flexible. To see how these messagse are used, see the Teensy code in the embedded modules directories.

The camera process is not implemented, but the commented code defines how the gimbals should be controlled. See the DriveProcess for information on how to handle data coming from the WebServer.
None of these modules were tested in the field. Drill seemed to work fine in the lab before we left for Utah.
The Teensy on the drill may be fried.

DriveProcess
------------
Some tweaks were made before the compute module board got swapped out, but the current code works well enough to drive. Simply translates gamepad messages to RPM messages, but some (now unused) features for telemetry and Torque/Current and Duty Cycle control are partly implemented. These interface with the VESC https://github.com/vedderb/bldc with a few modifications to the types of telemetry data sent. The modifications were not significant and much more detialed custom firmware is planned for 2017.

NavProcess
----------
Interfaces with a Piksi RTK device using a UART and the piksi library. A good example on how to interface custom libraries with the rover system. Also contains a simulator for testing, but nothing formal.

Example Processes
-----------------
These conain the bare minimum code to create a regular process, as well as ones that are able to communicate directly with rover hardware using a semaphore (I2C) as well as through a custom server adapter (CAN/SocketCAN).

CanServer, WebServer and JsonServer
-----------------------------------
These act as adapters between the internal state dictionary and the outside world.
* JsonServer translates dictonaries to JSON strings and sends them to a client over a socket
* CanServer translates dictionary keys to priorities (user-defined) and puts them on the CAN bus
* WebServer manages a Bottle-0.13 WSGI server. See Routes.py in the gui-software repository for information on how POST commands are turned into dictionary key:value pairs

All of the Servers are set up by main.py whch manages which processes' messages are diverted to which server.  All external data coming into the server is automatically placed or upated in the global state dictionary.
