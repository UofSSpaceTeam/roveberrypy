main script
===========
The main.py script bootstraps the rover system, automatically importing
and instantiating the enabled classes. After starting all the RoverProcesses,
the main script just sleeps in a loop until a keyboard interupt is generated.

To run from the command line, enter::

    python3 main.py

Depending on your operating system, python 3 may be the default version of python,
so you could get away with::

    python main.py

To stop the rover software, press Ctrl-c.

-------------------------------------------

.. automodule:: main
    :members:

