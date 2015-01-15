// Written by Jordan Kubica for CME 495 project, 2014-2015
// Code for the arduino which operates the base unit

//#define DEBUG

// pin connections
#define TRACKER_IN 5

// configuration
#define PAN_MAX 1560
#define PAN_MIN 430
#define TILT_MAX 1200
#define TILT_MIN 600
#define ROLL_MAX 1560
#define ROLL_MIN 430

// command message struct
typedef struct
{
	char sliderRate;
	char tableRate;
	byte panPosition;
	byte tiltPosition;
	byte csum;
} command_t;

// union for handling messages bytewise
typedef union
{
	command_t cmd_struct;
	byte cmd_bytes[sizeof(command_t)];
} command_t_union;

// command message header
const byte header[2] = {'m', 's'};

// this is run at power-up
void setup()
{
	// configure I/O
	
	// initialize output states
	
	// set up serial port for XBEE connection
	Serial1.begin(9600);
	Serial1.flush();
	
	#ifdef DEBUG
	{
		Serial.begin(9600);
		Serial.println("Hello world!");
	}
	#endif
}

// runs forever
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
		pulseIn(TRACKER_IN, HIGH, 10000);
	
	// measure the relevant pulses
	rollPulse = pulseIn(TRACKER_IN, HIGH, 10000); // ch 4
	panPulse = pulseIn(TRACKER_IN, HIGH, 10000); // ch 5
	tiltPulse = pulseIn(TRACKER_IN, HIGH, 10000); // ch 6
	
	// check for time out
	if(!panPulse || !tiltPulse || !rollPulse)
		return;
	
	// translate pulse length to degrees
	pan = map(constrain(panPulse, PAN_MIN, PAN_MAX), PAN_MIN, PAN_MAX, 180, 0);
	tilt = map(constrain(tiltPulse, TILT_MIN, TILT_MAX), TILT_MIN, TILT_MAX, 180, 0);
	roll = map(constrain(rollPulse, ROLL_MIN, ROLL_MAX), ROLL_MIN, ROLL_MAX, 0, 180);
	
	// fill in command message
	msg.cmd_struct.panPosition = pan;
	msg.cmd_struct.tiltPosition = tilt;
	
	// panning near edge of range turns table
	if(pan > 155)
		msg.cmd_struct.tableRate = 127;
	else if(pan < 25)
		msg.cmd_struct.tableRate = -127;
	else
		msg.cmd_struct.tableRate = 0;
	
	// roll axis controls slider
	if(roll > 130)
		msg.cmd_struct.sliderRate = 127;
	else if(roll < 50)
		msg.cmd_struct.sliderRate = -127;
	else
		msg.cmd_struct.sliderRate = 0;
	
	// compute checksum
	msg.cmd_struct.csum = msg.cmd_struct.panPosition + msg.cmd_struct.tiltPosition;
	msg.cmd_struct.csum += msg.cmd_struct.tableRate + msg.cmd_struct.sliderRate;
	
	// send complete message
	for(i = 0; i < 2; i++)
		buffer[i] = header[i];
	for(i = 0; i < sizeof(command_t_union); i++)
		buffer[i + 2] = msg.cmd_bytes[i];
	Serial1.write(buffer, sizeof(buffer));
	
	#ifdef DEBUG
	{
		Serial.print("  Pan: ");
		Serial.print(pan);
		Serial.print("\t  Tilt: ");
		Serial.print(tilt);
		Serial.print("\t  Roll: ");
		Serial.println(roll);
		Serial.print("  Slider: ");
		Serial.print((int)msg.cmd_struct.sliderRate);
		Serial.print("\t  Table: ");
		Serial.print((int)msg.cmd_struct.tableRate);
		Serial.print("\t  Csum: ");
		Serial.println(msg.cmd_struct.csum);
	}
	#endif
	
	// wait a bit before the next message
	delay(10);
}

