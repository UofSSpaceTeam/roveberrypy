
/*



*/

#include <VNH3SP30.h>

// number of linear actuator being used
int numLinac = 2;  // all arrays must be of length numLinac. However dir must be length numLinac + 1


// pin connections
#define L1inA 13
#define L1inB 12
#define L1pwm 10
#define L2inA 4 
#define L2inB 5 
#define L2pwm 6
// #define L3inA
// #define L3inB
// #define L3pwm
#define BASEinA 7
#define BASEinB 8
#define BASEpwm 9

int wiper[2];       
int minimum[2];
int maximum[2];

// create objects
VNH3SP30 linac[2] = { VNH3SP30(L1inA, L1inB, L1pwm) ,
                      VNH3SP30(L2inA, L2inB, L2pwm) };
                //    VNH3SP30(L3inA, L3inB, L3pwm) };
VNH3SP30 base (BASEinA, BASEinB, BASEpwm);


// global variables
int newPosition[2];    // analogReadValue which the linac is being set to
int initialPosition[2];      // intial position of the linac
bool inMotion[2];   // bool :: whether or not the linac's position is being set 
int dir[3];         // direction the linac needs to go
float scalingCoeff[2];  // scaling coefficient to convert analogReadValue to mm

// base variables
int interrupt_counter;
int newPositionCount;
const int pphr = 20088;  // points per half rotation of base
const int base_speed = 200;  // duty cycle of base
bool rotationInProgress = false;

//function headers
void setPosition (float[]);
void checkLinacPosition();
void checkBasePosition();
void positionChange();
// int* inverseKinecmatics(float*);


void setup() {
  // setup serial
  Serial.begin(9600);
  Serial.println("ARM_controller test!");

  //initalize interrupts
//  attachInterrupt(0,positionChange,CHANGE);
//  attachInterrupt(1,positionChange,CHANGE);


  //initalize pins and linear actuator constants
  wiper[0] = A1;
  minimum[0] = 392;
  maximum[0] = 583;
  scalingCoeff[0] = 0.615;

  wiper[1] = A0;
  minimum[1] = 410;
  maximum[1] = 583;
  scalingCoeff[1] = 0.615;

  // wiper[2] = A2;
  // minimum[2] = ;
  // maximum[2] = ;

  // make sure the linac are in brake position
  for(int i = 0; i < numLinac ; i++){
    inMotion[i] = false;
    linac[i].setDutyCycle(0);
  }
  
  // set position
  float positionArr[2];
  
  positionArr[0] = 50;
  positionArr[1] = 50;
  positionArr[2] = 0;
  
  
  Serial.println("Setting positions: ");
  Serial.print("L1: ");
  Serial.println(minimum[0] + 2 + positionArr[0]/scalingCoeff[0]);
  Serial.print("L1 is currently at: ");
  Serial.println(analogRead(A1));
  Serial.print("L2: ");
  Serial.println(minimum[1] + 2 + positionArr[1]/scalingCoeff[1]);
  Serial.print("L2 is currently at: ");
  Serial.println(analogRead(A0));
  Serial.print("BASE: ");
  Serial.println(positionArr[2]);
  Serial.print("BASE is currently at: ");
  Serial.println("not connected");
  
  setPosition(positionArr);
  

}




void loop() {

  checkLinacPosition();
  checkBasePosition();

  
  // if(Serial.available() && !inMotion[0] && !inMotion[1] && !rotationInProgress){
  //   Serial.println("Set position of the arm.")
  //   Serial.println("Enter L1 length [ 0 mm , 109 mm]")
  //   float input[numLinac] = { 0 , 0 , 0 };

  //   Serial.print("The current position is: ");
  //   Serial.println(analogRead(A1));
  //   float pos[1] ={ Serial.parseFloat()};
  //   if(pos[0] != 0){
  //     setPosition(pos);
  //   }
  // }
}

//-------------------------------------------------------------------------

void checkBasePosition(){
  if(rotationInProgress){
    if(interrupt_counter < newPositionCount){
      base.setDutyCycle(base_speed*dir[numLinac]);
    }
    else{
      rotationInProgress = false;
      // stop base and update position
      base.setDutyCycle(0);
      base.updatePosition(interrupt_counter*dir[numLinac]);
      interrupt_counter =0;
      newPositionCount = 0;
    }
  }
}

void positionChange(){ interrupt_counter ++; }

void checkLinacPosition(){
  // loop to set position of all the linacs
  for(int i = 0; i < numLinac ; i++){
    if(inMotion[i]){ // if the position of lineac[i] is currently being set
      float currentPosition = analogRead(wiper[i]); // read the current position (0 to 1023)
      Serial.println((newPosition[i] - currentPosition));
      if((dir[i]*(newPosition[i] - currentPosition) < 0) || (currentPosition < minimum[i]) || (currentPosition > maximum[i]) ){ // check if linac is at proper pos
          inMotion[i] = false;
          linac[i].setDutyCycle(0);
      }
      else{
        linac[i].setDutyCycle(255*dir[i]); // if we arent at the proper position then set the speed 
        // [enter set speed algo. here]
      }
    }
  }
}


void setPosition(float* pos){ 

  // set up setPosition for each linac
  for(int i = 0; i < numLinac ; i++){
    newPosition[i] = minimum[i] + 2 + pos[i]/scalingCoeff[i]; // analog read value corresponding to <pos> mm.
    initialPosition[i] = (analogRead(wiper[i]));      // inital position...currently not used but here for set speed algo
    
    if(initialPosition[i] != pos[i]){              // check that we are not already at the proper position
      inMotion[i] = true;                 // intialize setting position
      dir[i] = (newPosition[i] - initialPosition[i])/abs(newPosition[i] - initialPosition[i]);  // direction
    }
  }

  // set up base rotation
  newPositionCount = pphr/180.0*pos[2] - base.getPosition();
  if(newPositionCount != 0){
    rotationInProgress = true;
    base.updatePosition(interrupt_counter*dir[numLinac]);
    interrupt_counter = 0;
    dir[numLinac] = newPositionCount/abs(newPositionCount);
    newPositionCount = abs(newPositionCount);
  }
  
  

}


// int* inverseKinecmatics(float* pos){
//    [inverse kinematic code]
// }

