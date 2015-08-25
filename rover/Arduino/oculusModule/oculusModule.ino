#include <Servo.h>

#define DIR_PIN 7
#define STEP_PIN 4
#define MS1_PIN 2
#define MS2_PIN 3
#define TILT_SERVO_PIN 6
#define EXPOSURE_PIN 5
#define STEPS_PER_DEGREE 3.7 // ~1330 steps/rev
#define TILT_SERVO_MIN 900
#define TILT_SERVO_MAX 2100

byte key[3] = {0, 0, 0};
int panPosition = 0;
int commandedPosition = 0;
Servo tiltServo;

void setup()
{
	Serial.begin(9600);
	pinMode(DIR_PIN, OUTPUT);
	pinMode(STEP_PIN, OUTPUT);
	pinMode(MS1_PIN, OUTPUT);
	pinMode(MS2_PIN, OUTPUT);
	pinMode(EXPOSURE_PIN, OUTPUT);
	tiltServo.attach(TILT_SERVO_PIN, TILT_SERVO_MIN, TILT_SERVO_MAX);
	digitalWrite(DIR_PIN, LOW);
	digitalWrite(STEP_PIN, LOW);
	digitalWrite(MS1_PIN, HIGH);
	digitalWrite(MS2_PIN, LOW);
	digitalWrite(EXPOSURE_PIN, LOW);
	tiltServo.write(90);
}

void loop()
{
	int diff = commandedPosition - panPosition;
	if(diff)
	{
		spin(diff);
		panPosition += diff;
	}
	if(Serial.available())
	{
		key[0] = key[1];
		key[1] = key[2];
		key[2] = (byte)Serial.read();
		if(key[0] == 'm' && key[1] == 's' && key[2] == 'g')
		{
			key[0] = 0;
			key[1] = 0;
			while(Serial.available() < 3);
			commandedPosition = Serial.read() << 8;
			commandedPosition += Serial.read();
			tiltServo.write(180 - Serial.read());
		}
	}
}

void spin(int deg)
{
	if(deg > 0)
		digitalWrite(DIR_PIN, HIGH);
	else
		digitalWrite(DIR_PIN, LOW);
	step(abs(round(deg * STEPS_PER_DEGREE)));
	delay(70);
}

void step(int steps)
{
	for(int i = 0; i < steps; i++)
	{
		digitalWrite(STEP_PIN, HIGH);
		delayMicroseconds(600);
		digitalWrite(STEP_PIN, LOW);
		delayMicroseconds(600);
	}
}