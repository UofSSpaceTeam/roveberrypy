#ifndef MC33926_h
#define MC33926_h

#include "Arduino.h"

class MC33926
{
	private:
		int motorA;
		int motorB;
		volatile int count;
		char direction; // -1, 0, or 1
	
	public:		
		MC33926(int in1, int in2);

		// valid speed values: -255 to 255
		void set(int val);

		void addToCount(int num);

		int getCount();
		
		char getDirection();
};

#endif

