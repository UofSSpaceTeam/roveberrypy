#include <Wire.h>
#include <math.h>

// linear actuator control pins
#define L1_A		17
#define L1_B		16
#define L1_PWM		10
#define L1_WIPER	A8

#define L2_A		15
#define L2_B		14
#define L2_PWM		9
#define L2_WIPER	A7

#define L3_A		13
#define L3_B		12
#define L3_PWM		6
#define L3_WIPER	A6

#define BASE_A		11
#define BASE_B		8
#define BASE_PWM	5

#define G1_A		7
#define G1_B		2
#define G1_PWM		4

#define G2_A		1
#define G2_B		3

// linear actuator min and max positions
#define L1_MAX			885
#define L1_MIN			591

#define L2_MAX			862
#define L2_MIN			617

#define L3_MAX			810
#define L3_MIN			260

// tolerances
#define L1_TOL			10
#define L2_TOL			10
#define L3_TOL			10

// inverse kin min and max positions
#define INVK_MAX_X 		0
#define INVK_MIN_X 		0
#define INVK_MAX_Z		0
#deinfe INVK_MIN_Z		0
#define INVK_MAX_PHI	0
#deinfe INVK_MIN_PHI	0

enum DIRECTION {	EXTEND,		RETRACT, 	STILL		};

double dutyCycle = 255;

int L1[3] = {L1_A, L1_B, L1_PWM};
int L2[3] = {L2_A, L2_B, L2_PWM};
int L3[3] = {L3_A, L3_B, L3_PWM};
int* LA[3] = {&L1, &L2, &L3};

// actuator globals
int wiperPin[3] = {L1_WIPER, L2_WIPER, L3_WIPER};
int tolerance[3] = {L1_TOL, L2_TOL, L3_TOL};
int LA_MAX[3] = {L1_MAX, L2_MAX, L3_MAX};
int LA_MIN[3] = {L1_MIN, L2_MIN, L3_MIN};
double co0[] = {602.7172151459694, 609.5148521804905, -9.5409};
double co1[] = {2.6706077615978, 2.4617644953818, 6.5606};
double co2[] = {-0.0046229045464, 0.0004252476161, 0.041};
double co3[] = {0.0000267147227, -0.0000047310008, -0.0001};
int pphr = 13390;

// inverse kin stuff
float minOutput[3] = {0.0, 9.0, 33.0};
float maxOutput[3] = {109.0, 104.0, 100.0};
float countsPerDegree = 74.39;

double lengthLA[3];


void setPosition();

void setLAPosition();
void inverseKinematics();
void setLA(int, int);

void setLA(int la, DIRECTION dir, int dutyCycle){
	int pin[3];
	switch(la){
	case 0:
		pin[0] = L1_A;
		pin[1] = L1_B;
		pin[2] = L1_PWM;
		break;
	case 1:
		pin[0] = L2_A;
		pin[1] = L2_B;
		pin[2] = L2_PWM;
		break;
	case 2:
		pin[0] = L3_A;
		pin[1] = L3_B;
		pin[2] = L3_PWM;
		break;
	}
	
	switch(dir){
	case EXTEND:
		digitalWrite(pin[0], HIGH);
		digitalWrite(pin[1], LOW );
		analogWrite (pin[2], dutyCycle);
		break;
	case RETRACT:
		digitalWrite(pin[0], LOW);
		digitalWrite(pin[1], HIGH );
		analogWrite (pin[2], dutyCycle);
		break;
	case STILL:
		digitalWrite(pin[0],0);
		digitalWrite(pin[1],0);
		analogWrite (pin[2],0);
		break;
	}
}
void inverseKinematics(){
	lengthLA[0] = 80;
	lengthLA[1] = 60;
	lengthLA[2] = 70;
}
void setLAPosition(){
	
	for( int idx = 0; idx < 3; idx++ ){
		double length = lengthLA[idx];
		double pwmLength = co3[i]*x*x*x+ co2[i]*x*x+ co1[i]*x+ co0[i];
		
		double 	wiperReading[5];
		int 	readingIndex[5];
		double 	wiperValue = -1;
		
		for(int jdx = 0; jdx < 5; jdx++){
			readingIndex[jdx] = 0;
			wiperReading[jdx] = analogRead(wiper[idx]);
			for(int kdx = 0; kdx < jdx; kdx++){
				if(wiperReading[kdx] == wiperReading[jdx]) 	wiperValue = wiperReading[jdx];	// take mode if there is one
				if(wiperReading[kdx] > wiperReading[jdx])	readingIndex[kdx]++;
				if(wiperReading[kdx] < wiperReading[jdx]) 	readingIndex[jdx]++;
			}
		}
		if(wiperValue != -1){	// otherwise take the median
			for(int jdx = 0; jdx < 4; jdx++){
				if(readingIndex[jdx] == 2) wiperValue = wiperReading[jdx];
			}
		}
		
		double currReading = wiperValue;
		DIRECTION dir;
		if(pwmLength - currReading > 0) 		dir = EXTEND;
		else if(pwmLength - currReading == 0) 	dir = STILL
		else 									dir = RETRACT;
		
		pwmLength += dir*tolerance[i]/2; 
		if(abs(currentReading - pwmLength) > tolerance[idx]) dir = STILL;
		
		bool safeToMove = true;
		switch(dir){
		case EXTEND:
			safeToMove &= currReading < LA_MAX[idx];
			if(safeToMove) setLAPosition(idx,EXTEND, dutyCycle);
			break;
		case RETRACT:
			safeToMove &= currReading > LA_MIN[idx];
			if(safeToMove) setLAPosition(idx,RETRACT,dutyCycle);
			break;
		case STILL:
			setLAPosition(idx,STILL, 0);
			break;
		}
	}
}

void setup()
{
	Serial.begin(9600);
	LA[0].set(0);
	LA[1].set(0);
	LA[2].set(0);
	timer = millis();
}
