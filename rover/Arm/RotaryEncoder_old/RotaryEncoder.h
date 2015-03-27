/*
 _______________________________________________________________________________________
|																						|
|	Library for rotary encoder													        |
|   March 24, 2015																		|
|	University of Saskatchewan 														    |
|	USST, 2015																			|
|_______________________________________________________________________________________|

IMPORTANT NOTES: 
- a function to handle interrupts must be included in the .ino file
this should look like:

- the outputs from the encoders should all be connected through an OR gate to the Arduino's 
interrupt pin 


THE FOLLOWING MUST BE INCLUDED IN THE .ino FILE
________________________________________________________________________________________

// update the positions of the motors when there has been a state change
void stateChange(){
   <RotaryEncoder_Object1>.updatePosition();  //update the positions
   <RotaryEncoder_Object2>.updatePosition(); 
   
}

void setup() {
  attachInterrupt(0,stateChange,CHANGE);
  ...
  [continue program]
________________________________________________________________________________________
 
 
For the Arduino Uno:
If the output of the OR gate is connected to pin 2 then attachInterrupt(0,...
If the output of the OR gate is connected to pin 3 then attachInterrupt(1,...
*/

#ifndef RotaryEncoder_h
#define RotaryEncoder_h

#include "Arduino.h"

class RotaryEncoder {
	private:
		int pinA; // pin A
		int pinB; // pin B
		
		int cA; // current value of pin A
		int cB; // current value of pin B
		int pA; // previous value of pin A
		int pB; // previous value of pin B
		int posCnt; // count
		
		int pointsPerRotation; // number of points in a rotation [hard coded in constructor]
		
	public:
		//RotaryEncoder(int <pinA>, int <pinB>)
		// create an encoder object
		// VERY IMPORTANT:  make sure all encoder outputs are connected via and OR gate to
		// interrupt pin. Also dont forget the interupt function that calls updatePosition!
		RotaryEncoder(int , int ); 
		
		//update the position
		// must be called upon every interupt
		void updatePosition();
		
		//get the position of the motor
		// scaling factor is hard coded
		float getPosition();
};

#endif

//eof