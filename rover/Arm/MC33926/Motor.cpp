/*
 _______________________________________________________________________________________
|																						|
|	Library for MC33926 motor controller										        |
|	Written by Liam Bindle															    |
|   March 20, 2015																		|
|	University of Saskatchewan 														    |
| 	The following code is currently untested but compiles: March 20, 2015				|
|	USST, 2015																			|
|_______________________________________________________________________________________|

*/

#include "Arduino.h"
#include "Motor.h"

Motor::Motor(int m_in1, int m_in2, int m_enable, int motor_fb, int m_sf){
	in1 = m_in1;
	in2 = m_in2;
	enable = m_enable;
	m_fb = motor_fb;
	sf = m_sf;
	
	pinMode(in1,OUTPUT);
	pinMode(in2,OUTPUT);
	pinMode(enable,OUTPUT);
	enabled = true;
	pinMode(sf,INPUT);
	
	analogWrite(in1,0);
	analogWrite(in2,0);
	motorSpeed = 0;
	digitalWrite(enable,HIGH);
}

bool Motor::setDutyCycle(int val){
  if(val>0){
    //go forwards
    if(val<256){
      analogWrite(in1,val);
      analogWrite(in2,0);
	  return true;
    }
    else{ //if val > 255
      analogWrite(in1,255);
      analogWrite(in2,0);
	  return true;
    }
  }
  else if(val<0){
     //go backwards
    if(val > -256){
      analogWrite(in1,0);
      analogWrite(in2,val); 
      return true;
    }
    else{ //if val < -255
      analogWrite(in1,0);
      analogWrite(in2,255);
      return true;      
    }
  }
  else{ // set = 0
     analogWrite(in1,0);
	 analogWrite(in2,0);
     return true;
  }
  return false;
} 

bool Motor::setMotorSpeed(int val, int coeff){
  //coeff is to set the rate at which it accelerates 
  
  int absVal = val;
  if(val<0){ 
    absVal = -1*val;
  }
  int upperBound = map(absVal, 0,100,0,256);
  
   for(int t = 0; t*t/coeff <= upperBound ; t ++){
       setDutyCycle(t*t/coeff); 
   }
   motorSpeed =  map(absVal, 0,100,0,256);
} 

bool Motor::enableMotor(bool set){
	digitalWrite(enable,set);
	enabled = set;
}

float Motor::readCurrent(){
	float feedback = analogRead(m_fb);
	
	if(motorSpeed>=0){
		return feedback*0.0093006; // feeback is 525 mV/A
	}
	else{
		return -feedback*0.0093006;
	}
}

Motor::~Motor(){
	//do nothing
}

void Motor::checkFlag(){
	bool state = digitalRead(sf);
	if(!state){
		digitalWrite(enable, LOW);
		enabled = false;
		setDutyCycle(0);
	}
}

float Motor::getPosition(){
	// do something to get position
	// [code here]
	return 123;
}

bool Motor::setPosition(float position){
	
	float tolerance = 0.05; // ~ 3 deg 
	int minSpeed = 50; //min speed
	
	while( abs(position - getPosition())> tolerance){ // while we are not at the desired position
		
		// possibly add line to check for flag
		// checkFlag();
		
		
		float currentPosition = getPosition();
		int direction; // direction to rotate, 1 = ccw, -1 = cw
		
		// determine direction to rotate 
		if (position > currentPosition){ // rotate ccw
			direction = 1;
		}
		else{ // rotate cw
			direction = -1;
		}
		
		
		float distance = abs(position - currentPosition); // distance in rad to rotate
		
		if(distance < 0.2 ){ //if less than ~ 11.5 deg away
			motorSpeed = minSpeed*direction;
			setDutyCycle(motorSpeed);				
		}
		else if( distance < 1){ // if we are less than ~ 60 deg away begin decelerating proportional to distance
			motorSpeed = (minSpeed + 15*(distance*10-2))*direction; // formula so max speed is 170 but at 0.2 rad we are going minSpeed
				setDutyCycle( motorSpeed );
		}
		else{
			if(abs(motorSpeed) < 67){ // if the motor is at less than 66%, as of right now this value is arbitrary, make sure to change it and decelerating formula
				motorSpeed = motorSpeed*1.05; // this accelerating constant is arbitrary
				setDutyCycle(motorSpeed);
			}
			
		}
		
		
		
	}
	
	// once we are at the right position set the speed to zero
	setDutyCycle(0);
	motorSpeed = 0;
	return true; // return that it was successful
	
}


//eof