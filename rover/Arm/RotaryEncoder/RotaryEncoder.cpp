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



sorry for crappy commenting. Any question contact me: liam.bindle@usask.ca


*/

#include "Arduino.h"
#include "RotaryEncoder.h"

RotaryEncoder::RotaryEncoder(int A, int B){
	pinA = A;
	pinB = B;
	
	pinMode(pinA, INPUT);
	pinMode(pinB, INPUT);
	cA = digitalRead(pinA);
	pA = cA;
	cB = digitalRead(pinB);
	pB = cB;
	
	posCnt = 0;
	pointsPerRotation = 12;
}

void RotaryEncoder::updatePosition(){
	//read A and B
  cA = digitalRead(pinA);
  cB = digitalRead(pinB);
  
  //ugly nested ifs to handle state change
  //if a value has changed since the last loop
  if ((cA != pA) || (cB != pB)) {

    //if B changed ...need to add something to this if
    if (cB != pB) {
      //if A is currently LOW
      if (!cA) {
        switch (cB) {
          case 0:
            posCnt ++;
            break;
          case 1:
            posCnt--;
            break;
        }
      }
      //otherwise A is HIGH
      else {
        switch (cB) {
          case 0:
            posCnt --;
            break;
          case 1:
            posCnt++;
            break;
        }
      }
    }
    else {
      if (!cB) {
        switch (cA) {
          case 0:
            posCnt--;
            break;
          case 1:
            posCnt++;
        }
      }
      else {
        switch (cA) {
          case 0:
            posCnt++;
            break;
          case 1:
            posCnt--;
        }
      }
    }
  }
  
  //update previous values to current values
  pA = cA;
  pB = cB;
  
  
  
  
  // carry over the position in the case it goes more/less than 180 deg
  if(posCnt > pointsPerRotation/2){
	posCnt = -pointsPerRotation/2;
	posCnt ++;
  }
  else if( posCnt <= -pointsPerRotation/2){
	posCnt = pointsPerRotation/2;
  }
  
}

float RotaryEncoder::getPosition(){
	return 180*posCnt/(pointsPerRotation/2);
}



//eof