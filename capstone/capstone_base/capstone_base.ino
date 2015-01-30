// Written by Jordan Kubica for CME 495 project, 2014-2015
// Code for the arduino which operates the base unit

// pin connections
#define TRACKER_IN 5

// configuration
#define PAN_MAX 1560
#define PAN_MIN 430
#define TILT_MAX 1300
#define TILT_MIN 700
#define ROLL_MAX 1560
#define ROLL_MIN 430

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

void setup()
{	
	// set up serial port for XBEE connection
	Serial1.begin(9600);
	Serial1.flush();
}

void loop()
{
	command_t_union msg;
	unsigned long blankPulse, panPulse, tiltPulse, rollPulse;
	byte pan, tilt, roll, csum, i;
	byte buffer[sizeof(command_t_union) + 2];
	
	// wait for the start of an r/c frame from the headtracker
	do
	{
		blankPulse = pulseIn(TRACKER_IN, HIGH, 100000);
	} while(blankPulse < 5000);
	
	// ignore channels 1-3
	for(i = 0; i < 3; i++)
		pulseIn(TRACKER_IN, HIGH, 100000);
	
	// measure the relevant pulses
	rollPulse = pulseIn(TRACKER_IN, HIGH, 100000); // ch 4
	panPulse = pulseIn(TRACKER_IN, HIGH, 100000); // ch 5
	tiltPulse = pulseIn(TRACKER_IN, HIGH, 100000); // ch 6
	
	// check for time out
	if(!panPulse || !tiltPulse || !rollPulse)
		return;
	
	// translate pulse length to degrees
	pan = map(constrain(panPulse, PAN_MIN, PAN_MAX), PAN_MIN, PAN_MAX, 0, 180);
	tilt = map(constrain(tiltPulse, TILT_MIN, TILT_MAX), TILT_MIN, TILT_MAX, 0, 180);
	roll = map(constrain(rollPulse, ROLL_MIN, ROLL_MAX), ROLL_MIN, ROLL_MAX, 0, 180);
	
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
	Serial1.write(buffer, sizeof(buffer));
	
	// wait a bit before the next message
	delay(10);
}






