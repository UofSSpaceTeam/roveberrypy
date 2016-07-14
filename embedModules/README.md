Post URC 2016
=============
Some notes on some of the modules:

Arm
---
Communications is buggy. I2C packets seem to be recieved from the rover properly,
but the values aren't translated to motor movement.
Directly controlling the arm with the serial command prompt works fine.
There is likely something wrong with the `parseCommand` function,
so one may try directly changing `g_duty_cycle` in the `recieveCommand` function.
I'm not sure this will help however, as during debugging,
the duty cycle manager was setting the motors correctly, but the arm didn't move.
There may be a flag somewhere that was not set/reset properly or something.

Drill, StorageBin, ExampleCAN and others using Teensy CAN bus
-----
This is for a Teensy 3.1/3.2 using a Microchip CAN transceiver as well as the FlexCAN library (https://github.com/teachop/FlexCAN_Library). They simply are notified of all messages and send messages at the beginning and end of the main loop.

These were working in the lab, but failed at competition. Likely a fried Teensy. :frowning:
The rover network archetecture was not well suited to the high speeds required by the motors. Improvements are needed there.

Science sensors
---------------
We never had time to really make these work. Potential benchtop code is here in the sensors folder.
