#include <Wire.h>
#include <math.h>
#include <VNH3SP30.h>
#include <MC33926.h>

#define TIMEOUT 750
#define CMD_HEADER 0xF7
#define CMD_TRAILER 0xF8
#define I2C_ADDRESS 0x08

#define L1A 0
#define L1B 1
#define L1PWM 3
#define L1WIPER A2
#define L2A 2 
#define L2B 7 
#define L2PWM 4
#define L2WIPER A1
#define L3A 8
#define L3B 11
#define L3PWM 5
#define L3WIPER A0
#define BASEA 12
#define BASEB 13
#define BASEPWM 6
#define BASEINT1 20
#define BASEINT2 21
#define HANDSPINA 22
#define HANDSPINB 23
#define HANDOPENA 9
#define HANDOPENB 10

#define L1MAX 870
#define L1MIN 591
#define L1TOLERANCE 10
#define L2MAX 862
#define L2MIN 617
#define L2TOLERANCE 10
#define L3MAX 832
#define L3MIN 412
#define L3TOLERANCE 10
#define BASETOLERANCE 100

#define MAX_X 793.5
#define MIN_X -793.5
#define MAX_Y 793.5
#define MIN_Y -793.5
#define MAX_Z 800
#define MIN_Z -239
#define MAX_PHI 45
#define MIN_PHI -45

enum command_type
{
	SET_SPEEDS,
	SET_POSITION
};

typedef struct
{
	byte header;
	byte type;
	short d1;
	short d2;
	short d3;
	short d4;
	short d5;
	short d6;
	short d7;
	byte csum;
	byte trailer;
} command;

VNH3SP30 base = VNH3SP30(BASEA, BASEB, BASEPWM);
VNH3SP30 LA[3] = {VNH3SP30(L1A, L1B, L1PWM),
				VNH3SP30(L2A, L2B, L2PWM),
				VNH3SP30(L3A, L3B, L3PWM)};
MC33926 handSpin = MC33926(HANDSPINA, HANDSPINB);
MC33926 handOpen = MC33926(HANDOPENA, HANDOPENB);

unsigned long timer;
volatile command cmd;
byte* cmdPointer = (byte*)(&cmd);
volatile byte cmdCount = 0;
volatile bool newCommand = false;

// movement commanding
int position[4] = {400, 0, 200, -60}; // x, y, z, phi
int speed[4] = {0, 0, 0, 0}; // base, L1, L2, L3
int spin, open;
int throttle = 128; // 0 - 255

// actuator config
int wiperPin[3] = {L1WIPER, L2WIPER, L3WIPER};
int tolerance[3] = {L1TOLERANCE, L2TOLERANCE, L3TOLERANCE};
double co0[] = {602.7172151459694, 609.5148521804905, -9.5409};
double co1[] = {2.6706077615978, 2.4617644953818, 6.5606};
double co2[] = {-0.0046229045464, 0.0004252476161, 0.041};
double co3[] = {0.0000267147227, -0.0000047310008, -0.0001};

// inverse kin stuff
float kinOutputBase; // degrees
float kinOutput[3];
float minOutput[3] = {0.0, 9.0, 33.0};
float maxOutput[3] = {109.0, 104.0, 100.0};
float countsPerDegree = 74.39;

// prototypes
void receiveEvent(int count); // incoming I2C byte
void processCommand();
void setSpeeds();
void setPosition();
void setGripper();
void doInverseKinematics();
int averageReading(int pin, int num);
void baseInterrupt();
int getNewLength(int index, double target);
int getNewCount(float angle);
void printCommand();

void setup()
{
	Serial.begin(9600);
	Wire.begin(I2C_ADDRESS);
	Wire.onReceive(receiveEvent);
	attachInterrupt(BASEINT1, baseInterrupt, RISING);
	base.set(0);
	LA[0].set(0);
	LA[1].set(0);
	LA[2].set(0);
	timer = millis();
}

void loop()
{
	if(newCommand)
		processCommand();
	else if(millis() - timer > TIMEOUT)
	{
		for(int i = 0; i < 4; i++)
			speed[i] = 0;
		spin = 0;
		open = 0;
		setSpeeds();
		setGripper();
		Serial.println("TO");
		timer = millis();
	}
}

void processCommand()
{
	switch(cmd.type)
	{
		case SET_SPEEDS:
		speed[3] = cmd.d1; // base
		speed[0] = cmd.d2; // LA1
		speed[1] = cmd.d3; // LA2
		speed[2] = cmd.d4; // LA3
		spin = constrain(cmd.d5, -255, 255);
		open = constrain(cmd.d6, -255, 255);
		throttle = constrain(cmd.d7, 0, 255);
		printCommand();
		setSpeeds();
		setGripper();
		timer = millis();
		break;

		case SET_POSITION:
		position[0] = map(cmd.d1, -1000, 1000, MIN_X, MAX_X);
		position[1] = map(cmd.d2, -1000, 1000, MIN_Y, MAX_Y);
		position[2] = map(cmd.d3, -1000, 1000, MIN_Z, MAX_Z);
		position[3] = map(cmd.d4, -1000, 1000, MIN_PHI, MAX_PHI);
		spin = constrain(cmd.d5, -255, 255);
		open = constrain(cmd.d6, -255, 255);
		throttle = constrain(cmd.d7, 0, 255);
		doInverseKinematics();
		setPosition();
		setGripper();
		timer = millis();
		break;
	}
	newCommand = false;
}

void printCommand()
{
	char buf[32];
	if(cmd.type == SET_SPEEDS)
		Serial.print("Speeds: ");
	else if(cmd.type == SET_POSITION)
		Serial.print("Position: ");
	sprintf(buf, "(%i, %i, %i, %i, %i, %i, %i)", \
		cmd.d1, cmd.d2, cmd.d3, cmd.d4, cmd.d5, cmd.d6, cmd.d7);
	Serial.println(buf);
}

void setPosition() // blocking until move is done
{
	int newLength[3];
	int length, newCount, count;
	for(int i = 0; i < 3; i++)
	{
		newLength[i] = getNewLength(i, kinOutput[i]);
		length = averageReading(wiperPin[i], 5);
		if(abs(newLength[i] - length) > tolerance[i])
		{
			if(newLength[i] > length)
				LA[i].set(throttle);
			else
				LA[i].set(-throttle);
		}
	}
	
	newCount = getNewCount(kinOutputBase);
	count = base.getCount();
	if(abs(newCount - count) > BASETOLERANCE)
	{
		if(newCount > count)
			base.set(throttle);
		else
			base.set(-throttle);
	}
	
	boolean done[3] = {false, false, false};
	boolean baseDone = false;
	char direction;
	while(!done[0] || !done[1] || !done[2] || !baseDone)
	{
		for(int i = 0; i < 3; i++)
		{
			if(!done[i])
			{
				length = averageReading(wiperPin[i], 10);
				direction = LA[i].getDirection();
				if((direction > 0 && length > newLength[i]) \
					|| (direction < 0 && length < newLength[i]))
				{
					LA[i].set(0);
					done[i] = true;
				}
			}
		}
		if(!baseDone)
		{
			baseDone = true;
			count = base.getCount();
			direction = base.getDirection();
			if((direction > 0 && count > newCount) \
				|| (direction < 0 && count < newCount))
			{
				base.set(0);
				baseDone = true;
			}
		}
	}
}

int getNewLength(int index, double target)
{
	return int((co3[index] * pow(target, 3)) + (co2[index] * pow(target,2)) + \
		(co1[index] * target) + (co0[index]));
}

int getNewCount(float angle)
{
	return int(angle * countsPerDegree);
}

void setSpeeds()
{
	int length;
	for(int i = 0; i < 3; i++)
	{
		// length = averageReading(wiperPin[i], 10);
		// if((length < L1MAX && length > L1MIN) || \
			// (length > L1MAX && speed[0] < 0) || \
			// (length < L1MIN && speed[0] > 0))
			LA[i].set(speed[i]);
	// else
		// LA[i].set(0);
	}
	base.set(speed[3]);
}

int averageReading(int pin, int num)
{
	unsigned long result = 0;
	for(int i = 0; i < num; i++)
		result += analogRead(pin);
	return int(result / num);
}

void setGripper()
{
	handSpin.set(spin);
	handOpen.set(open);
}

void doInverseKinematics()
{
	float x = position[0];
	float y = position[1];
	float z = position[2];
	float phi = position[3];
	float a0x = 30.34;
	float a0z = 95.25;
	float a1 = 335.95;
	float a2 = 393;

	float t = hypot(x + a0x, y);
	float p = z - a0z;
	float c3 = (pow(t, 2) + pow(p, 2) - pow(a1, 2) - pow(a2, 2)) / (2 * a1 * a2);
	float g3 = acos(c3);
	float K1 = a1 + (a2 * cos(g3));
	float K2 = a2 * sin(g3);
	float g2 = atan2(p, t) - atan2(K1, K2);

	float T2 = 90.0 - (g2 * 180.0 / PI);
	float T3 = 180.0 - (g3 * 180.0 / PI);
	float T4 = 180.0 + phi - T3 - T2;

	// L1
	kinOutput[0] = sqrt(130621.0-67573.0*cos((T2+38.84)*PI/180)) - 292.35;
	kinOutput[0] = constrain(kinOutput[0], minOutput[0], maxOutput[0]);

	// L2
	kinOutput[1] = sqrt(118487.0-50392.0*cos(T3*PI/180.0)) - 292.35;
	kinOutput[1] = constrain(kinOutput[1], minOutput[1], maxOutput[1]);

	// L3
	kinOutput[2] = sqrt(54750.0-24580.0*cos(PI/2.0-T4*PI/180.0)) - 167.5;
	kinOutput[2] = constrain(kinOutput[2], minOutput[2], minOutput[2]);
	
	// Base
	kinOutputBase = atan2(y, x) * (180.0 / PI);
}

void baseInterrupt()
{
	if(digitalRead(BASEINT2) == HIGH)
		base.addToCount(1);
	else
		base.addToCount(-1);
}

void receiveEvent(int count)
{
	if(newCommand)
		return;
	while(Wire.available())
	{
		byte in = Wire.read();
		
		if(cmdCount == 0) // wait for header
		{
			if(in == CMD_HEADER)
			{
				cmdPointer[cmdCount] = in;
				cmdCount++;
			}
			continue;
		}
		if(cmdCount < sizeof(command)) // add middle bytes
		{
			cmdPointer[cmdCount] = in;
			cmdCount++;
		}
		if(cmdCount == sizeof(command)) // check for complete
		{
			if(in == CMD_TRAILER)
			{
				byte csum = cmd.type + cmd.d1 + cmd.d2 + cmd.d3 + cmd.d4 \
					+ cmd.d5 + cmd.d6 + cmd.d7;
				if(csum == cmd.csum)
					newCommand = true;
			}
			cmdCount = 0;
		}
	}
}


