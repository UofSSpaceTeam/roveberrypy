// Example code demonstrating I2C communication with an arduino module

#include <Wire.h>

#define TIMEOUT 750
#define CMD_HEADER 0xF7
#define CMD_TRAILER 0xF8
#define I2C_ADDRESS 0x07

enum command_type // instruction class from the Pi
{
	SET_LED
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

// Wiring connections get defined here

const int LEDPins[] = {13};

// I2C data variables and functions

unsigned long timer;
volatile command cmd;
byte* cmdPointer = (byte*)(&cmd);
volatile byte cmdCount = 0;
volatile bool newCommand = false;

void receiveEvent(int count); // incoming I2C byte

void processCommand();

// Specific module functions
void stopAll();

void setup() 
{
	Wire.begin(I2C_ADDRESS);
	Wire.onReceive(receiveEvent);
	
	// Example LED
	pinMode(LEDPins[0], OUTPUT);
	digitalWrite(LEDPins[0], LOW);
	
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
		case SET_LED:
			setLedByVal(cmd.d1, cmd.d2);
			
		break;
	}
	newCommand = false;
}

void setLedByVal(int led, int state)
{
	digitalWrite(LEDPins[led], state);
}

void stopAll()
{
	return;
}

