// Written by Jordan Kubica for CME 495 project, 2014-2015
// Code for the arduino which operates the base unit

// dependencies
#include <Servo.h>

// pin connections
#define TRACKER_IN 5
#define SERVO_OUT 6

// command message struct
typedef struct
{
	byte panPosition;
	byte tiltPosition;
	byte motors;
	byte csum;
} command_t;

// union for handling messages bytewise
typedef union
{
	command_t cmd_struct;
	byte cmd_bytes[sizeof(command_t)];
} command_t_union;

// initial calibration values
int panMax = 1560;
int panMin = 430;
int tiltMax = 1300;
int tiltMin = 700;
int rollMax = 1560;
int rollMin = 430;

// calibration starting servo
Servo buttonServo;

void setup()
{
	// usb serial connection for calibration / control
	Serial.begin(9600);
	Serial.flush();
	
	// set up serial port for XBEE connection to rover
	Serial1.begin(9600);
	Serial1.flush();
	
	// button pressing servo
	buttonServo.attach(SERVO_OUT);
	buttonServo.write(90);
}

void loop()
{
	command_t_union msg;
	unsigned long blankPulse, panPulse, tiltPulse, rollPulse;
	byte pan, tilt, roll, csum, i;
	byte buffer[sizeof(command_t_union) + 2];
	byte calState = 0;
	int panZero, tiltZero, rollZero;
	
	// check for calibration request
	if(Serial.available())
	{
		switch(Serial.read())
		{
			case 's': // start calibration
			{
				// first, push HT center button
				buttonServo.write(70);
				delay(500);
				buttonServo.write(90);
				Serial.println("Calibration started - Set Centerpoint");
				calState = 1;
				break;
			}
			case 'n': // continue calibration
			{
				if(calState == 1)
				{
					panZero = panPulse;
					tiltZero = tiltPulse;
					rollZero = rollPulse;
					Serial.println("Centerpoint set. Set Pan Endpoint");
					calState = 2;
				}
				else if(calState == 2)
				{
					if(panPulse > panZero)
						panMax = panPulse;
						panMin = 2 * panZero - panMax;
					else
						panMin = panPulse;
						panMax = 2 * panZero - panMin;
					Serial.println("Pan Endpoint set. Set Tilt Endpoint");
					calState = 3;
				}
				else if(calState == 3)
				{
					if(tiltPulse > tiltZero)
						tiltMax = tiltPulse;
						tiltMin = 2 * tiltZero - tiltMax;
					else
						tiltMin = tiltPulse;
						tiltMax = 2 * tiltZero - tiltMin;
					Serial.println("Tilt Endpoint set. Set Roll Endpoint");
					calState = 4;
				}
				else if(calState == 4)
				{
					if(rollPulse > rollZero)
						rollMax = rollPulse;
						rollMin = 2 * rollZero - rollMax;
					else
						rollMin = rollPulse;
						rollMax = 2 * rollZero - rollMin;
					Serial.println("Roll Endpoint set. Calibration Complete");
					calState = 0;
				}
				break;
			}
		}
	}
	
	// wait for the start of an r/c frame from the headtracker
	do
	{
		blankPulse = pulseIn(TRACKER_IN, HIGH, 100000);
	} while(blankPulse < 5000);
	
	// ignore channels 1-3
	for(i = 0; i < 3; i++)
		pulseIn(TRACKER_IN, HIGH, 100000);
	
	// measure the relevant pulses
	do
	{
		rollPulse = pulseIn(TRACKER_IN, HIGH, 100000); // ch 4
		panPulse = pulseIn(TRACKER_IN, HIGH, 100000); // ch 5
		tiltPulse = pulseIn(TRACKER_IN, HIGH, 100000); // ch 6
	} while(!panPulse || !tiltPulse || !rollPulse);
	
	// calibration mode
	if(calState)
		return;
	
	// translate pulse length to degrees
	pan = map(constrain(panPulse, panMin, panMax), panMin, panMax, 0, 180);
	tilt = map(constrain(tiltPulse, tiltMin, tiltMax), tiltMin, tiltMax, 0, 180);
	roll = map(constrain(rollPulse, rollMin, rollMax), rollMin, rollMax, 0, 180);
	
	// fill in command message
	msg.cmd_struct.panPosition = pan;
	msg.cmd_struct.tiltPosition = tilt;
	
	// panning near edge of range turns table
	if(pan > 155)
		msg.cmd_struct.motors = 0x01;
	else if(pan < 25)
		msg.cmd_struct.motors = 0x02;
	else
		msg.cmd_struct.motors = 0x00;
	
	// roll axis controls slider
	if(roll > 140)
		msg.cmd_struct.motors |= 0x04;
	else if(roll < 40)
		msg.cmd_struct.motors |= 0x08;
	
	// compute checksum
	msg.cmd_struct.csum = (byte)(msg.cmd_struct.panPosition
	+ msg.cmd_struct.tiltPosition
	+ msg.cmd_struct.motors);
	
	// send complete message
	buffer[0] = 'm';
	buffer[1] = 's';
	for(i = 0; i < sizeof(command_t_union); i++)
		buffer[i + 2] = msg.cmd_bytes[i];
	
	// wait a bit before the next message
	delay(10);
}






