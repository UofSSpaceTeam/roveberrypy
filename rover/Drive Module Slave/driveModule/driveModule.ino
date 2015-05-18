#include <Wire.h>

#define TIMEOUT 750
#define CMD_HEADER 0xF7
#define CMD_TRAILER 0xF8
#define I2C_ADDRESS 0x07

enum command_type // instructions from the Pi
{
	SET_MOTORS
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
const byte m_pwm[] = {5, 6, 9, 10, 11, 13};

unsigned long timer;
volatile command cmd;
byte* cmdPointer = (byte*)(&cmd);
volatile byte cmdCount = 0;
volatile bool newCommand = false;

void receiveEvent(int count); // incoming I2C byte

void processCommand();

// index: which motor, 0 to 5
// value: speed, -255 to 255
void setMotor(byte index, short value);

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
	timer = millis();
}

void loop()
{
	if(newCommand)
		processCommand();
	else if(millis() - timer > TIMEOUT)
	{
		stopAll();
		timer = millis();
	}
}

void receiveEvent(int count)
{
	if(newCommand)
		return;
	while(Wire.available())
	{
		byte in = Wire.read();
		
		if(cmdCount == 0) // wait for header
		{
			if(in == CMD_HEADER)
			{
				cmdPointer[cmdCount] = in;
				cmdCount++;
			}
			continue;
		}
		
		if(cmdCount < sizeof(command)) // add middle bytes
		{
			cmdPointer[cmdCount] = in;
			cmdCount++;
		}
		
		if(cmdCount == sizeof(command)) // check for complete
		{
			if(in == CMD_TRAILER)
			{
				byte csum = cmd.type + cmd.d1 + cmd.d2;
				if(csum == cmd.csum)
					newCommand = true;
			}
			cmdCount = 0;
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
		timer = millis();
		break;
	}
	newCommand = false;
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

