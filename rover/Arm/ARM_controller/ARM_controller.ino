
/*



*/
#include <Wire.h>
#include "VNH3SP30.h"

// number of linear actuator being used
int numLinac  = 2;  // all arrays must be of length numLinac. However dir must be length numLinac + 1

#define TIMEOUT 750

// pin connections
#define L1inA 13
#define L1inB 12
#define L1pwm 10
#define L2inA 4
#define L2inB 5 
#define L2pwm 6
// #define L3inA
// #define L3inB
// #define L3pwm
#define BASEinA 7
#define BASEinB 8
#define BASEpwm 9

int wiper[2];       
int minimum[2];
int maximum[2];
enum command_type // instructions from the Pi
{
	STOP, // stop all motors
	SET_POS, // set desired speed for left / right sides
        NUDGE
};

typedef struct
{
	byte header;
	byte type; // actually used as enum command_type, that's ok
	short d1; // Base rotation
	short d2; // LinAc. 1
	short d3; // LinAc. 2
        //short d4; // LinAc. 3
	byte csum; // sum of cmd_type, d1, d2, d3, d4
	byte trailer;
} command;

enum motor_state // describes possible states of motors
{
	OK,
	STALL
};

// arduino address on bus
const byte i2c_address = 0x08;

// traction control data
motor_state m_state[] = {OK, OK, OK, OK}; // current state
float position[] = {0, 0, 0, 0}; // commanded speed commanded

// state information
const byte CMD_HEADER = 0xF7;
const byte CMD_TRAILER = 0xF8;
unsigned long timeout;
volatile command cmd;
byte* cmd_ptr = (byte*)(&cmd);
volatile byte cmd_count = 0;
volatile bool new_cmd = false;

// create objects
VNH3SP30 linac[2] = { VNH3SP30(L1inA, L1inB, L1pwm) ,
                      VNH3SP30(L2inA, L2inB, L2pwm) };
                //    VNH3SP30(L3inA, L3inB, L3pwm) };
VNH3SP30 base (BASEinA, BASEinB, BASEpwm);


// global variables
int newPosition[2];    // analogReadValue which the linac is being set to
int initialPosition[2];      // intial position of the linac
bool inMotion[2];   // bool :: whether or not the linac's position is being set 
int dir[3];         // direction the linac needs to go
float scalingCoeff[2];  // scaling coefficient to convert analogReadValue to mm

// base variables
int interrupt_counter;
int newPositionCount;
const int pphr = 20088;  // points per half rotation of base
const int base_speed = 200;  // duty cycle of base
bool rotationInProgress = false;

//function headers
void setPosition (float[]);
void checkLinacPosition();
void checkBasePosition();
void positionChange();
// int* inverseKinecmatics(float*);
// Interrupt handler for receiving a byte via I2C
void receiveEvent(int count);

// function to actually process command
void processCommand();


void setup() {
  // setup serial
  Serial.begin(9600);
  delay(1000);
  Serial.println("ARM_controller test!");

  //initalize interrupts
//  attachInterrupt(0,positionChange,CHANGE);
//  attachInterrupt(1,positionChange,CHANGE);


  //initalize pins and linear actuator constants
  wiper[0] = A1;
  minimum[0] = 392;
  maximum[0] = 583;
  scalingCoeff[0] = 0.615;

  wiper[1] = A0;
  minimum[1] = 410;
  maximum[1] = 583;
  scalingCoeff[1] = 0.615;

  // wiper[2] = A2;
  // minimum[2] = ;
  // maximum[2] = ;

  // make sure the linac are in brake position
  for(int i = 0; i < numLinac ; i++){
    inMotion[i] = false;
    linac[i].setDutyCycle(0);
  }
  
  // set position
  float positionArr[2];
  
  positionArr[0] = 50;
  positionArr[1] = 50;
  positionArr[2] = 0;
  
  
  Serial.println("Setting positions: ");
  Serial.print("L1: ");
  Serial.println(minimum[0] + 2 + positionArr[0]/scalingCoeff[0]);
  Serial.print("L1 is currently at: ");
  Serial.println(analogRead(A1));
  Serial.print("L2: ");
  Serial.println(minimum[1] + 2 + positionArr[1]/scalingCoeff[1]);
  Serial.print("L2 is currently at: ");
  Serial.println(analogRead(A0));
  Serial.print("BASE: ");
  Serial.println(positionArr[2]);
  Serial.print("BASE is currently at: ");
  Serial.println("not connected");
  
  setPosition(positionArr); 
  
  //Wire.begin(i2c_address);
  //Wire.onReceive(receiveEvent);

  // initialize outputs (done by the H_Bridge class)

  // clear cmd struct
  //for(unsigned int i = 0; i < sizeof(command); i++)
	//cmd_ptr[i] = 0x00;

  // arm timeout
  timeout = millis();
  

}




void loop() {
  /*if(new_cmd) {
	processCommand();
	new_cmd = false;
  }*/

  checkLinacPosition();
  checkBasePosition();
  /*Serial.print(position[0]);
  Serial.print(',');
  Serial.print(position[1]);
  Serial.print(',');
  Serial.print(position[2]);
  Serial.print(',');
  Serial.println();
  setPosition(position); */
  
  /*if(millis() - timeout > TIMEOUT) {
	Serial.println("TO");
	timeout = millis();
  }*/

  
  // if(Serial.available() && !inMotion[0] && !inMotion[1] && !rotationInProgress){
  //   Serial.println("Set position of the arm.")
  //   Serial.println("Enter L1 length [ 0 mm , 109 mm]")
  //   float input[numLinac] = { 0 , 0 , 0 };

  //   Serial.print("The current position is: ");
  //   Serial.println(analogRead(A1));
  //   float pos[1] ={ Serial.parseFloat()};
  //   if(pos[0] != 0){
  //     setPosition(pos);
  //   }
  // }
}

//-------------------------------------------------------------------------

void checkBasePosition(){
  if(rotationInProgress){
    if(interrupt_counter < newPositionCount){
      base.setDutyCycle(base_speed*dir[numLinac]);
    }
    else{
      rotationInProgress = false;
      // stop base and update position
      base.setDutyCycle(0);
      base.updatePosition(interrupt_counter*dir[numLinac]);
      interrupt_counter =0;
      newPositionCount = 0;
    }
  }
}

void positionChange(){ interrupt_counter ++; }

void checkLinacPosition(){
  // loop to set position of all the linacs
  for(int i = 0; i < numLinac ; i++){
    if(inMotion[i]){ // if the position of lineac[i] is currently being set
      float currentPosition = analogRead(wiper[i]); // read the current position (0 to 1023)
      Serial.println((newPosition[i] - currentPosition));
      if((dir[i]*(newPosition[i] - currentPosition) < 0) || (currentPosition < minimum[i]) || (currentPosition > maximum[i]) ){ // check if linac is at proper pos
          inMotion[i] = false;
          linac[i].setDutyCycle(0);
      }
      else{
        linac[i].setDutyCycle(255*dir[i]); // if we arent at the proper position then set the speed 
        // [enter set speed algo. here]
      }
    }
  }
}


void setPosition(float* pos){

  float* lengths = inverseKinematics(pos);
  // set up setPosition for each linac
  for(int i = 0; i < numLinac ; i++){
    newPosition[i] = minimum[i] + 2 + lengths[i]/scalingCoeff[i]; // analog read value corresponding to <pos> mm.
    initialPosition[i] = (analogRead(wiper[i]));      // inital position...currently not used but here for set speed algo
    
    if(initialPosition[i] != pos[i]){              // check that we are not already at the proper position
      inMotion[i] = true;                 // intialize setting position
      dir[i] = (newPosition[i] - initialPosition[i])/abs(newPosition[i] - initialPosition[i]);  // direction
    }
  }

  // set up base rotation
  newPositionCount = pphr/180.0*lengths[numLinac] - base.getPosition();
  if(newPositionCount != 0){
    rotationInProgress = true;
    base.updatePosition(interrupt_counter*dir[numLinac]);
    interrupt_counter = 0;
    dir[numLinac] = newPositionCount/abs(newPositionCount);
    newPositionCount = abs(newPositionCount);
  }
  
  

}


float* inverseKinematics(float* pos){
  //constants
  float x = pos[0];
  float y = pos[1];
  float z = pos[2];
  float phi = pos[3];
  float a0x = 30.34;
  float a0z = 95.25;
  float a1 = 335.95;
  float a2 = 393;
  //intermediate calculations
  float t = sqrt((x+a0x)*(x+a0x) + y*y);
  float p = z - a0z;
  float c3 = (t*t + p*p - a1*a1 - a2*a2)/(2*a1*a2);
  float g3 = acos(c3);
  float K1 = a1 + a2*cos(g3);
  float K2 = a2*sin(g3);
  float g2 = atan2(p,t) - atan2(K1, K2);
  //output angles
  float T1 = atan2(x,y)*180.0/PI;
  float T2 = 90.0 - g2*180.0/PI;
  float T3 = 180.0  - g3*180.0/PI;
  float T4 = 180.0 + phi - T3 - T2;
  //Actuator lengths
  float L1 = sqrt(130621.0-67573.0*cos(T2+38.84)*PI/180.0) - 292.35;
  float L2 = sqrt(118487.0-50392.0*cos(T3*PI/180.0)) - 292.35;
  float L3 = sqrt(54750.0-24580.0*cos(PI/2.0-T4*PI/180.0)) - 167.5;
  float lengths[] = {L1, L2, L3, T1};
  return lengths;
}

void receiveEvent(int count)
{
	byte in;

	if(new_cmd == true)
		return;

	while(Wire.available())
	{
		in = Wire.read();
		// wait for header
		if(!cmd_count)
		{
			if(in == CMD_HEADER)
			{
				*cmd_ptr = in;
				cmd_count++;
			}
			continue;
		}

		// add middle bytes
		if(cmd_count < sizeof(command))
		{
			cmd_ptr[cmd_count] = in;
			cmd_count++;
		}

		// check for complete
		if(cmd_count == sizeof(command))
		{
			if(in == CMD_TRAILER)
			{
				byte csum = cmd.type + cmd.d1 + cmd.d2 + cmd.d3;
				if(csum == cmd.csum)
                                        //Serial.println("checksum passed");
					new_cmd = true;
			}
			cmd_count = 0;
		}
	}
}

void processCommand()
{
	switch(cmd.type)
	{
		case STOP:
			break;

		case SET_POS:
			position[0] = cmd.d1;
			position[1] = cmd.d2;
			position[2] = cmd.d3;
                        //position[3] = cmd.d4;
			timeout = millis();
			break;

		case NUDGE:
                      break;
	}
}
