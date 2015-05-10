

#include "Arduino.h"
#include "MC33926.h"

MC33926::MC33926(int m_in1, int m_in2 ){
	
	// define arduino connections
	in1 = m_in1; // in1 pin
	in2 = m_in2; // in2 pin
	
	// set inital state of the H bridge
	analogWrite(in1,0);
	analogWrite(in2,0);
  position = 0;
}

void MC33926::setDutyCycle(int val){
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


void MC33926::updatePosition(int pos){
  position += pos;
}

int MC33926::getPosition(){
  return position;
}


MC33926::~MC33926(){
  //do nothing
}



//eof