/*
 _______________________________________________________________________________________
|																						|
|	Library for MC33926 motor controller										        |
|	Written by Liam Bindle															    |
|   March 20, 2015																		|
|	University of Saskatchewan 														    |
|	USST, 2015																			|
|_______________________________________________________________________________________|

*/
#ifndef Motor_h
#define Motor_h

#include "Arduino.h"

class Motor {
	private:
		int in1; // mX_in1 pin
		int in2; // mX_in2 pin
		int enable; // mX_en pin 
		int m_fb; // mX_fb pin
		int sf; // mX_sf pin
		
		bool enabled; // enabled state 
		float motorSpeed; // current motor speed
	
	public:
		// Constructor
		// Motor( <Pin mX_in1> , <Pin mX_in2> , <Pin en> , <Pin fb> , <Pin sf> )
		Motor(int, int, int, int, int);
		
		// set the duty cycle to M1O1/M1O2
		// setDutyCycle( <valid PWM value>)
		bool setDutyCycle(int);
		
		// set the motor speed to a value(speed between -100 and 100) with constant acc
		// setMotorSpeed( <speed> , <accelerating constant> )
		bool setMotorSpeed(int,int);
		
		//set enabled the motor
		// enableMotor( <true/false>)
		bool enableMotor(bool);
		
		// read current used by the motor, calibrated for MC33926
		// readCurrent()
		float readCurrent();
		
		// check that everything is working properly
		//checkFlag()
		void checkFlag();
		
		// get the position the motor is currently at
		// returns radians
		float getPosition();
		
		
		// set the position of the motor
		// setPosition( < [rad] > )
		bool setPosition(float);
		
		// De-constructor
		~Motor();
};

#endif

//eof