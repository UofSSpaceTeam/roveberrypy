

#include "VNH3SP30.h"

// number of linear actuator being used
#define numLinac 2  // all arrays must be of length numLinac. However dir must be length numLinac + 1


// pin connections
#define L1inA 
#define L1inB 
#define L1pwm 
#define L2inA 
#define L2inB 
#define L2pwm 
// #define L3inA
// #define L3inB
// #define L3pwm
#define BASEinA 
#define BASEinB 
#define BASEpwm 

int wiper[numLinac];       
int minimum[numLinac];
int maximum[numLinac];

// create objects
VNH3SP30 linac[numLinac] = { VNH3SP30(L1inA, L1inB, L1pwm) , VNH3SP30(L2inA, L2inB, L2pwm) };
                //    VNH3SP30(L3inA, L3inB, L3pwm) };
VNH3SP30 base (BASEinA, BASEinB, BASEpwm);


// global variables
int newPosition[numLinac];    // analogReadValue which the linac is being set to
int initialPosition[numLinac];      // intial position of the linac
bool inMotion[numLinac];   // bool :: whether or not the linac's position is being set 
int dir[numLinac + 1];         // direction the linac needs to go
float scalingCoeff[numLinac];  // scaling coefficient to convert analogReadValue to mm

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
  attachInterrupt(0,positionChange,CHANGE);
  attachInterrupt(1,positionChange,CHANGE);

  //initalize pins and linear actuator constants
  wiper[0] = A0;
  minimum[0] = 392;
  maximum[0] = 583;
  scalingCoeff[0] = 0.615;

  wiper[1] = A1;
  minimum[1] = 410;
  maximum[1] = 583;
  scalingCoeff[1] = 0.615;

  // ...
  // wiper[numLinac] = A2;
  // minimum[numLinac] = ;
  // maximum[numLinac] = ;

  // make sure the linac are in brake position
  for(int i = 0; i < numLinac ; i++){
    inMotion[i] = false;
    linac[i].setDutyCycle(0);
  }

}


void loop() {

  checkLinacPosition();
  checkBasePosition();

  // get position somehow
  // call setPosition(position), where position is array of positions
  // position[0] is new position of L1 , [mm]
  // position[1] is new position of L2 , [mm]
  // position[2] is new position of L3 , [mm]
  // position[3] is new position of BASE , [deg]


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
      Serial.println(dir[i]*(newPosition[i] - currentPosition));
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
  newPositionCount = pphr/180.0*pos[numLinac] - base.getPosition();
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
