/*
_______________________________________________________________________
Rotary Encoder Example
March 25, 2015

Pin Configuration:

Rotary Encoder #1, r1
Ch A  7  <- Arduino connection
Ch B  8  <- Arduino connection

Rotary Encoder #2, r2
Ch A  5  <- Arduino connection
Ch B  6  <- Arduino connection

IMPORTANT NOTE:
All of the ouputs from the rotary encoder are connected
through an OR gate to the Arduino's interupt pin (for UNO 2)

OR gate (encoder outputs)   2  <- Arduino connection
_______________________________________________________________________
*/

#include <RotaryEncoder.h>

RotaryEncoder r1 (7,8);
RotaryEncoder r2 (5,6);

//upon interrupt update motor positions (this must manually be 
// put into the .ino file)
void stateChange(){
   r1.updatePosition();
   r2.updatePosition(); 
}

void setup() {
  // attach interupt to encoder channels (this must manually be
  // inlucded in the .ino file)
  attachInterrupt(0,stateChange,CHANGE); // 0 corresponds
                                       // to pin 2 on UNO
  // additional setup
  Serial.begin(9600);
  Serial.println(" ________________________________________________ ");
  Serial.println("|                                                |");
  Serial.println("|         Rotart Encoder library example         |");
  Serial.println("|         March 21, 2015                         |");
  Serial.println("|________________________________________________|");
  Serial.println(" ");
  Serial.println(" ");
  Serial.println(" ");
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.print("R1 Current position: ");
  Serial.println(r1.getPosition());
  Serial.print("R2 Current position: ");
  Serial.println(r2.getPosition());
  
  delay(10000); // delay to show that it will keep track of position on its own.
}
