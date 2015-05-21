// Code for the Arduino controlling the motor drivers.
// Written for Arduino Micro.
#include <Servo.h>
#include <Wire.h>

#define TIMEOUT 2500000
#define PULSE_TIME 30

// definition of structures and enums

enum command_type // instructions from the Pi
{
	STOP, // stop all motors
	SET_SPEED, // set desired speed for drill / elevator
	SET_LASER // Turn on/off desired laser
};

typedef struct
{	
	byte header;
	byte type; // actually used as enum command_type, that's ok
	short d1; // 16-bit signed
	short d2;
	byte csum; // sum of cmd_type, d1, d2
	byte trailer;
} command;


/*
	Wiring connections.
	Each motor only takes a servo pulse
	Two Lasers have an enable HIGH, one enable LOW
*/

// pin connetions for motor
const byte m_pwm[] = {9, 10};
const byte l_pwr[] = {4, 6, 5};

// arduino address on bus
const byte i2c_address = 0x09;

// servo stuff for motors
Servo drillMotor;
Servo elevMotor;

// control data
volatile short m_cmd[] = {0, 0}; // commanded speeds
volatile short l_cmd[] = {0, 0, 0}; // commanded lasers

// state information
const byte CMD_HEADER = 0xF7;
const byte CMD_TRAILER = 0xF8;
unsigned long timeout;
unsigned long prevTime;
volatile command cmd;
byte* cmd_ptr = (byte*)(&cmd);
volatile byte cmd_count = 0;
volatile bool new_cmd = false;


// function prototypes

// Interrupt handler for receiving a byte via I2C
void receiveEvent(int count);

// function to actually process command
void processCommand();

/*
	sets a single motor to the specified direction and power level.
	index: which motor, [0, 1]
	value: speed and direction, [-255, 255]
*/
void setMotor(byte index, short value);

/*
	Turns on a single laser
	index: which laser, [0, 1, 2]
	value: on or off [0, 1]
*/
void setLaser(byte index, short value);

// stops all motors and lasers.
void stopAll();


// functions

void setup() {
	Serial.begin(9600); // debug
	Wire.begin(i2c_address);
	Wire.onReceive(receiveEvent);
	Wire.onRequest(requestEvent);
		
	drillMotor.attach(m_pwm[0]);
	elevMotor.attach(m_pwm[1]);
	
	// clear cmd struct
	for(int i = 0; i < sizeof(command); i++)
		cmd_ptr[i] = 0x00;
	
	// arm timeout
	timeout = millis();
	prevTime = millis();
}

void loop()
{
	if(new_cmd)
	{	 
		//Serial.println("New Command");
		processCommand();
		new_cmd = false;
	}
	for(int i = 0; i < 2; i++)
	{	
		setMotor(i, m_cmd[i]);
		
		if(millis() - timeout > TIMEOUT)
		{
			Serial.println("TO");
			stopAll();
			timeout = millis();
		}
	}
	for(int i = 0; i < 3; i++) {
		setLaser(i, l_cmd[i]);
	}
}

void receiveEvent(int count)
{
	byte in;
	
	if(new_cmd == true)
		return;
	
	while(Wire.available())
	{
		in = Wire.read();
				//Serial.println(in);
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
				byte csum = cmd.type + cmd.d1 + cmd.d2;
				if(csum == cmd.csum)
					new_cmd = true;
			}
			cmd_count = 0;
		}
	}
}

void processCommand()
{
	//Serial.println("got command");
		//Serial.println(cmd.type);
		switch(cmd.type)
	{
		case STOP:
		stopAll();
		break;
		
		case SET_SPEED:
		//Serial.print(cmd.d1);
		//Serial.print(" ");
		//Serial.println(cmd.d2);
		if(cmd.d1 > 255 || cmd.d1 < -255)
			break;
		if(cmd.d2 > 255 || cmd.d2 < -255)
			break;
		m_cmd[0] = cmd.d1;
		m_cmd[1] = cmd.d2;
			timeout = millis();
		break;
		
		case SET_LASER:
		if(cmd.d1 > 3 || cmd.d1 < 0)
			break;
		if(cmd.d2 > 1 || cmd.d1 < 0)
			break;
		l_cmd[cmd.d1 - 1] = cmd.d2;
			timeout = millis();
		break;
		
	}
}

void requestEvent()
{
	return;
}

void setMotor(byte index, short value)
{
		int pwm = map(value, -255, 255, 800, 2200);
		//Serial.print(index);
		//Serial.print(':');
		//Serial.println(pwm);
		if(index == 0) {
		  if(value == 0) {
			drillMotor.writeMicroseconds(1500);
		  }
		 else{
			drillMotor.writeMicroseconds(pwm);
		 }
		}
		else {
			if(value == 0) {
				elevMotor.writeMicroseconds(1500);
			}
		else {
			elevMotor.writeMicroseconds(pwm);
		}
	}
}

void setLaser(byte index, short value)
{
  if(index == 2){
    if(value) Serial.println("Pen Laser On");  
   digitalWrite(l_pwr[index], !value);
  }
  else{
    if(value){
      //if(value && index == 0) Serial.println("A Laser On");
      //if(value && index == 1) Serial.println("B Laser On");
      pinMode(l_pwr[index], INPUT);
    }
    else{
      pinMode(l_pwr[index], OUTPUT);
      digitalWrite(l_pwr[index], LOW);
    }
  }
}

void stopAll()
{
	Serial.println("stopped");
		drillMotor.writeMicroseconds(1500);
		elevMotor.writeMicroseconds(1500);

}
