#rover-software

About
-----
The USST Rover project has developed a multi-threaded python application designed to manage a system of interconnected embedded modules over a variety of networks.

Using the python language and focusing on support from standard libraries, high-level abstraction of hardware interfaces and devices can be prototyped, tested and deployed in embedded environments and on the user's PC. The software supports defined configurations based on detected hardware, and multithreading allows for standalone modules to be easily swapped out.

Features
-------
* Synchronizes state between an arbitrary number of independent python processes using the multiprocessing library and a very simple global state dictionary
  * Write any python code, threads, classes or libraries with no restrictions
  * Trigger event-driven actions based on watched changes in the global state
* Extends the global state on a numbner of network interfaces:
  * CAN through SocketCAN
  * JSON Raw Sockets with the native Python Socket module
  * Lightweight BottlePy WSGI web server (see rover-gui for the user interface software)

Future
------
* ~~Update from Python 2.7 to 3.5~~ In progress. Haven't tested the servers yet.
* Implement a lightweight standardized serialization protocol for communication with embedded peripherals
* Add logging and database features
* Automated unit testing
* Rewrite the CAN server using python sockets
* Add a UART and I2C server

How To Contribute
-----------------
1. Pick an issue on the issue tracker or create an issue and have it assigned to a milestone
2. Check out or create a milestone branch
2. Code!
3. Make a pull request to the dev branch
4. Stable code will be automatically pushed to master

For general information on how to contribue to USST projects please see the Wiki in the usst-docs repository.
To get in touch with the team, visit www.usst.ca.
