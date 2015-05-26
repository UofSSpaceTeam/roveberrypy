// Code for the Arduino controlling the motor drivers.
// Written for Arduino Micro.
#include <Servo.h>
#include <Wire.h>

#define TIMEOUT 2500
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
	int d1; // 16-bit signed
	int d2;
	byte csum; // sum of cmd_type, d1, d2
	byte trailer;
} command;


/*
	Wiring connections.
	Each motor only takes a servo pulse
	Two Lasers have an enable HIGH, one enable LOW
*/

// pin connetions for motor
const byte l_pwr[] = {4, 6, 5};
byte drillPin = 10;
byte elevPin = 11;

// arduino address on bus
const byte i2c_address = 0x09;

// servo stuff for motors
Servo drillMotor;
short drillSpeed = 0;
short desiredDrillSpeed = 0;
Servo elevMotor;
short elevSpeed = 0;
short desiredElevSpeed = 0;

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


void receiveEvent(int count);
void processCommand();
void updateDrill();
void updateElev();
void stopAll();
/*
	Turns on a single laser
	index: which laser, [0, 1, 2]
	value: on or off [0, 1]
*/
void setLaser(byte index, short value);

void setup()
{
	Serial.begin(9600);
	Wire.begin(i2c_address);
	Wire.onReceive(receiveEvent);
	
	pinMode(drillPin, OUTPUT);
	pinMode(elevPin, OUTPUT);
	for(int i = 0; i < 3; i++)
		pinMode(l_pwr[i], OUTPUT);
	
	drillMotor.attach(drillPin);
	elevMotor.attach(elevPin);
	stopAll();
		
	timeout = millis();
	prevTime = timeout;
}

void loop()
{
	if(new_cmd)
		processCommand();
	
	updateDrill();
	updateElev();
	
	if(millis() - timeout > TIMEOUT)
	{
		Serial.println("TO");
		stopAll();
		timeout = millis();
	}
	for(int i = 0; i < 3; i++)
		setLaser(i, l_cmd[i]);
	delay(50);
}

void processCommand()
{
	switch(cmd.type)
	{
		case STOP:
		stopAll();
		break;
		
		case SET_SPEED:
		desiredDrillSpeed = constrain(cmd.d1, -255, 255);
		desiredElevSpeed = constrain(cmd.d2, -255, 255);
		timeout = millis();
		break;
		
		case SET_LASER:
		Serial.println("laser");
		if(cmd.d1 > 3 || cmd.d1 < 0)
			break;
		if(cmd.d2 > 1 || cmd.d1 < 0)
			break;
		l_cmd[cmd.d1 - 1] = cmd.d2;
		timeout = millis();
		Serial.print(cmd.d1);
		Serial.print(", ");
		Serial.println(cmd.d2);
		break;
	}
	new_cmd = false;
}

void updateDrill()
{
	if(desiredDrillSpeed == 0)
	{
		drillMotor.writeMicroseconds(1500);
		return;
	}
	else if(abs(desiredDrillSpeed - drillSpeed) < 5)
		drillSpeed = desiredDrillSpeed;
	else if(desiredDrillSpeed > drillSpeed)
		drillSpeed += 5;
	else
		drillSpeed -= 5;
	drillMotor.writeMicroseconds(map(drillSpeed, -255, 255, 900, 2100));
}
	
void updateElev()
{
	if(desiredElevSpeed == 0)
	{
		elevMotor.writeMicroseconds(1500);
		return;
	}
	else if(abs(desiredElevSpeed - elevSpeed) < 5)
		elevSpeed = desiredElevSpeed;
	else if(desiredElevSpeed > elevSpeed)
		elevSpeed += 5;
	else
		elevSpeed -= 5;
	elevMotor.writeMicroseconds(map(elevSpeed, -255, 255, 900, 2100));
}

void setLaser(byte index, short value)
{
  //Serial.print(l_pwr[index]);
  //Serial.println(value);
  if(index == 2){
	//if(value) Serial.println("P Laser On");
	//else Serial.println("P Laser Off");  
   digitalWrite(l_pwr[index], !value);
  }
  else{
	digitalWrite(l_pwr[index], value);
	}
}

void stopAll()
{
	Serial.println("stopped");
	drillSpeed = 0;
	desiredDrillSpeed = 0;
	elevSpeed = 0;
	desiredElevSpeed = 0;
	drillMotor.writeMicroseconds(1500);
	elevMotor.writeMicroseconds(1500);
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

