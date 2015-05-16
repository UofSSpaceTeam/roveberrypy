#include "VNH3SP30.h"
#include <Wire.h>

// pin connections
#define L1inA 0
#define L1inB 1
#define L1pwm 3
#define L2inA 2 
#define L2inB 7 
#define L2pwm 4
#define L3inA 8
#define L3inB 11
#define L3pwm 5
#define BASEinA 12
#define BASEinB 13
#define BASEpwm 6

#define TIMEOUT 750

// definition of structures and enums

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


int numLinac = 3;

// create objects
VNH3SP30 linac[3] = { VNH3SP30(L1inA, L1inB, L1pwm) ,
                      VNH3SP30(L2inA, L2inB, L2pwm) ,
                      VNH3SP30(L3inA, L3inB, L3pwm) };
VNH3SP30 base (BASEinA, BASEinB, BASEpwm);

// ------------------- set positions --------------------------
float pos[4] = {400,0,100,-60};

// global variable definitions


// arduino address on bus
const byte i2c_address = 0x08;

// traction control data
motor_state m_state[] = {OK, OK, OK, OK}; // current state
volatile int position[] = {0, 0, 0, 0}; // commanded speed commanded

// state information
const byte CMD_HEADER = 0xF7;
const byte CMD_TRAILER = 0xF8;
unsigned long timeout;
volatile command cmd;
byte* cmd_ptr = (byte*)(&cmd);
volatile byte cmd_count = 0;
volatile bool new_cmd = false;

int wiper[3], minimum[3],maximum[3];
float scalingCoeff[3], positions[4], setTo, curr;
int interrupt_counter, newPositionCount, dir;
const int pphr = 13390;
int base_dir;
void positionChange(){ interrupt_counter ++; }
int tolerance[4] = {4,4,6,5} ;

// function prototypes

// Interrupt handler for receiving a byte via I2C
void receiveEvent(int count);

// function to actually process command
void processCommand();

// Could be used to send data to the Pi, watch out for 5v <-> 3.3v issues
void requestEvent(); //currently not used

void setup() {
  // setup serial
  Serial.begin(9600);
  delay(2000);
  Serial.println("ARM_controller test!");
  Wire.begin(i2c_address);
  Wire.onReceive(receiveEvent);
  Wire.onRequest(requestEvent);
  //initalize interrupts
  pinMode(20,INPUT);
  pinMode(21,INPUT);
  attachInterrupt(20,positionChange,CHANGE);
  attachInterrupt(21,positionChange,CHANGE);
  
  // clear cmd struct
  for(unsigned int i = 0; i < sizeof(command); i++)
    cmd_ptr[i] = 0x00;
  

  //initalize pins and linear actuator constants
  wiper[0] = A2;
  minimum[0] = 591;//595
  maximum[0] = 870;
  scalingCoeff[0] = 0.3893;

  wiper[1] = A1;
  minimum[1] = 617; //622
  maximum[1] = 862;
  scalingCoeff[1] = 0.3878;//0.3878

  wiper[2] = A0;
  minimum[2] = 412;
  maximum[2] = 832;
  scalingCoeff[2]=0.238;
  
  // make sure the linac are in brake position
  for(int i = 0; i < numLinac ; i++){
    linac[i].setDutyCycle(0);
  }
  base_dir = 0;
  
  // arm timeout
  timeout = millis();
}
void loop() {
  if(new_cmd) {
    processCommand();
    new_cmd = false;
  }
  
  inverseKinematics(pos);
  setPosition();
  
  if(millis() - timeout > TIMEOUT) {
    Serial.println("TO");
    timeout = millis();
  }
}

void setPosition(){
  for(int i = 0; i < numLinac ; i ++){
    setTo = minimum[i]+positions[i]/scalingCoeff[i];
    float sum = 0;
    for(int j = 0 ; j < 5 ; j++){
      sum += analogRead(wiper[i]);
    } 
    
    curr = sum/5;
    dir = (setTo - curr)/abs(setTo - curr);
    if((abs(curr-setTo) > tolerance[i])&& !((curr <= minimum[i])&&(dir==-1)) && !((curr >= maximum[i])&&(dir==1)) ){
      linac[i].setDutyCycle(255*dir);
    }
    else{linac[i].setDutyCycle(0);}
  }
  
  base.updatePosition(interrupt_counter*base_dir);
  interrupt_counter = 0;
  newPositionCount = pphr/180.0*positions[numLinac]-base.getPosition();
  base_dir = newPositionCount/abs(newPositionCount);
  newPositionCount = abs(newPositionCount);
  if(newPositionCount > tolerance[numLinac]){base.setDutyCycle(255*base_dir);}
  else{
    base.setDutyCycle(0);
    base_dir = 0;
  }
}
void inverseKinematics(float* coordinate){
  //constants
  float x = coordinate[0];
  float y = coordinate[1];
  float z = coordinate[2];
  float phi = coordinate[3];
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
  positions[3] = atan2(y,x)*180.0/PI; //theta 1
  float T2 = 90.0 - g2*180.0/PI;
  float T3 = 180.0  - g3*180.0/PI;
  float T4 = 180.0 + phi - T3 - T2;
  //Actuator lengths
  positions[0] = sqrt(130621.0-67573.0*cos((T2+38.84)*PI/180)) - 292.35;
  positions[1] = sqrt(118487.0-50392.0*cos(T3*PI/180.0)) - 292.35;
  positions[2] = sqrt(54750.0-24580.0*cos(PI/2.0-T4*PI/180.0)) - 167.5;
  positions[1] = map(positions[1],9,104,0,104);
  positions[2] = map(positions[2],33,100,0,100);

  Serial.print("L1: ");
  Serial.println(positions[0]);
  Serial.print("L2: ");
  Serial.println(positions[1]);
  Serial.print("L3: ");
  Serial.println(positions[2]);
  Serial.print("Base: ");
  Serial.println(positions[3]);
  Serial.println(t);
  Serial.println(p);
  Serial.println(c3);
  Serial.println(g3);
  Serial.println(K1);
  Serial.println(K2);
  
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

void requestEvent()
{
	return;
}

