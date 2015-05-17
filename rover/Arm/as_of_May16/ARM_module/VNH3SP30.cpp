

#include "Arduino.h"
#include "VNH3SP30.h"

VNH3SP30::VNH3SP30(int inA_pin, int inB_pin, int pmw){
	
	// define arduino connections
	inA = inA_pin; // in1 pin
	inB = inB_pin; // in2 pin
  pmw_pin = pmw;
	
	// set inital state of the H bridge
	pinMode(inA, OUTPUT);
  pinMode(inB,OUTPUT);
  pos = 0;
}

void VNH3SP30::setDutyCycle(int val){
  // if value is positive
  if( val == 0){// set = 0
    digitalWrite(inA, LOW);
    digitalWrite(inB, LOW);
    analogWrite(pmw_pin,0);
    return;
  }
   else if(val>0){
    //go forwards
    digitalWrite(inA, HIGH);
    digitalWrite(inB, LOW);
    if(val<256){
      analogWrite(pmw_pin, val);
	  return;
    }
    else{ //if val > 255
      analogWrite(pmw_pin,255);
	  return;
    }
  }
  else if(val<0){
	 val = abs(val);
     //go backwards
    digitalWrite(inA, LOW);
    digitalWrite(inB, HIGH);
    if(val > 256){
      analogWrite(pmw_pin,val);
      return;
    }
    else{ //if val < 255
      analogWrite(pmw_pin,255);
      return;      
    }
  }
  else{ // catch anything weird
    digitalWrite(inA, LOW);
    digitalWrite(inB, LOW);
    analogWrite(pmw_pin,0);
    return;
  }
  return;
} 


void VNH3SP30::updatePosition(int update){
  pos += update;
}

int VNH3SP30::getPosition(){
  return pos;
}

VNH3SP30::~VNH3SP30(){
  //do nothing
}



//eof