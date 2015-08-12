#include <Wire.h>
#include <math.h>



// linear actuator control pins
#define null_pin 	0;

#define L1_A		17
#define L1_B		16
#define L1_PWM		10
#define L1_WIPER	A8
#define L1_C2 		0
#define L1_C1 		2.391
#define L1_C0 		624.2

#define L2_A		15
#define L2_B		14
#define L2_PWM		9
#define L2_WIPER	A7
#define L2_C2 		0
#define L2_C1 		2.404
#define L2_C0 		626

#define L3_A		13
#define L3_B		12
#define L3_PWM		6
#define L3_WIPER	A6
#define L3_C2 		-0.303
#define L3_C1 		16.35
#define L3_C0 		-16.79

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



#define EXTEND			1
#define RETRACT 		2

#define ON 				1
#define OFF 			0

#define POSITION  10
#define DIRECT    11
#define NUDGE     12

// -------------------------- I2C communication -------------------------------------
#define TIMEOUT 750
#define CMD_HEADER 0xF7
#define CMD_TRAILER 0xF8
#define I2C_ADDRESS 0x08

unsigned long timer;
volatile command cmd;
byte* cmdPointer = (byte*)(&cmd);
volatile byte cmdCount = 0;
volatile bool newCommand = false;

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

void processCommand()
{
	switch(cmd.type)
	{
		case SET_SPEEDS:
		speed[3] = cmd.d1; // base
		speed[0] = cmd.d2; // LA1
		speed[1] = cmd.d3; // LA2
		speed[2] = cmd.d4; // LA3
		gspin = constrain(cmd.d5, -191, 191);
		gopen = constrain(cmd.d6, -255, 255);
		throttle = constrain(cmd.d7, 0, 255);
		//printCommand();
		setSpeeds();
		setGripper();
		timer = millis();
		break;

		case SET_POSITION:
		/*position[0] = map(cmd.d1, -1000, 1000, MIN_X, MAX_X);
		position[1] = map(cmd.d2, -1000, 1000, MIN_Y, MAX_Y);
		position[2] = map(cmd.d3, -1000, 1000, MIN_Z, MAX_Z);
		position[3] = map(cmd.d4, -1000, 1000, MIN_PHI, MAX_PHI);*/
		position[0] = cmd.d1;
		position[1] = cmd.d2;
		position[2] = cmd.d3;
		position[3] = cmd.d4;
		gspin = constrain(cmd.d5, -191, 191);//9 volts maximum
		gopen = constrain(cmd.d6, -255, 255);
		throttle = constrain(cmd.d7, 0, 255);
        //printCommand();
		doInverseKinematics();
		setPosition();
		setGripper();
		timer = millis();
		break;
	}
	newCommand = false;
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
				byte csum = cmd.type + cmd.d1 + cmd.d2 + cmd.d3 + cmd.d4
					+ cmd.d5 + cmd.d6 + cmd.d7;
				if(csum == cmd.csum) {
                                        //Serial.println("csum");
					newCommand = true;
                                } 
			}
			cmdCount = 0;
		}
	}
}

// -------------------------------- End I2C communication -------------------------------


// ---------------------------- VNH5019 MOTOR DRIVER CLASS ------------------------------
class VNH5019 {
  private:
    int pinA;
    int pinB;
    int pinPWM;
    int pinWIPER;

    int MAX_DR;
    int MIN_DR;

    double calibration_coeff[3];

    int DIRECTION;
    int avgTravel;
  public:
    VNH5019(int pinA_, int pinB_, int pinPWM_, int pinWIPER_);
    VNH5019(int pinA_, int pinB_, int pinPWM_);
    VNH5019(int pinA_, int pinB_);

    void	setMAX_DR(int max_dr);
    void	setMIN_DR(int min_dr);
    void	setCalibration(double c2, double c1, double c0);

    void	turn(int ON_OFF, int dir, int dutyCycle);
    void	turn(int ON_OFF, int dir);
    void	turn(int ON_OFF);
    void  setPWM(int dutyCycle);

    int 	readPosition();
    void	initalizePins();
    bool	isSafe();

    void 	setDirection(int dir);
    int 	convertPhysDR(double phys);
    double convertDRPhys(int dr);

    int getDirection();


};

VNH5019::VNH5019(int pinA_, int pinB_, int pinPWM_, int pinWIPER_) { // constructor
  pinA 		= pinA_;
  pinB 		= pinB_;
  pinPWM 		= pinPWM_;
  pinWIPER 	= pinWIPER_;
  DIRECTION = 0;

  avgTravel = 0;
  calibration_coeff[2] = 0;
  calibration_coeff[1] = 0;
  calibration_coeff[0] = 0;
}


VNH5019::VNH5019(int pinA_, int pinB_, int pinPWM_) { // constructor
  pinA 		= pinA_;
  pinB 		= pinB_;
  pinPWM 		= pinPWM_;
  pinWIPER 	= -1;
  DIRECTION = 0;
  avgTravel = 0;
  calibration_coeff[2] = 0;
  calibration_coeff[1] = 0;
  calibration_coeff[0] = 0;

}


VNH5019::VNH5019(int pinA_, int pinB_) { // constructor
  pinA 		= pinA_;
  pinB 		= pinB_;
  pinPWM 		= -1;
  pinWIPER 	= -1;
  DIRECTION = 0;
  avgTravel = 0;
  calibration_coeff[2] = 0;
  calibration_coeff[1] = 0;
  calibration_coeff[0] = 0;
}

void VNH5019::setMAX_DR(int max_dr) { // set maximum digital read position
  MAX_DR = max_dr;
}

void VNH5019::setMIN_DR(int min_dr) { // set minumum digital read position
  MIN_DR = min_dr;
}
void VNH5019::setCalibration(double c2, double c1, double c0) {	// set calibration coeffs
  calibration_coeff[2] = c2;
  calibration_coeff[1] = c1;
  calibration_coeff[0] = c0;
}
void VNH5019::turn(int ON_OFF, int dir, int dutyCycle) { // turn la on/off
  DIRECTION = dir;
  if (ON_OFF == ON) {
    switch (dir) {
      case EXTEND:
        digitalWrite(pinA, LOW);
        digitalWrite(pinB, HIGH);
        if (pinPWM != -1) analogWrite(pinPWM, dutyCycle);
        break;
      case RETRACT:
        digitalWrite(pinA, HIGH);
        digitalWrite(pinB, LOW);
        if (pinPWM  != -1) analogWrite(pinPWM, dutyCycle);
        break;
    }
  } else if (ON_OFF == OFF) {
    digitalWrite(pinA, LOW);
    digitalWrite(pinB, LOW);
    if (pinPWM != -1) analogWrite(pinPWM, 0);
  }
}




void VNH5019::turn(int ON_OFF, int dir) { // turn la on/off
  DIRECTION = dir;
  if (ON_OFF == ON) {
    switch (dir) {
      case EXTEND:
        digitalWrite(pinA, LOW);
        digitalWrite(pinB, HIGH);
        if (pinPWM != -1) analogWrite(pinPWM, 255);
        break;
      case RETRACT:
        digitalWrite(pinA, HIGH);
        digitalWrite(pinB, LOW);
        if (pinPWM  != -1) analogWrite(pinPWM, 255);
        break;
    }
  } else if (ON_OFF == OFF) {
    digitalWrite(pinA, LOW);
    digitalWrite(pinB, LOW);
    if (pinPWM != -1) analogWrite(pinPWM, 0);
  }
}


void VNH5019::turn(int ON_OFF) { // turn la off
  if (ON_OFF == ON && DIRECTION != 0) {
    turn(ON, DIRECTION);
  } else {
    digitalWrite(pinA, LOW);
    digitalWrite(pinB, LOW);
    if (pinPWM != -1) analogWrite(pinPWM, 0);
  }
}
#define apx_term2 4
#define apx_terms 13
int VNH5019::readPosition() {		// get digital position of the la
  if (pinWIPER != -1) {
    int reading[apx_term2];
    int ocCount[apx_term2];
    for (int take = 0; take < apx_term2; take++) {
      int       wiperReading[apx_terms];
      int       readingIndex[apx_terms];
      double    wiperValue = -1;

      for (int jdx = 0; jdx < apx_terms; jdx++) {
        readingIndex[jdx] = 0;
        wiperReading[jdx] = analogRead(pinWIPER);
        for (int kdx = 0; kdx < jdx; kdx++) {
          if (wiperReading[kdx] == wiperReading[jdx])
            wiperValue = wiperReading[jdx];
          if (wiperReading[kdx] > wiperReading[jdx])
            readingIndex[kdx]++;
          if (wiperReading[kdx] < wiperReading[jdx])
            readingIndex[jdx]++;
        }
      }
      if (wiperValue != -1) { // otherwise take the median
        for (int jdx = 0; jdx < apx_terms; jdx++) {
          if (readingIndex[jdx] == int(apx_terms / 2))
            wiperValue = wiperReading[jdx];
        }
      }
      reading[take] = wiperValue;
    }
    int mostCommon = reading[0];
    int count = 1;
    // get mode
    for(int idx = 0; idx < apx_term2; idx++){
      int currCount = 1;
      for(int jdx = 0; jdx < apx_term2; jdx++){
        if(idx != jdx) if(reading[idx] == reading[jdx]) currCount++;
      }
      if(currCount > count) mostCommon = reading[idx];      
    }
    return mostCommon;
  }
  return 0;
}

void VNH5019::initalizePins() {	// initalize the pins
  pinMode(pinA, OUTPUT);
  pinMode(pinB, OUTPUT);
  if (pinPWM != -1)	pinMode(pinPWM, OUTPUT);
  if (pinWIPER != -1) 	pinMode(pinWIPER, INPUT);
}

bool VNH5019::isSafe() {		// check that the position is safe
  bool safe = true;
  switch (DIRECTION) {
    case EXTEND:
      safe &= readPosition() < MAX_DR;
      break;
    case RETRACT:
      safe &= readPosition() > MIN_DR;
      break;
  }
  if (!safe) {
    turn(OFF);
  }
  return safe;
}

void VNH5019::setDirection(int dir) { // set the direction
  DIRECTION = dir;
  if (dir == 0) turn(OFF);
}

int VNH5019::convertPhysDR(double phys) { // get the digital read for a position in mm
  return calibration_coeff[2] * phys * phys + calibration_coeff[1] * phys + calibration_coeff[0] + 0.5;
}

int VNH5019::getDirection() {
  return DIRECTION;
}

double VNH5019::convertDRPhys(int dr) {
  if (calibration_coeff[2] == 0) {
    return (dr - calibration_coeff[0]) / calibration_coeff[1];
  } else {
    return (-calibration_coeff[1] + sqrt(calibration_coeff[1] * calibration_coeff[1] - 4 * calibration_coeff[2] * (calibration_coeff[0] - dr))) / (2 * calibration_coeff[2]);
  }
}

void VNH5019::setPWM(int dutyCycle){
  if(pinPWM != -1) analogWrite(pinPWM,dutyCycle);
}

// ------------------------ END OF VNH5019 CLASS ------------------------------

VNH5019 L1(L1_A, L1_B, L1_PWM, L1_WIPER);
VNH5019 L2(L2_A, L2_B, L2_PWM, L2_WIPER);
VNH5019 L3(L3_A, L3_B, L3_PWM, L3_WIPER);
VNH5019 G1(G1_A, G1_B, G1_PWM);
VNH5019 G2(G1_A, G1_B);

VNH5019* la[3] = {&L1, &L2, &L3};
VNH5019* gr[3] = {&G1, &G2};

bool newCommand() {
  // return true if new command has been given
  return newCommad;
}

void invKinCommand(double r, double z, double phi) {

  // constants
  double a0r = 30.34;
  double a0z = 95.25;
  double a1 = 335.95;
  double a2 = 397;

  double a1s = a1 * a1;
  double a2s = a2 * a2;
  double ar2 = (a0r + r) * (a0r + r);
  double az2 = (a0z - z) * (a0z - z);

  double lengthLA[3];

  // intermediate calcs
  // L1
  double temp1  = atan2(a2 * sqrt(1.0 - (a1s + a2s - ar2 - az2) * (a1s + a2s - ar2 - az2) / (4.0 * a1s * a2s)), (a1s - a2s + ar2 + az2) / (2.0 * a1));
  double temp2  = cos(2.24868 + temp1 - atan2(a0r + r, z - a0z));
  lengthLA[0]   = 259.948072 * sqrt(1.9330354 - temp2) - 292.35;

  //L2
  lengthLA[1]   = 199.919984 * sqrt(3.17794235 + (-a1s - a2s + ar2 + az2) / (a1 * a2)) - 292.35;

  //L3
  temp1 = acos((-a1s - a2s + ar2 + az2) / (2 * a1 * a2));
  temp2 = atan2(a2 * sqrt(1.0 - (a1s + a2s - ar2 - az2) * (a1s + a2s - ar2 - az2) / (4 * a1s * a2s)), (a1s - a2s + ar2 + az2) / (2 * a1));
  lengthLA[2] = 156.780100778 * sqrt(2.2274206672 + cos(phi * 0.01745329251 + temp1 - temp2 + atan2(a0r + r, z - a0z))) - 170.5;
  int drLength[3];
  int numberAtDestination = 0;

  Serial.print("Setting L1 to ");
  Serial.println(lengthLA[0]);
  Serial.print("Setting L2 to ");
  Serial.println(lengthLA[1]);
  Serial.print("Setting L3 to ");
  Serial.println(lengthLA[2]);

  // turn on the LA's
  for (int idx = 0; idx < 3; idx++) {
    drLength[idx] = la[idx]->convertPhysDR(lengthLA[idx]); // get dr of final position
    int dr = la[idx]->readPosition(); // read position
    // set direction
    if (dr > drLength[idx]) {
      la[idx]->setDirection(RETRACT);
      if (la[idx]->isSafe()) la[idx]->turn(ON);
    }
    if (dr < drLength[idx]) {
      la[idx]->setDirection(EXTEND);
      if (la[idx]->isSafe()) la[idx]->turn(ON);
    }
    if (dr == drLength[idx]) {
      la[idx]->setDirection(0);
      numberAtDestination++;
      Serial.print("L");
      Serial.print(idx + 1);
      Serial.print(" has reached it destination and stopped at ");
      Serial.println(la[idx]->convertDRPhys(la[idx]->readPosition()));
    }
  }

  Serial.println("Waiting for actuators to get to their final position");
  
  int prevReading[3];
  prevReading[0] = 0;
  prevReading[1] = 0;
  prevReading[2] = 0;
  int n = 0;
  while (numberAtDestination < 3 && !newCommand()) {
    for (int idx = 0; idx < 3; idx++) {
      
      la[idx]->isSafe(); // make sure that position is okay

      int dr = la[idx]->readPosition();
      int dir = la[idx]->getDirection();

      bool complete = dir == 0;
      if (!complete) {
        
        if(abs(dr-drLength[idx]) < 7) la[idx]->setPWM(127);
        if(abs(dr-drLength[idx]) < 5) la[idx]->setPWM(100);
        if(abs(dr-drLength[idx]) < 3) la[idx]->setPWM(50);
        if(abs(dr-drLength[idx]) < 1) la[idx]->setPWM(20);
        
        // check that the linac has actually moved (once every 50 loops)
        if(n%100 == 0 && abs(prevReading[idx] - dr) < 1 && !complete){
          la[idx]->setPWM(255);
          prevReading[idx] = dr;
        }
        n++;
        
        switch (dir) {
          case EXTEND:
            if (dr > drLength[idx]) {
              la[idx]->setDirection(0);
              la[idx]->turn(OFF);
              numberAtDestination++;
              Serial.print("L");
              Serial.print(idx + 1);
              Serial.print(" has reached it destination and stopped at ");
              Serial.println(la[idx]->convertDRPhys(la[idx]->readPosition()));
            }
            break;
          case RETRACT:
            if (dr < drLength[idx]) {
              la[idx]->setDirection(0);
              la[idx]->turn(OFF);
              numberAtDestination++;
              Serial.print("L");
              Serial.print(idx + 1);
              Serial.print(" has reached it destination and stopped at ");
              Serial.println(la[idx]->convertDRPhys(la[idx]->readPosition()));
            }
            break;

        }
      }

    }
  }
}

void executeNewCommand(int type) {
  switch (type) {
    case POSITION:
      break;
    case DIRECT:
      break;
    case NUDGE:
      break;

  }
}

void setup() {
  Serial.begin(9600);
  Wire.begin(I2C_ADDRESS);
  Wire.onReceive(receiveEvent);
  delay(1000);
  // set max's
  la[0]->setMAX_DR(L1_MAX);
  la[1]->setMAX_DR(L2_MAX);
  la[2]->setMAX_DR(L3_MAX);

  // set min's
  la[0]->setMIN_DR(L1_MIN);
  la[1]->setMIN_DR(L2_MIN);
  la[2]->setMIN_DR(L3_MIN);

  // set calibration coeffs
  la[0]->setCalibration(0, 2.44, 621);
  la[1]->setCalibration(0, 2.419, 627);
  la[2]->setCalibration(-0.0303, 16.35, -16.79);

  // initalize pins
  la[0]->initalizePins();
  la[1]->initalizePins();
  la[2]->initalizePins();

  invKinCommand(500, 300, 0);
}
int i = 1;
void loop() {
  int input = Serial.parseInt();
  if (input == 1) {
    la[i]->turn(ON, EXTEND);
    delay(1000);
    la[i]->turn(OFF);
  } else if (input == -1) {
    la[i]->turn(ON, RETRACT);
    delay(1000);
    la[i]->turn(OFF);
  } else if (input == 2) {
    la[i]->turn(ON, EXTEND, 127);
    delay(1000);
    la[i]->turn(OFF);
  } else if (input == -2) {
    la[i]->turn(ON, RETRACT, 127);
    delay(1000);
    la[i]->turn(OFF);
  }
  Serial.println(la[i]->readPosition());
}




