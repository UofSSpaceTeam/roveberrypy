
#ifndef MC33926_h
#define MC33926_h

#include "Arduino.h"

class MC33926 {
	private:

		// arduino connections
		int in1; // motor output control 1 pin
		int in2; // motor output control 2 pin

		// state of thh motor (enable/disabled)
		int position;

	
	public:		

		// Constructor
		// Motor( <control_pin1> , <control_pin2> )
		MC33926(int, int);

		// setDutyCycle( <valid PWM value>)
		// set H bridge duty cycle, [-255,255]
		// control 1 set + for positive values
		void setDutyCycle(int);

		//convinient place to store position count
		void updatePosition(int);

		// get position count
		int getPosition();
		
		// De-constructor, does nothing
		~MC33926();
};

#endif

//eof