Roveberrypy 
===========
[![Documentation Status](https://readthedocs.org/projects/roveberrypy/badge/?version=latest)](http://roveberrypy.readthedocs.io/en/latest/?badge=latest)

About
-----
The USST Rover project has developed a multi-threaded Python 3 application designed to manage a system of interconnected embedded modules over a variety of networks.

Using the Python language and focusing on support from standard libraries, high-level abstraction of hardware interfaces and devices can be prototyped, tested and deployed in embedded environments and on the user's PC. The software supports defined configurations based on detected hardware, and multithreading allows for standalone modules to be easily swapped out.

Features
--------
* Synchronizes state between an arbitrary number of independent Python processes using the multiprocessing library and a very simple global state dictionary
  * Write any Python code, threads, classes or libraries with no restrictions
  * Easy to use publish/subscribe based inter-process communication.
* Extends the global state on a numbner of network interfaces:
  * Serial over USB with pyserial.
  * Lightweight BottlePy WSGI web server (see [rover-gui](https://github.com/UofSSpaceTeam/rover-webui/tree/d7e1a6e840f479ed2c5b5d0c0a93fe3b54bead02) for the user interface software)
  * Integration with [VESC motor controllers](http://vedder.se/2015/01/vesc-open-source-esc/) with [PyVESC](https://github.com/LiamBindle/PyVESC)

Documentation
-------------
*Documentation for Roveberrypy can be found at [Read the Docs](http://roveberrypy.readthedocs.io/en/latest/).*
If you are a member of the USST and are a member of our Github organization, you _should_ have access
to [usstdocs.herokuapp.com](usstdocs.herokuapp.com). This site has various other tutorials and links to documentation
for our projects, some aspects of which we prefer to keep secret due to the nature of the competitions we
take part in. Unfortunately the authentication script can be a bit flakey and can block you out the first time you go there.
Keep refreshing the page, try again in an hour or two, and contact Carl if issues persist.

Future
------
* Implement a lightweight standardized serialization protocol for communication with embedded peripherals
* Add database features
* Automated unit testing
* Rewrite the CAN server using python sockets
* Add a I2C server

How To Contribute
-----------------
We have a [wiki page](https://github.com/UofSSpaceTeam/usst-docs/wiki/USST-git-work-flow) outlining our workflow.

1. Pick an issue on the issue tracker or create an issue and have it assigned to a milestone
2. Check out or create a feature branch.
2. Code!
3. Make a pull request to the dev branch.
4. Stable code will be merged into master eventually.

For general information on how to contribue to USST projects please see the [Wiki in the usst-docs repository](https://github.com/UofSSpaceTeam/usst-docs/wiki).
To get in touch with the team, visit www.usst.ca.
