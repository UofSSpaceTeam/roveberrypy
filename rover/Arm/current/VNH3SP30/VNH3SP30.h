/*
 _______________________________________________________________________________________
|																						|
|	Library for VNH3SP30 motor controller										        |
|	Written by Liam Bindle															    |
|   April 1, 2015																	    |
|	USST, 2015																			|
|_______________________________________________________________________________________|

*/

#ifndef VNH3SP30_h
#define VNH3SP30_h

#include "Arduino.h"

class VNH3SP30 {
	private:

		// arduino connections
		int inA; // motor output control 1 pin
		int inB; // motor output control 2 pin
		int enable_pin; // enable pin
		int pmw_pin;

		// state of thh motor (enable/disabled)
		bool state;
		int pos;

	
	public:		

		// Constructor
		// Motor( <inA> , <inB> , <enable_pin>, <pmw_pin> )
		VNH3SP30(int, int, int, int);

		// setDutyCycle( <valid PWM value>)
		// set duty cycle, [-255,255]
		void setDutyCycle(int);
		
		// check if the motor is enabled
		bool checkState();
		
		// enable or disable the motor
		void enable();
		void disable();

		void updatePosition(int);
		int getPosition();
		
		// De-constructor, does nothing
		~VNH3SP30();
};

#endif

//eof