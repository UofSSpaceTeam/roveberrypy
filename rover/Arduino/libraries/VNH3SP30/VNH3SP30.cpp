#include "Arduino.h"
#include "VNH3SP30.h"

VNH3SP30::VNH3SP30(int A, int B, int PWM)
{
	motorA = A;
	motorB = B;
	motorPWM = PWM;
	pinMode(motorA, OUTPUT);
	pinMode(motorB, OUTPUT);
	pinMode(motorPWM, OUTPUT);
	digitalWrite(motorA, LOW);
	digitalWrite(motorB, LOW);
	digitalWrite(motorPWM, LOW);
	count = 0;
	direction = 0;
}

void VNH3SP30::set(int val)
{
	val = constrain(val, -255, 255);
	if(val == 0)
	{
		digitalWrite(motorA, LOW);
		digitalWrite(motorB, LOW);
		digitalWrite(motorPWM, LOW);
		direction = 0;
	}
	else if(val > 0)
	{
		digitalWrite(motorA, HIGH);
		digitalWrite(motorB, LOW);
		analogWrite(motorPWM, val);
		direction = 1;
	}
	else
	{
		digitalWrite(motorA, LOW);
		digitalWrite(motorB, HIGH);
		analogWrite(motorPWM, abs(val));
		direction = -1;
	}
}

void VNH3SP30::addToCount(int num)
{
	count += num;
}

int VNH3SP30::getCount()
{
	return count;
}

char VNH3SP30::getDirection()
{
	return direction;
}

