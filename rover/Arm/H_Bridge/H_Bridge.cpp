/*
 _______________________________________________________________________________________
|                                                                                       |
| Library for H-bridge                                                                  |
| Written by Liam Bindle                                                                |
|   March 27, 2015                                                                      |
| USST, 2015                                                                            |
|_______________________________________________________________________________________|

*/

#include "Arduino.h"
#include "H_Bridge.h"

H_Bridge::H_Bridge(int m_in1, int m_in2, int m_enable){
	
	// define arduino connections
	in1 = m_in1; // in1 pin
	in2 = m_in2; // in2 pin
	enable_pin = m_enable; // enable pin
	
	// set inital state of the H bridge
	pinMode(enable_pin,OUTPUT);
	analogWrite(in1,0);
	analogWrite(in2,0);
	digitalWrite(enable_pin,HIGH);
	state = true;
  position = 0;
}

void H_Bridge::setDutyCycle(int val){
  // if value is positive
  if(val>0){
    //go forwards
    if(val<256){
      analogWrite(in1,val);
      analogWrite(in2,0);
	  return;
    }
    else{ //if val > 255
      analogWrite(in1,255);
      analogWrite(in2,0);
	  return;
    }
  }
  else if(val<0){
	val = abs(val);
     //go backwards
    if(val > -256){
      analogWrite(in1,0);
      analogWrite(in2,val);
      return;
    }
    else{ //if val < -255
      analogWrite(in1,0);
      analogWrite(in2,255);
      return;      
    }
  }
  else{ // set = 0
     analogWrite(in1,0);
	 analogWrite(in2,0);
     return;
  }
  return;
} 

bool H_Bridge::checkState(){
  return state;
}

void H_Bridge::updatePosition(int pos){
  position += pos;
}

int H_Bridge::getPosition(){
  return position;
}

void H_Bridge::enable(){
	state = true;
	digitalWrite(enable_pin,HIGH);
}

void H_Bridge::disable(){
	state = false;
	digitalWrite(enable_pin,LOW);
}

H_Bridge::~H_Bridge(){
  //do nothing
}



//eof