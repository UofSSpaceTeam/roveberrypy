#include <Wire.h>
#include <math.h>

// linear actuator control pins
#define null_pin 	0;

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
#define L1_MAX			899
#define L1_MIN			630

#define L2_MAX			950
#define L2_MIN			649

#define L3_MAX			1023
#define L3_MIN			5

// tolerances
#define L1_TOL			12
#define L2_TOL			12
#define L3_TOL			14

// inverse kin min and max positions
#define INVK_MAX_X 		0
#define INVK_MIN_X 		0
#define INVK_MAX_Z		0
#define INVK_MIN_Z		0
#define INVK_MAX_PHI		0
#define INVK_MIN_PHI		0

#define EXTEND  1
#define RETRACT 2
#define STILL   3

// actuator globals
int wiperPin[3] = {L1_WIPER, L2_WIPER, L3_WIPER};
int tolerance[3] = {L1_TOL, L2_TOL, L3_TOL};
int LA_MAX[3] = {L1_MAX, L2_MAX, L3_MAX};
int LA_MIN[3] = {L1_MIN, L2_MIN, L3_MIN};
double co0[] =  { 624.2, 626, -16.79};  
double co1[] =  { 2.391, 2.404, 16.35};
double co2[] = { 0, 0, -0.0303};

int apx_terms = 13;

struct drivePins {
    int pinA;
    int pinB;
    int pinPWM;
    int pinWiper;
    drivePins(int pinA_, int pinB_, int pinPWM_, int pinWiper_ ){
      pinA = pinA_;
      pinB = pinB_;
      pinPWM = pinPWM_;
      pinWiper = pinWiper_;
    }
    drivePins(int pinA_, int pinB_, int pinPWM_){
      pinA = pinA_;
      pinB = pinB_;
      pinPWM = pinPWM_;
      pinWiper = -1;
    }
    drivePins(int pinA_, int pinB_){
      pinA = pinA_;
      pinB = pinB_;
      pinPWM = -1;
      pinWiper = -1;
    }

    void set(int dir, int dutyCycle){
        switch(dir){
        case EXTEND:
          digitalWrite(pinA, LOW);
          digitalWrite(pinB, HIGH);
          if(pinPWM != -1)  analogWrite (pinPWM, dutyCycle);
          break;
        case RETRACT:
          digitalWrite(pinA, HIGH);
          digitalWrite(pinB, LOW );
          if(pinPWM != -1)  analogWrite (pinPWM, dutyCycle);
          break;
        case STILL:
          digitalWrite(pinA,0);
          digitalWrite(pinB,0);
          if(pinPWM != -1)  analogWrite (pinPWM,0);
          break;
        }
    }

    double readPosition(){
        if(pinWiper != -1){
            double   wiperReading[apx_terms];
            int   readingIndex[apx_terms];
            double  wiperValue = -1;
            
            for(int jdx = 0; jdx < apx_terms; jdx++){
              readingIndex[jdx] = 0;
              wiperReading[jdx] = analogRead(pinWiper);
              for(int kdx = 0; kdx < jdx; kdx++){
                if(wiperReading[kdx] == wiperReading[jdx])  wiperValue = wiperReading[jdx]; // take mode if there is one
                if(wiperReading[kdx] > wiperReading[jdx]) readingIndex[kdx]++;
                if(wiperReading[kdx] < wiperReading[jdx])   readingIndex[jdx]++;
              }
            }
            if(wiperValue != -1){ // otherwise take the median
              for(int jdx = 0; jdx < apx_terms; jdx++){
                if(readingIndex[jdx] == int(apx_terms/2)) wiperValue = wiperReading[jdx];
              }
            }
            return wiperValue;
        }
        return 0;
    }

    void initalize(){
      pinMode(pinA, OUTPUT);
      pinMode(pinB, OUTPUT);
      if(pinPWM != -1)    pinMode(pinPWM,   OUTPUT);
      if(pinWiper != -1)  pinMode(pinWiper, INPUT);
    }
};

drivePins linac1(L1_A, L1_B, L1_PWM, L1_WIPER);
drivePins linac2(L2_A, L2_B, L2_PWM, L2_WIPER);
drivePins linac3(L3_A, L3_B, L3_PWM, L3_WIPER);
drivePins gripper1(G1_A, G1_B, G1_PWM);
drivePins gripper2(G1_A, G1_B);

drivePins* LA[3] = {&linac1, &linac2, &linac3 };
drivePins* G[2] = {&gripper1, &gripper2};

int dutyCycle = 255;



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


void inverseKinematics(double r, double z, double phi){
  
	// constants
  double a0r = 30.34;
  double a0z = 95.25;
  double a1 = 335.95;
  double a2 = 397;
  
  double a1s = a1*a1;
  double a2s = a2*a2;
  double ar2 = (a0r+r)*(a0r+r);
  double az2 = (a0z-z)*(a0z-z);
  

  // intermediate calcs
  // L1
  double temp1  = atan2(a2*sqrt(1.0-(a1s+a2s-ar2-az2)*(a1s+a2s-ar2-az2)/(4.0*a1s*a2s)),(a1s-a2s+ar2+az2)/(2.0*a1));
  double temp2  = cos(2.24868+temp1-atan2(a0r+r,z-a0z));
  lengthLA[0]   = 259.948072*sqrt(1.9330354 - temp2) - 292.35;

  //L2
  lengthLA[1]   = 199.919984*sqrt(3.17794235 +(-a1s-a2s+ar2+az2)/(a1*a2)) - 292.35;

  //L3
  temp1 = acos((-a1s-a2s+ar2+az2)/(2*a1*a2));
  temp2 = atan2(a2*sqrt(1.0-(a1s+a2s-ar2-az2)*(a1s+a2s-ar2-az2)/(4*a1s*a2s)),(a1s-a2s+ar2+az2)/(2*a1));
  lengthLA[2] = 156.780100778*sqrt(2.2274206672 + cos(phi*0.01745329251+temp1-temp2+atan2(a0r+r,z-a0z))) - 170.5;
  
}
void setLAPosition(){
  // get distances
  double dist1 = abs((LA[0]->readPosition() - co0[0])/co1[0] - lengthLA[0]);
  double dist2 = abs((LA[1]->readPosition() + co0[1])/co1[1] - lengthLA[1]);
  
	
	for( int idx = 0; idx < 3; idx++ ){
		// get requested position
		double reqPos = lengthLA[idx];
		double digiPos = co2[idx]*reqPos*reqPos + co1[idx]* reqPos + co0[idx];
	  	
		// get currrent position
		double physPos = LA[idx]->readPosition();

		// determine direction to go
    int dir = 0;
		if 	( physPos == digiPos )	dir = STILL;
		else if	( physPos >  digiPos ) 	dir = RETRACT;
		else if ( physPos <  digiPos ) 	dir = EXTEND;

		// adjust digital position to account for tolerance
		switch(dir){
		case RETRACT:
			if( abs( digiPos - tolerance[idx]/2 - physPos ) < tolerance[idx]) 	dir = STILL;
			break;
		case EXTEND:
			if( abs( digiPos + tolerance[idx]/2 - physPos ) < tolerance[idx])	dir = STILL;
		}

		// check that linear actuator is safe to move
		// if it is safe to move then go ahead
		bool safeToMove = true;
		switch(dir){
		case EXTEND:
			safeToMove &= physPos < LA_MAX[idx];
			if(safeToMove) LA[idx]->set(EXTEND,dutyCycle);
			break;
		case RETRACT:
			safeToMove &= physPos > LA_MIN[idx];
			if(safeToMove) LA[idx]->set(RETRACT,dutyCycle);
			break;
		case STILL:
			LA[idx]->set(STILL,dutyCycle);
			break;
		}
	}
}

void manual(int la, int dir){
  LA[0]->set(RETRACT,255);
}

void setup()
{
	Serial.begin(9600);
  
  LA[0]->initalize();
  LA[1]->initalize();
  LA[2]->initalize();
  G[0] ->initalize();
  G[1] ->initalize();
}
int i = 2;
void loop(){
  inverseKinematics(450,350,0);
  setLAPosition();
}

