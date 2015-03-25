
//Define pins
int input_channelA = 2;
int input_channelB = 6;
int output_channelA = 5;
int output_channelB = 4;
int powerCtrl = 3;


int pos = 0; //global state of the motor position
int ppr = 186; //Points per rotation

//readMotorPosition()
//Interput function
//Keeps track of the motor position and 
//prints the value in radians to serial
void readMotorPosition() {
  if(digitalRead(input_channelA)) {
    if(pos >= 186) {
        pos = 0;
      } else {
        pos++;
      }
    }
   /*else  {
     if(pos <= 0) {
        pos = 186;
      } else {
        pos--;
      }
    }*/
    Serial.println(pos*2.0*PI/ppr);
}

//setMotorPower(power)
//Sets the pwm pin to control the speed 
//of the motor.
void setMotorPower(int power) {
  if(power > 0 && power < 256) {
    analogWrite(powerCtrl, power);
    digitalWrite(output_channelA, HIGH);
  }
  else {
    analogWrite(powerCtrl, 0);
    digitalWrite(output_channelA, LOW);
  }
}


//getSerial()
//Gathers character input from 
//the serial and converts it to an integer.
int getSerial() {
  int inbyte, serialdata;
  serialdata = 0;
   do {
    inbyte = Serial.read();  
    if (inbyte > 0 && inbyte != '\n') { 
      serialdata = serialdata * 10 + inbyte - '0';
    }
  } while (inbyte != '\n');
  return serialdata;
}

//rotate(angle, power) !!!WORK IN PROGRESS!!!
//rotates the motor to an angle in radians
void rotate(int angle, int power) {
  float c = 0;
  setMotorPower(power);
  while(pos*2.0*PI/ppr <= angle && pos*2.0*PI/ppr <= 2.0*PI) {
    readMotorPosition();
    Serial.println(pos*2.0*PI/ppr);
  }
  setMotorPower(0);
}
  
  

void setup() {
  // Initialization for recieving data from motor
  pinMode(input_channelA, INPUT);
  pinMode(input_channelB, INPUT);
  
  //Initialization for controling the motor.
  pinMode(output_channelA, OUTPUT);
  pinMode(output_channelB, OUTPUT);
  digitalWrite(output_channelB, LOW);
  
  //when pin 2 changes, call readMotorPosition()
  attachInterrupt(0,readMotorPosition,CHANGE);
  
  Serial.begin(9600); 
}

int power = 128; //Initial motor speed
void loop() {
   
   setMotorPower(power);
   power = getSerial();
   
}


