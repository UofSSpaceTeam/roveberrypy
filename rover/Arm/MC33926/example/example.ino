/*

MC33926 motor controller library example
Written by Liam Bindle
March 21, 2015

- getPosition has not been implemented yet
- feedback has not been tested

Pin Configuration:

M2FB   A0   <- Arduino connection 
M2Sf'  13   <- Arduino connection 
M2D1   GND
M2D2   VDD
M2IN1  11   <- Arduino connection 
M2IN2  10   <- Arduino connection 
INV    GND
SLEW   GND
EN     12   <- Arduino connection 

*/

#include <SoftwareSerial.h>
#include <MC33926.h> //inlcude the library

#define sf 13
#define in1 11
#define in2 10
#define en 12
#define fb A0

MC33926 m1 (in1, in2, en, fb, sf); // set up, initally everything is disabled

void setup() {
  Serial.begin(9600);
  Serial.println(" ________________________________________________ ");
  Serial.println("|                                                |");
  Serial.println("|            MC33926 library example             |");
  Serial.println("|            March 21, 2015                      |");
  Serial.println("|________________________________________________|");
  Serial.println(" ");
  Serial.println(" ");
  Serial.println(" ");
  
}

void loop() {
  
  //give command
  Serial.flush();
  Serial.println("Options:");
  Serial.println("1.   Enable/Disable");
  Serial.println("2.   Set duty cycle");
  Serial.println("3.   Set position [not yet implemented]");
  Serial.println("4.   Get position [not yet implemented]");
  Serial.println("Waiting for entry...");
  
  while(!Serial.available());
  int foo = Serial.read()-'0';
  
  if(foo == 1){
    Serial.println(" ");
    Serial.println("Enable = 1, Disable = 0");
    Serial.println("Waiting for entry...");
    while(!Serial.available()); 
    foo = Serial.read()-'0';
    if(foo == 1){
       m1.enable(); 
    }
    else if(foo == 0){
       m1.disable(); 
    }
    else{
       Serial.println("Invalid Entry!"); 
    }
    bool state = m1.checkState();
    Serial.print("Motor state is now: ");
    Serial.println(state); 
    Serial.println(" ");
  }
  
  else if(foo == 2){
    Serial.println(" ");
    Serial.println("Enter an integer between -255 and 255");
    while(!Serial.available());
    Serial.println("Waiting for entry...");
    foo = Serial.parseInt();
    m1.setDutyCycle(foo);
    m1.checkFlag();
    Serial.print("The duty cycle has been set to: ");
    Serial.println(foo);
    Serial.println(" "); 
  }
  

}