/*

Pin Configuration for MC33926:

M2D1   GND
M2D2   VDD
M2IN1  11   <- Arduino connection 
M2IN2  10   <- Arduino connection 
INV    GND
SLEW   GND
EN     12   <- Arduino connection 

*/

#include <H_Bridge.h>
#include <SoftwareSerial.h>

//define pin connections
#define in1 11
#define in2 10
#define m1in1 6
#define m1in2 5
#define en 12

// create motor object
H_Bridge m1 (in1,in2,en);

// interrupt counter
int temp_tick_cnt;

//define constants to be used
const int ppr = 90;
const int maxSpeed = 200;
const int minSpeed = 40;

//function headers
int getSerial();
void positionChange();
void setPosition(int, H_Bridge &);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.println("H_Bridge test!");
  attachInterrupt(0,positionChange,CHANGE);
  attachInterrupt(1,positionChange,CHANGE);
}

void loop() {

  Serial.print("The current position of the motor is: ");
  Serial.println(m1.getPosition()*360/ppr);
  int pos = Serial.parseInt();
  if(pos != 0){
    setPosition(pos*ppr/360, m1);
  }

}

//-------------------------------------------------------------------------

int getSerial() {
  int inbyte, serialdata;
  serialdata = 0;
   do {
    inbyte = Serial.read();  
    if (inbyte > 0 && inbyte != '\n') { 
      serialdata = serialdata * 10 + inbyte - '0';
    }
  } while (inbyte != '\n');
  return serialdata;
}

void positionChange(){ temp_tick_cnt ++; }

void setPosition(int pos, H_Bridge& motor){
  
  //set up
  temp_tick_cnt = 0;
  int ticks = pos - motor.getPosition();
  int sign = ticks/abs(ticks);
  ticks = abs(ticks);

  //wait till we get to the position
  while(temp_tick_cnt < ticks){
    if(temp_tick_cnt > ticks / 2){
      motor.setDutyCycle((((maxSpeed-minSpeed)/ppr)*2*(ticks - temp_tick_cnt)+minSpeed)*sign);
    }
    else{
      motor.setDutyCycle(((2*(maxSpeed-minSpeed)/ppr)*(temp_tick_cnt)+minSpeed)*sign);
    }
  }

  // stop motor and update position
  motor.setDutyCycle(0);
  motor.updatePosition(temp_tick_cnt*sign);

}