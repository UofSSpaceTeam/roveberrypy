// Written by Jordan Kubica for CME 495 project, 2014-2015
// Code for the arduino which operates the rover unit
#include <Servo.h>

// pin connections
#define TABLE_A 8
#define TABLE_B 9
#define TABLE_PWM 5
#define PAN_SERVO_PIN 14
#define TILT_SERVO_PIN 10

// configuration
#define TIMEOUT 750
#define PAN_SERVO_MIN 940
#define PAN_SERVO_MAX 2100
#define TILT_SERVO_MIN 900
#define TILT_SERVO_MAX 2100

// function prototypes
void tableLeft();
void tableRight();
void tableStop();

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

// checks for message header
byte key[2] = {0, 0};

Servo panServo;
Servo tiltServo;

// timeout counter
unsigned long timer = 0;

void setup()
{
	// configure I/O
	pinMode(TABLE_A, OUTPUT);
	pinMode(TABLE_B, OUTPUT);
	pinMode(TABLE_PWM, OUTPUT);
	panServo.attach(PAN_SERVO_PIN, PAN_SERVO_MIN, PAN_SERVO_MAX);
	tiltServo.attach(TILT_SERVO_PIN, TILT_SERVO_MIN, TILT_SERVO_MAX);
	
	// initialize output states
	tableStop();
	panServo.write(90);
	tiltServo.write(90);
	
	// set up serial port for XBEE connection
	Serial1.begin(9600);
	Serial1.flush();
}

// runs forever
void loop()
{
	static command_t_union msg;
	byte i;
		
	// check serial port for new message data
	if(Serial1.available())
	{
		// shift in the next byte
		key[0] = key[1];
		key[1] = (byte)Serial1.read();
		
		// check for a complete header
		if((key[0] == 'm') && (key[1] == 's'))
		{
			// reset key
			key[0] = 0;
			key[1] = 0;
			
			// read in message data
			for(i = 0; i < sizeof(command_t_union); i++)
			{
				while(!Serial1.available());
				msg.cmd_bytes[i] = Serial1.read();
			}
			
			// check for a valid checksum
			if((byte)msg.cmd_struct.csum == (byte)(msg.cmd_struct.panPosition
				+ msg.cmd_struct.tiltPosition + msg.cmd_struct.motors))
			{
				timer = millis();
  				panServo.write(180 - msg.cmd_struct.panPosition);
				tiltServo.write(180 - msg.cmd_struct.tiltPosition);
				
				if(msg.cmd_struct.motors & 0x01)
					tableLeft();
				else if(msg.cmd_struct.motors & 0x02)
					tableRight();
				else
					tableStop();
			}
		}
	}
	if(millis() - timer > TIMEOUT) // check timeout
		tableStop();
}

void tableLeft()
{
	digitalWrite(TABLE_A, HIGH);
	digitalWrite(TABLE_B, LOW);
	digitalWrite(TABLE_PWM, HIGH);
}

void tableRight()
{
	digitalWrite(TABLE_A, LOW);
	digitalWrite(TABLE_B, HIGH);
	digitalWrite(TABLE_PWM, HIGH);
}

void tableStop()
{
	digitalWrite(TABLE_PWM, LOW);
	digitalWrite(TABLE_A, LOW);
	digitalWrite(TABLE_B, LOW);
}

