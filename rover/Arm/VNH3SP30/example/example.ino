/*

Pin Configuration for MC33926:

inA   3
inB   4
en    5
pmw   6
pot   A0;

*/

#include <VNH3SP30.h>

//constants
int numLinac = 1; // number of linear actuators
int tolerance = 10; // position tolerance [analogReadValue], 10 <=> 1.5mm for 6in stoke linacs

// pin connections
int inA_0 = 3;      // channel A pin
int inB_0 = 4;      // channel B pin
int en_0 = 5;       // enable pin
int pmwPin_0 = 6;   // pwm pin
int fb[1];          // position feedback pin


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

  // make sure the linac are in brake position
  for(int i = 0; i < numLinac ; i++){
    inMotion[i] = false;
    linac[i].setDutyCycle(0);
  }

  // set linac specific constants (fb and scalingCoeff)
  fb[0] = A0;
  scalingCoeff[0] = 0.148974; //   mm / analogReadValue

}

//function headers
void setPosition (float[]);
// int* inverseKinecmatics(float*);


void loop() {

  // loop to set position of all the linacs
  for(int i = 0; i < numLinac ; i++){
    if(inMotion[i]){ // if the position of lineac[i] is currently being set
      float curFb = analogRead(fb[i]); // read the current position (0 to 1023)
      if(dir[i]*(newPosFb[i] - curFb) < tolerance){ // check if linac is at proper pos
          inMotion[i] = false;
          linac[i].setDutyCycle(0);
      }
      else{
        linac[i].setDutyCycle(100*dir[i]); // if we arent at the proper position then set the speed 
        // [enter set speed algo. here]
      }
    }
  }

  // if(Serial.available()){
  //   Serial.print("The current position of the motor is: ");
  //   Serial.println(m1.getPosition()*180.0/ppr);
  //   int pos = Serial.parseInt();
  //   if(pos != 0){
  //     int positionm = ppr/180.0*pos;
  //     setPosition(positionm, m1);
  //     Serial.println(positionm);
  //   }
  // }
}

//-------------------------------------------------------------------------

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

void setPosition(float* pos){ // position in mm

  // set up setPosition for each linac
  for(int i = 0; i < numLinac ; i++){
    newPosFb[i] = pos[i]/scalingCoeff[i]; // analog read value corresponding to <pos> mm.
    intPos[i] = (analogRead(fb[i]));      // inital position...currently not used but here for set speed algo
    
    if(intPos[i] != pos[i]){              // check that we are not already at the proper position
      inMotion[i] = true;                 // intialize setting position
      dir[i] = (pos[i] - intPos[i])/abs(pos[i] - intPos[i]);  // direction
    }
  }

}


// int* inverseKinecmatics(float* pos){
//    [inverse kinematic code]
// }
