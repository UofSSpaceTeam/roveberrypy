#include <I2C.h>
#define SENSOR_ADDRESS 0x62
#define TRIGGER_REG 0x00
#define TRIGGER_VALUE 0x04
#define RESULT_REG 0x8F
#define SIGNAL_REG 0x0E
#define MULT_ADDRESS 0x70
#define DISTANCE_THRESH 5
#define DIR_PIN 99
#define STEP_PIN 99
#define MS1_PIN 99
#define MS2_PIN 99

int stepsPerReading = 100;

void setup()
{
	Serial.begin(57600);
	delay(1000);
	I2c.begin();
	I2c.timeOut(50);
	pinMode(DIR_PIN, OUTPUT);
	pinMode(STEP_PIN, OUTPUT);
	pinMode(MS1_PIN, OUTPUT);
	pinMode(MS2_PIN, OUTPUT);
	digitalWrite(MS1_PIN, LOW);
	digitalWrite(MS2_PIN, HIGH); // 1/4 step
	digitalWrite(STEP_PIN, LOW);
	digitalWrite(DIR_PIN, LOW);
	goHome();
}

void loop()
{
	readCommand();
	digitalWrite(DIR_PIN, LOW);
	scan();
	readCommand();
	digitalWrite(DIR_PIN, HIGH);
	scan();
}

void goHome()
{
	digitalWrite(DIR_PIN, LOW);
	while(readTopSensor() > DISTANCE_THRESH)
		for(int i = 0; i < 20; i++)
			step();
	digitalWrite(DIR_PIN, HIGH);
	while(readTopSensor() < DISTANCE_THRESH)
		for(int i = 0; i < 5; i++)
			step();
}

void step()
{
	digitalWrite(STEP_PIN, HIGH);
	delay(1);
	digitalWrite(STEP_PIN, LOW);
	delay(1);
}

void scan()
{
	int topDistance = 0;
	int count = 0;
	while(topDistance > DISTANCE_THRESH || count < 5)
	{
		topDistance = readTopSensor();
		Serial.print("<lidarDataTop:");
		Serial.print(topDistance);
		Serial.print("><lidarDataBottom:");
		Serial.print(readBottomSensor());
		Serial.println(">");
		count++;
		for(int i = 0; i < stepsPerReading; i++)
			step();
	}
	Serial.print("count = ");
	Serial.println(count);
}

int readTopSensor()
{
	setChannel(0);
	return getDistance();
}

int readBottomSensor()
{
	setChannel(1);
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
		while(result)
		{
			result = I2c.read(SENSOR_ADDRESS, RESULT_REG, 2, buf);
			delay(1);
		}
		distance = int(buf[0] << 8) + buf[1];
		if(distance)
			break;
	}
	return distance;
}

void readCommand()
{
	char buf[64];
	byte i = 0;
	unsigned long start = millis();
	while(Serial.available())
	{
		buf[0] = Serial.read();
		if(buf[0] == '<')
			while(millis() - start > 500)
				if(Serial.available())
				{
					buf[++i] = Serial.read();
					if(buf[i] == '>')
					{
						buf[i+1] = '\0';
						parseCommand(buf);
						return;
					}
					else if(i > 62)
						return;
				}
	}
}

void parseCommand(char* cmd)
{
	Serial.println(cmd);
	byte length = strcspn(cmd, ":");
	Serial.println(length);
	if(!strncmp("scanRate", cmd, length))
		stepsPerReading = 10 * atoi(cmd + length);
}		
		
		