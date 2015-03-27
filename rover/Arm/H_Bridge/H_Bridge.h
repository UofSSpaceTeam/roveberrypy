/*
 _______________________________________________________________________________________
|																						|
|	Library for H-bridge 														        |
|	Written by Liam Bindle															    |
|   March 27, 2015																	    |
|	USST, 2015																			|
|_______________________________________________________________________________________|

*/
#ifndef H_Bridge_h
#define H_Bridge_h

#include "Arduino.h"

class H_Bridge {
	private:

		// arduino connections
		int in1; // motor output control 1 pin
		int in2; // motor output control 2 pin
		int enable_pin; // enable pin

		// state of thh motor (enable/disabled)
		bool state;
		int position;

	
	public:		

		// Constructor
		// Motor( <control_pin1> , <control_pin2> , <enable_pin> )
		H_Bridge(int, int, int);

		// setDutyCycle( <valid PWM value>)
		// set H bridge duty cycle, [-255,255]
		// control 1 set + for positive values
		void setDutyCycle(int);
		
		// check if the motor is enabled
		bool checkState();

		//convinient place to store position count
		void updatePosition(int);

		// get position count
		int getPosition();
		
		// enable or disable the motor
		void enable();
		void disable();
		
		// De-constructor, does nothing
		~H_Bridge();
};

#endif

//eof