
//Pololu lsm303 library, and Heading.ino example code
#include <Wire.h>
#include <LSM303.h>

LSM303 compass;

void setup() {
  Serial.begin(9600);
  Wire.begin();
  compass.init();
  compass.enableDefault();
  
  /*
  Calibration values; the default values of +/-32767 for each axis
  lead to an assumed magnetometer bias of 0. Use the Calibrate example
  program to determine appropriate values for your particular unit.
  */
  compass.m_min = (LSM303::vector<int16_t>){-447, -619, -451};
  compass.m_max = (LSM303::vector<int16_t>){+592, +332, +489};
}

void loop() {
  char inbyte = Serial.read();
  if(inbyte == 'r') {
    compass.read();
    float heading = compass.heading();
    Serial.print(heading);
  }
  
}
