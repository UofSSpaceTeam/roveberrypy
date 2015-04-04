/*

 
 */

#include <VNH3SP30.h>

//define pin connections
#define inA 13
#define inB 12
#define pmw 10
#define en 4

// create motor object
VNH3SP30 base (inA,inB,en, pmw);

// interrupt counter
int temp_tick_cnt;
int set_tick;
int sign;

//define constants to be used
const int ppr = 20088;
const int maxSpeed = 255;
const int minSpeed = 80;
bool rotationInProgress = false;
bool readSerial = true;

//function headers
void positionChange();
void setPosition(int);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.println("VNH3SP30 test!");
  attachInterrupt(0,positionChange,CHANGE);
  attachInterrupt(1,positionChange,CHANGE);
}

void loop() {

  if(rotationInProgress){
    if(temp_tick_cnt < set_tick){
      float foo=((maxSpeed-minSpeed)*1.0/ppr)*2;
      if(temp_tick_cnt > set_tick / 2){
        base.setDutyCycle((foo*(set_tick - temp_tick_cnt)*0.8+minSpeed)*sign);
      }
      else{
        base.setDutyCycle((foo*temp_tick_cnt+minSpeed)*sign);
      }
    }
    else{
      rotationInProgress = false;
      // stop base and update position
      base.setDutyCycle(0);
      base.updatePosition(temp_tick_cnt*sign);
      temp_tick_cnt =0;
      set_tick = 0;
      Serial.print("The current position of the motor is: ");
      Serial.println(base.getPosition()*180.0/ppr);
    }
  }

  if(Serial.available() && !rotationInProgress){
    int pos = Serial.parseInt();
    if(pos != 0){
      int positionm = ppr/180.0*pos;
      setPosition(positionm);
      readSerial = false;
    }
  }

}

//-------------------------------------------------------------------------

void positionChange(){ 
  temp_tick_cnt ++;  
}

void setPosition(int pos){
  //set up
  rotationInProgress = true;
  temp_tick_cnt = 0;
  set_tick = pos - base.getPosition();
  sign = set_tick/abs(set_tick);
  set_tick = abs(set_tick);
}



