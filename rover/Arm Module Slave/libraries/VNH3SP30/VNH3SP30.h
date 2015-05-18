#ifndef VNH3SP30_h
#define VNH3SP30_h

#include "Arduino.h"

class VNH3SP30
{
	private:
		int motorA;
		int motorB;
		int motorPWM;
		volatile int count;
		char direction; // -1, 0, or 1
	
	public:		
		VNH3SP30(int A, int B, int PWM);

		// valid speed values: -255 to 255
		void set(int val);

		void addToCount(int num);
		
		int getCount();
		
		char getDirection();
};

#endif

