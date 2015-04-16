// Code for the Arduino controlling the arm drivers.
// Adapted from the driveModule
// Written for Arduino Micro.

#include <Wire.h>

#define TIMEOUT 750

// definition of structures and enums

enum command_type // instructions from the Pi
{
	STOP, // stop all motors
	SET_POS, // set desired speed for left / right sides
};

typedef struct
{
	byte header;
	byte type; // actually used as enum command_type, that's ok
	short d1; // x direction
	short d2; // y direction
	short d3; // z direction
	byte csum; // sum of cmd_type, d1, d2, d3
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
motor_state m_state[] = {OK, OK, OK}; // current state
volatile short position[] = {0, 0, 0}; // commanded speed commanded

// state information
const byte CMD_HEADER = 0xF7;
const byte CMD_TRAILER = 0xF8;
unsigned long timeout;
volatile command cmd;
byte* cmd_ptr = (byte*)(&cmd);
volatile byte cmd_count = 0;
volatile bool new_cmd = false;


// function prototypes

// Interrupt handler for receiving a byte via I2C
void receiveEvent(int count);

// function to actually process command
void processCommand();

// Could be used to send data to the Pi, watch out for 5v <-> 3.3v issues
void requestEvent();

// functions

void setup()
{
	Serial.begin(9600); // debug
	Wire.begin(i2c_address);
	Wire.onReceive(receiveEvent);
	Wire.onRequest(requestEvent);

	// initialize outputs (done by the H_Bridge class)

	// clear cmd struct
	for(int i = 0; i < sizeof(command); i++)
		cmd_ptr[i] = 0x00;

	// arm timeout
	timeout = millis();
}

void loop()
{
	if(new_cmd)
	{
		processCommand();
		new_cmd = false;
	}
	
	//Do stuff here
        Serial.println(position[0]);
        Serial.println(position[1]);
        Serial.println(position[2]);

	/*if(millis() - timeout > TIMEOUT)
	{
		Serial.println("TO");
		timeout = millis();
	}*/
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
	// Serial.println("got command");
	switch(cmd.type)
	{
		case STOP:
			break;

		case SET_POS:
			/* bounds checking
			if(cmd.d1 > 255 || cmd.d1 < -255)
				break; */
			position[0] = cmd.d1;
			position[1] = cmd.d2;
			position[2] = cmd.d3;
			timeout = millis();
			break;

		/*case SET_MOTOR:
			if(cmd.d1 < 0 || cmd.d1 > 5)
				break;
			position[cmd.d1] = cmd.d2;
			timeout = millis();
			break; */
	}
}

void requestEvent()
{
	return;
}

