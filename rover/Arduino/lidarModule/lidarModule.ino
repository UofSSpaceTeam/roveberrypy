#include <I2C.h>
#define SENSOR_ADDRESS 0x62
#define TRIGGER_REG 0x00
#define TRIGGER_VALUE 0x04
#define RESULT_REG 0x8F
#define SIGNAL_REG 0x0E
#define MULT_ADDRESS 0x70
#define NUM_SENSORS 2
#define CW 1
#define CCW -1
#define EDGE_THRESH 7

int rotation = 0;
int stepsPerRotation;
int distance[NUM_SENSORS];
int signal[NUM_SENSORS];

void setup()
{
	Serial.begin(115200);
	delay(1000);
	I2c.begin();
	I2c.timeOut(50);
	calibrateStepper();
	while(!Serial); // wait for usb connection
}

void loop()
{
	for(int i = 0; i < NUM_SENSORS; i++)
	{
		setChannel(i);
		distance[i] = getDistance();
		signal[i] = getSignalStrength();
	}
	sendJson();
	rotate(CW, 1);
}

void calibrateStepper()
{
	int threshold = 7;
	int count;
	setChannel(0);
	spinToEdge(CW, RISING);
	stepsPerRotation = rotateUntracked(CW, 10);
	stepsPerRotation += spinToEdge(CW, RISING);
	count = rotateUntracked(CCW, 5);
	count += spinToEdge(CCW, RISING);
	rotateUntracked(CW, (count + stepsPerRotation) / 2);
	rotation = 0;
}

int rotate(int direction, unsigned int steps)
{
	rotateUntracked(direction, steps);
	rotation += steps;
	if(rotation < 0)
		rotation += stepsPerRotation;
	else if(rotation > stepsPerRotation)
		rotation -= stepsPerRotation;
	return int(steps);
}

int rotateUntracked(int direction, unsigned int steps)
{
	if(direction == CW)
	{
		
	}
	else if(direction == CCW)
	{
		
	}
	for(int i = 0; i < abs(steps); i++)
	{
		delay(10);
	}
	return int(steps);
}

int spinToEdge(int direction, int type)
{
	int steps = 0;
	if(type == RISING)
	{
		while(getDistance() > EDGE_THRESH)
			rotateUntracked(direction, 1);
		steps += rotateUntracked(direction, 2);
		while(getDistance() < EDGE_THRESH)
			steps += rotateUntracked(direction, 1);
	}
	else if(type == FALLING)
	{
		while(getDistance() < EDGE_THRESH)
			rotateUntracked(direction, 1);
		steps += rotateUntracked(direction, 2);
		while(getDistance() > EDGE_THRESH)
			steps += rotateUntracked(direction, 1);
	}
	return abs(steps);
}

void setChannel(byte channel)
{
	uint8_t reg = (0x04 | channel);
	uint8_t result = 1;
	while(result)
	{
		delay(1);
		result = I2c.write((uint8_t)MULT_ADDRESS, reg);
	}
}

int getDistance()
{
	writeSensorTrigger();
	return readSensorDistance();
}

int getSignalStrength()
{
	byte buf;
	uint8_t result = 1;
	while(result)
	{
		delay(1);
		result = I2c.read(SENSOR_ADDRESS, SIGNAL_REG, 1, &buf);
	}
	return int(buf);
}

void writeSensorTrigger()
{
	uint8_t result = 1;
	while(result)
	{
		delay(1);
		result = I2c.write(SENSOR_ADDRESS, TRIGGER_REG, TRIGGER_VALUE);
	}
}

int readSensorDistance()
{
	byte buf[2];
	uint8_t result = 1;
	while(result)
	{
		delay(1);
		result = I2c.read(SENSOR_ADDRESS, RESULT_REG, 2, buf);
	}
	return int(buf[0] << 8) + buf[1];
}

void sendJson()
{
	Serial.print("{\"rot\": \"");
	Serial.print(rotation);
	Serial.print("\", \"d1\": \"");
	Serial.print(distance[0]);
	Serial.print("\", \"s1\": \"");
	Serial.print(signal[0]);
	Serial.print("\", \"d2\": \"");
	Serial.print(distance[1]);
	Serial.print("\", \"s2\": \"");
	Serial.print(signal[1]);
	Serial.println("\"}");
}

