 _______________________________________________________________________________________
|																						|
|	Library for MC33926 motor controller										        |
|	Written by Liam Bindle															    |
|   March 20, 2015																		|
|	University of Saskatchewan 														    |
| 	The following code is currently untested but compiles: March 20, 2015				|
|	USST, 2015																			|
|_______________________________________________________________________________________|


_________________________________________________________________________________________
Motor( <Pin mX_in1> , <Pin mX_in2> , <Pin en> , <Pin fb> , <Pin sf> )
Create motor object

PRE: PINS :: integer, correct pin numbers
_________________________________________________________________________________________

setMotorSpeed( < speed > , <accelerating factor> )
Kind of a useless method but allows you to set the speed of the motor. Provides const acc.

PRE: speed :: integer, [-100, 100]
	 accelerating factor :: integer, acelerating coeff.
RETURN: true if successful
_________________________________________________________________________________________

setDutyCycle( < value > )
Set the duty cycle to the motor

PRE: value :: integer, [-255,255]
	      negative for cw rotation
RETURN: true if successful
_________________________________________________________________________________________

enableMotor( < t / f > )
... self explanatory

PRE: bool is passed
RETURN: true is successful
_________________________________________________________________________________________

readCurrent()
Get the current that the motor is using. Currently set for MC33926

RETURN: current, [A]
_________________________________________________________________________________________

checkFlag();
Check that all is working okay.

POST: if there is an error the motor is disabled 
RETURN: enabled state of the motor
_________________________________________________________________________________________

getPosition();
Get the position of the motor.  ** currently not implemented

RETURN: Position of the motor in rad.
_________________________________________________________________________________________

setPosition( < position >)
Give the motor a position to rotate to.

PRE: position :: float, valid angle. 0 is straight ahead
POST: motor has moved to this position
RETURN: true if successful
_______________________________________________________________________________________










