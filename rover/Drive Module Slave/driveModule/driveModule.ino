// Code for the Arduino controlling the motor drivers.
// Written for Arduino Micro.

#include <Wire.h>

#define TIMEOUT 750
#define CMD_HEADER 0xF7
#define CMD_TRAILER 0xF8
#define I2C_ADDRESS 0x07

enum command_type // instructions from the Pi
{
	SET_MOTORS // 0: set power for left and right side motors
};

typedef struct
{	
	byte header;
	byte type;
	short d1; // 16-bit signed
	short d2;
	byte csum; // sum of cmd_type, d1, d2
	byte trailer;
} command;

// Wiring connections per motor
const byte m_a[] = {12, 12, 12, 4, 4, 4};
const byte m_b[] = {8, 8, 8, 7, 7, 7};
const byte m_pwm[] = {5, 6, 9, 10, 11, 13}; //5 6 9 10 11 13

unsigned long timeout;
volatile command cmd;
byte* cmd_ptr = (byte*)(&cmd);
volatile byte cmd_count = 0;
volatile bool new_cmd = false;

// Interrupt handler for receiving a byte via I2C
void receiveEvent(int count);

// function to actually process command
void processCommand();

// sets a single motor to the specified direction and power level.
// index: which motor, 0 to 5
// value: speed and direction, -255 to 255
void setMotor(byte index, short value);

// stops all motors.
void stopAll();

void setup() 
{
	Wire.begin(I2C_ADDRESS);
	Wire.onReceive(receiveEvent);
	
	for(int i = 0; i < 6; i++)
	{
		pinMode(m_a[i], OUTPUT);
		pinMode(m_b[i], OUTPUT);
		pinMode(m_pwm[i], OUTPUT);
	}
	stopAll();
	timeout = millis();
}

void loop()
{
	if(new_cmd)
		processCommand();
	else if(millis() - timeout > TIMEOUT)
	{
		stopAll();
		timeout = millis();
	}
}

void receiveEvent(int count)
{
	if(new_cmd)
		return;
	while(Wire.available())
	{
		byte in = Wire.read();
		
		// wait for header
		if(cmd_count == 0)
		{
			if(in == CMD_HEADER)
			{
				cmd_ptr[cmd_count] = in;
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
	switch(cmd.type)
	{		
		case SET_MOTORS:
		cmd.d1 = constrain(cmd.d1, -255, 255);
		cmd.d2 = constrain(cmd.d2, -255, 255);
		setMotor(0, cmd.d1);
		setMotor(1, cmd.d1);
		setMotor(2, cmd.d1);
		setMotor(3, cmd.d2);
		setMotor(4, cmd.d2);
		setMotor(5, cmd.d2);
		timeout = millis();
		break;
	}
	new_cmd = false;
}

void setMotor(byte index, short value)
{
	if(value == 0)
		digitalWrite(m_pwm[index], LOW);
	else if(value > 0)
	{
		digitalWrite(m_a[index], HIGH);
		digitalWrite(m_b[index], LOW);
		analogWrite(m_pwm[index], abs(value));
	}
	else
	{
		digitalWrite(m_a[index], LOW);
		digitalWrite(m_b[index], HIGH);
		analogWrite(m_pwm[index], abs(value));
	}
}

void stopAll()
{
	for(int i = 0; i < 6; i++)
		setMotor(i, 0);
}

