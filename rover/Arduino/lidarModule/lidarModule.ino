#include <I2C.h>
#define SENSOR_ADDRESS 0x62
#define TRIGGER_REG 0x00
#define TRIGGER_VALUE 0x04
#define RESULT_REG 0x8F
#define SIGNAL_REG 0x0E
#define MULT_ADDRESS 0x70
#define DISTANCE_THRESH 5
#define DIR_PIN 10
#define STEP_PIN 16
#define MS1_PIN 14
#define MS2_PIN 9

byte frequency = 255;
volatile int count = 1;

void setup()
{
	Serial.begin(57600);
	delay(1000);
	Serial.println("start");
	I2c.begin();
	I2c.timeOut(50);
	pinMode(DIR_PIN, OUTPUT);
	pinMode(STEP_PIN, OUTPUT);
	pinMode(MS1_PIN, OUTPUT);
	pinMode(MS2_PIN, OUTPUT);
	digitalWrite(MS1_PIN, LOW);
	digitalWrite(MS2_PIN, LOW);
	digitalWrite(STEP_PIN, LOW);
	digitalWrite(DIR_PIN, LOW);
	attachInterrupt(4, switchHit, RISING);
}

void loop()
{
	noTone(STEP_PIN);
	Serial.print("<");
	Serial.print(readTopSensor());
	Serial.print(",");
	Serial.print(readBottomSensor());
	Serial.print(",");
	Serial.print(count);
	Serial.println(">");
	count++;
	if(Serial.available())
	{
		frequency = Serial.read();
		if(frequency < 32)
			frequency = 32;
		Serial.print("speed = ");
		Serial.println((int)frequency);
		Serial.flush();
	}
	tone(STEP_PIN, frequency);
	delay(500);
}

void step()
{
	digitalWrite(STEP_PIN, HIGH);
	delay(2);
	digitalWrite(STEP_PIN, LOW);
	delay(2);
}

int readTopSensor()
{
	setChannel(1);
	return getDistance();
}

int readBottomSensor()
{
	setChannel(0);
	return getDistance();
}

void setChannel(byte channel)
{
	uint8_t reg = (0x04 | channel);
	uint8_t result = 1;
	while(result)
	{
		result = I2c.write((uint8_t)MULT_ADDRESS, reg);
		delay(1);
	}
}

int getDistance()
{
	int distance = 0;
	byte buf[2];
	for(int i = 0; i < 5; i++)
	{
		uint8_t result = 1;
		while(result)
		{
			result = I2c.write(SENSOR_ADDRESS, TRIGGER_REG, TRIGGER_VALUE);
			delay(1);
		}
		result = 1;
		while(result)
		{
			result = I2c.read(SENSOR_ADDRESS, RESULT_REG, 2, buf);
			delay(1);
		}
		distance = int(buf[0] << 8) + buf[1];
		if(distance > 0)
			break;
	}
	return distance;
}

void switchHit()
{
	count = 0;
}

