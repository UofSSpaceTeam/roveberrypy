Tutorial
========
**IN PROGRESS**

This page will describe how the rover system works and how to get going with creating a new RoverProcess.

A RoverProcess is essentially a program that is in charge of one
component of the rover's behaviour, and/or hardware.
We designed the RoverProcesses to have a similar structure as an
Arduino sketch, so all your initialization goes in a "setup" function,
and anything you want to run continually in a "loop" function.
There is also an interprocess communication (IPC) system that
allows RoverProcesses to communicate with each other, and leads
to more advanced event driven programming.
All RoverProcess are stored in the folder "roverprocess",
which is also a python package.

Adding a new RoverProcess
-------------------------

To add a new RoverProcess, start by copying the ExampleProcess.py
and call it whatever you want your process to be named.
So if your process name is TestProcess, call the file TestProcess.py.
The ExampleProcess is written as an attempt to show off the features
of the rover software, and not everything is required for your process to run.
The absolute minimal RoverProcess is as follows::

    from .RoverProcess import RoverProcess

    class MinimalProcess(RoverProcess):
        pass

That's it! The RoverProces super/parent class has default definitions
for all its methods, so anything you don't need you can leave out.
To enable the process, open up ``main.py`` and find the line in the
``main`` function where the ``init_modulesList`` is called.
The parameters should be names of RoverProcesses you want enabed.
Change the line to be::
    
    modulesList = init_modulesList("MinimalProcess")

Now run the main script as `described in its documentation`__.
It should look something like this::

    root                : INFO     Enabled modules:
    root                : INFO     ('MinimalProcess',)
    root                : INFO     Registering process subscribers...
    root                : INFO     STARTING: ['MinimalProcess']

To stop the rover software, press Ctrl-c. You should get this::

    ^Croot                : INFO     STOP: ['MinimalProcess']
    StateManager        : INFO     StateManager shutting down
    root                : INFO     MinimalProcess shutting down
    StateManager        : INFO     StateManager shutting down
    StateManager        : INFO     StateManager shut down success!

You can see how the main script started up your MinimalProcess,
but when it stops, there is also a StateManager that stops as well.
The StateManager is another RoverProcess that manages the IPC mechanism.
You can ignore it for the most part, unless you plan on adding features
to the whole rover process system its self.

At this point, if you don't know Python, you should probably learn it ;).
There are plenty of tutorials on the internet and Youtube, though the
official Python documentation has a decent tutorial as well.
Don't worry about becoming fluent, just learn up to and including
classes and inheritance and how modules work, and you should be fine.
The rest is best learned through experience and practice.

Obviously, this MinimalProcess is pretty boring, so lets make our process actually do something.
At the top, import the ``time`` module. In your MinimalProcess,
add a method called ``loop`` that takes no parameters other than ``self``.
The ``loop`` method is run continually until you press Ctrl-c to stop the system.
Let's create a simple hello world printer::

    def loop(self):
        print("Hello World!")
        time.sleep(1)

This should print "Hello World!" to the screen every second.

Sometimes you need to do stuff once right when the system starts up
such as initializing variables. This can be done by adding a ``setup``
method to the process::

    def setup(self, args):
        self.var = 42
        print("In setup()")

This will declare a new member called var and assign it a value of 42.
It can be accessed later in the main loop or in message handler functions.
The parameter ``args`` is just the arguments passed into the ``__init__``
method (the constructor). There used to be uses for it, but you
probably won't need to use it anymore.
If you run the rover software now, you should get::

    root                : INFO     Enabled modules:
    root                : INFO     ('MinimalProcess',)
    root                : INFO     Registering process subscribers...
    root                : INFO     STARTING: ['MinimalProcess']
    In setup()
    Hello World
    Hello World
    Hello World
    Hello World
    ^Croot                : INFO     MinimalProcess shutting down
    root                : INFO     STOP: ['MinimalProcess']
    StateManager        : INFO     StateManager shutting down
    StateManager        : INFO     StateManager shutting down
    StateManager        : INFO     StateManager shut down success!


That's the basics of adding a minimal process, the next section will talk about
the IPC system. Before you move on however, there is one last thing to cover
regarding printing to the console.
While there is nothing technically wrong with using the ``print()`` function,
the RoverProcess system provides a more useful way to print messages to
the user/developer. This is the logging module.
The method ``self.log()`` is a wrapper for Python's built in logging module.
It allows us to print more detailed information about which process is
printing messages to the console and when, and it provides logging "levels"
which allows us to classify some statements as debug messages, others as
warnings or errors, and we can easily change how verbose the rover software
is by changing a line in the main script.
Check out the `Python Logging`_ documentation for more information.
While you can import the logging module and make calls to it directly,
``self.log()`` provided by the RoverProcess should be fine for most uses.

Try changing the print statement in ``setup`` from ``print("In setup()")`` to::

    self.log("In setup()", "DEBUG")

In the ``loop`` method, change ``print("Hello World!")`` to::

    self.log("Hello World!")

Now, running the software should give you this::

    root                : INFO     Enabled modules:
    root                : INFO     ('MinimalProcess',)
    root                : INFO     Registering process subscribers...
    root                : INFO     STARTING: ['MinimalProcess']
    MinimalProcess      : DEBUG    In setup()
    MinimalProcess      : INFO     Hello World
    MinimalProcess      : INFO     Hello World
    MinimalProcess      : INFO     Hello World
    MinimalProcess      : INFO     Hello World
    ^Croot                : INFO     MinimalProcess shutting down
    root                : INFO     STOP: ['MinimalProcess']
    StateManager        : INFO     StateManager shutting down
    StateManager        : INFO     StateManager shutting down
    StateManager        : INFO     StateManager shut down success!

Notice the format of the output. When many processes are spamming stuff
to the console, this is *very* handy to tell which process is doing what.

You will also have noticed that the second column displays the logging level.
The ``self.log`` method optionally takes a logging level as we did in our setup
method. It defaults to ``INFO`` if not given.

Now in the main script find the line in the ``init_logging`` function that
calls the ``logging.basicConfig`` function. Change the level from ``DEBUG``
to ``INFO`` and run the software again.
The debug log in the setup method was not printed.
Always be selective about what level you give statements.
Generally, anything that gets printed every 100 milliseconds should be ``DEBUG``.

One last thing about logging: everything is also written to a file called log.log.
This may be useful if the rover crashes or something. Hopefully in the future
we can have different log levels for the file and the console.


__ main.html

.. _Python Logging: https://docs.python.org/3.5/library/logging.html
