/*

Pin Configuration for L2:

A -- BLACK
B -- RED

A1 -- BLUE
GND -- WHITE
5V -- YELLOW 

*/

#include <VNH3SP30.h>

//constants
int numLinac = 1; // number of linear actuators
int tolerance = 1; // position tolerance [analogReadValue], 10 <=> 1.5mm for 6in stoke linacs

// pin connections
int inA_0 = 13  ;      // channel A pin
int inB_0 = 12;      // channel B pin
int en_0 = 4;       // enable pin
int pmwPin_0 = 10;   // pwm pin
int fb[1];          // position feedback pin

int minimum = 410;
int maximum = 583;


// create array ofVNH3SP30 objects
VNH3SP30 linac[1] = { VNH3SP30(inA_0, inB_0, en_0, pmwPin_0) };

// global variables
int newPosFb[1];    // analogReadValue which the linac is being set to
int intPos[1];      // intial position of the linac
bool inMotion[1];   // bool :: whether or not the linac's position is being set 
int dir[1];         // direction the linac needs to go
float scalingCoeff[1];  // scaling coefficient to convert analogReadValue to mm


void setup() {
  // setup serial
  Serial.begin(9600);
  Serial.println("VNH3SP30 test!");
  Serial.println(analogRead(A1));

  // make sure the linac are in brake position
  for(int i = 0; i < numLinac ; i++){
    inMotion[i] = false;
    linac[i].setDutyCycle(0);
  }

  // set linac specific constants (fb and scalingCoeff)
  fb[0] = A1;
  scalingCoeff[0] = 0.615; //   mm / analogReadValue

}

//function headers
void setPosition (float[]);
// int* inverseKinecmatics(float*);


void loop() {

  // loop to set position of all the linacs
  for(int i = 0; i < numLinac ; i++){
    if(inMotion[i]){ // if the position of lineac[i] is currently being set
      float curFb = analogRead(fb[i]); // read the current position (0 to 1023)
      Serial.println(dir[i]*(newPosFb[i] - curFb));
      if((dir[i]*(newPosFb[i] - curFb) < tolerance) || (curFb < minimum) || (curFb > maximum) ){ // check if linac is at proper pos
          inMotion[i] = false;
          linac[i].setDutyCycle(0);
      }
      else{
        linac[i].setDutyCycle(60*dir[i]); // if we arent at the proper position then set the speed 
        // [enter set speed algo. here]
      }
    }
  }

  
  if(Serial.available() && !inMotion[0]){
    Serial.print("The current position is: ");
    Serial.println(analogRead(A1));
    float pos[1] ={ Serial.parseFloat() - 9};
    if(pos[0] != -9){
      setPosition(pos);
    }
  }
}

//-------------------------------------------------------------------------

void setPosition(float* pos){ // position in mm
  
  Serial.print("The linac is being set to " );
  Serial.print(pos[0]);
  Serial.println(" mm");
  // set up setPosition for each linac
  for(int i = 0; i < numLinac ; i++){
    newPosFb[i] = 413 + pos[i]/scalingCoeff[i]; // analog read value corresponding to <pos> mm.
    intPos[i] = (analogRead(fb[i]));      // inital position...currently not used but here for set speed algo
    
    if(intPos[i] != pos[i]){              // check that we are not already at the proper position
      inMotion[i] = true;                 // intialize setting position
      dir[i] = (newPosFb[i] - intPos[i])/abs(newPosFb[i] - intPos[i]);  // direction
    }
  }
  Serial.print("Dir = ");
  Serial.println(dir[0]);
  Serial.print("Looking for: ");
  Serial.println(newPosFb[0]);
  Serial.print("State: ");
  Serial.println(inMotion[0]);

}


// int* inverseKinecmatics(float* pos){
//    [inverse kinematic code]
// }
