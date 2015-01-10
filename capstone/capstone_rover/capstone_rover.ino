// Written by Jordan Kubica for CME 495 project, 2014-2015
// Code for the arduino which operates the rover unit

#define DEBUG

// dependencies
#include <Servo.h>

// pin connections
#define SLIDER_PWM 5
#define TABLE_A 7
#define TABLE_B 4
#define TABLE_PWM 6
#define PAN_SERVO_PIN 14
#define TILT_SERVO_PIN 15

// don't change these because interrupts would break
#define SLIDER_A 8
#define SLIDER_B 9
#define LEFT_LIMIT 2
#define RIGHT_LIMIT 3

// configuration
#define PAN_SERVO_MIN 1000
#define PAN_SERVO_MAX 2000
#define TILT_SERVO_MIN 1000
#define TILT_SERVO_MAX 2000

// function prototypes
void setSlider(int rate);
void setTable(int rate);
void limitInterrupt();

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

// command message header and key (header checker)
const byte header[3] = {'m', 's', 'g'};
byte key[3] = {0, 0, 0};

// globals
Servo panServo;
Servo tiltServo;
volatile enum {STOPPED, LEFT, RIGHT} sliderDirection;

// this is run at power-up
void setup()
{
	// configure I/O
	pinMode(SLIDER_A, OUTPUT);
	pinMode(SLIDER_B, OUTPUT);
	pinMode(SLIDER_PWM, OUTPUT);
	pinMode(LEFT_LIMIT, INPUT_PULLUP);
	pinMode(RIGHT_LIMIT, INPUT_PULLUP);
	pinMode(TABLE_A, OUTPUT);
	pinMode(TABLE_B, OUTPUT);
	pinMode(TABLE_PWM, OUTPUT);
	panServo.attach(PAN_SERVO_PIN, PAN_SERVO_MIN, PAN_SERVO_MAX);
	tiltServo.attach(TILT_SERVO_PIN, TILT_SERVO_MIN, TILT_SERVO_MAX);
	
	// initialize output states
	digitalWrite(SLIDER_A, LOW);
	digitalWrite(SLIDER_B, LOW);
	digitalWrite(SLIDER_PWM, LOW);
	sliderDirection = STOPPED;
	digitalWrite(TABLE_A, LOW);
	digitalWrite(TABLE_B, LOW);
	digitalWrite(TABLE_PWM, LOW);
	panServo.write(90);
	tiltServo.write(90);
	
	// set up serial port for XBEE connection
	Serial1.begin(9600);
	Serial1.flush();
	
	// set up interrupts on limit switches
	attachInterrupt(0, limitInterrupt, FALLING);
	attachInterrupt(1, limitInterrupt, FALLING);
	
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
	static command_t_union msg;
	byte i, tmp;
	
	// check serial port for new message data
	if(Serial1.available())
	{
		// shift the next byte
		key[0] = key[1];
		key[1] = key[2];
		key[2] = (byte)Serial1.read();
		
		#ifdef DEBUG
		{
			for(i = 0; i < 3; i++)
				Serial.print(" " + key[i]);
			Serial.println();
		}
		#endif
		
		// check for a complete header
		if((header[0] == key[0]) && (header[1] == key[1]) && (header[2] == key[2]))
		{
			// read in message data
			for(i = 0; i < sizeof(msg); i++)
			{
				while(!Serial1.available());
				msg.cmd_bytes[i] = Serial1.read();
				
				#ifdef DEBUG
					Serial.print("got ");
					Serial.print(i);
					Serial.print(" / ");
					Serial.println(sizeof(msg));
				#endif
			}
			
			// check for a valid checksum
			tmp = (byte)msg.cmd_struct.sliderRate;
			tmp += (byte)msg.cmd_struct.tableRate;
			tmp += (byte)msg.cmd_struct.panPosition;
			tmp += (byte)msg.cmd_struct.tiltPosition;
			
			// execute the commands in the message
			if(msg.cmd_struct.csum == tmp)
			{
				setSlider(msg.cmd_struct.sliderRate);
				setTable(msg.cmd_struct.tableRate);
				panServo.write(msg.cmd_struct.panPosition);
				tiltServo.write(msg.cmd_struct.tiltPosition);
				
				#ifdef DEBUG
					Serial.print("checksum ok: ");
					Serial.println(tmp);
				#endif
			}
			#ifdef DEBUG
				Serial.print("bad checksum: ");
				Serial.print(tmp);
				Serial.print(" != ");
				Serial.println(msg.cmd_struct.csum);
			#endif
		}
	}
}

void setSlider(char rate)
{
	if(rate == 0) // stop slider
	{
		digitalWrite(SLIDER_PWM, LOW);
		digitalWrite(SLIDER_A, LOW);
		digitalWrite(SLIDER_B, LOW);
		sliderDirection = STOPPED;
	}
	else if(rate > 0) // move right
	{
		if(digitalRead(RIGHT_LIMIT) == HIGH) // limit switch not pressed
		{
			digitalWrite(SLIDER_A, HIGH);
			digitalWrite(SLIDER_B, LOW);
			analogWrite(SLIDER_PWM, min(abs(rate * 2), 255));
			sliderDirection = RIGHT;
		}
	}
	else // move left
	{
		if(digitalRead(LEFT_LIMIT) == HIGH); // limit switch not pressed
		{
			digitalWrite(SLIDER_A, LOW);
			digitalWrite(SLIDER_B, HIGH);
			analogWrite(SLIDER_PWM, min(abs(rate * 2), 255));
			sliderDirection = LEFT;
		}
	}
}

void setTable(char rate)
{
	if(rate == 0) // stop table
	{
		digitalWrite(TABLE_PWM, LOW);
		digitalWrite(TABLE_A, LOW);
		digitalWrite(TABLE_B, LOW);
	}
	else if(rate > 0) // rotate clockwise
	{
		digitalWrite(TABLE_A, HIGH);
		digitalWrite(TABLE_B, LOW);
		analogWrite(TABLE_PWM, min(abs(rate), 255));
	}
	else // rotate counterclockwise
	{
		digitalWrite(TABLE_A, LOW);
		digitalWrite(TABLE_B, HIGH);
		analogWrite(TABLE_PWM, min(abs(rate), 255));
	}
}

// ISR which stops the slider when the limit switches are pressed
void limitInterrupt()
{
	PORTB &= B11001111; // sets pins directly on the pro micro board
	sliderDirection = STOPPED;
}

