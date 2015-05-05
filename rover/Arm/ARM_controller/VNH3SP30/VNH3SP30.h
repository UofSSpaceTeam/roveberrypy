

#ifndef VNH3SP30_h
#define VNH3SP30_h

#include "Arduino.h"

class VNH3SP30 {
	private:

		// arduino connections
		int inA; // motor output control 1 pin
		int inB; // motor output control 2 pin
		int pmw_pin;

		// state of thh motor (enable/disabled)
		int pos;

	
	public:		

		// Constructor
		// Motor( <inA> , <inB> , <enable_pin>, <pmw_pin> )
		VNH3SP30(int, int, int);

		// setDutyCycle( <valid PWM value>)
		// set duty cycle, [-255,255]
		void setDutyCycle(int);
		
		// check if the motor is enabled
		bool checkState();

		void updatePosition(int);
		int getPosition();
		
		// De-constructor, does nothing
		~VNH3SP30();
};

#endif

//eof