//Arduino 1.0+ Only
//Arduino 1.0+ Only

//////////////////////////////////////////////////////////////////
//©2011 bildr
//Released under the MIT License - Please reuse change and share
//Simple code for the TMP102, simply prints temperature via serial
//////////////////////////////////////////////////////////////////

#include <Wire.h>
#include <SoftwareSerial.h>

SoftwareSerial mySerial(3,2);
int tmp102Address = 0x48;

void setup(){
  Serial.begin(9600);
  mySerial.begin(9600);
  Wire.begin();
  delay(500);
  
}

void loop(){

  int celsius = getTemperature();
  char str[8];
  sprintf(str, "%i", celsius);
  mySerial.write("                                ");
  mySerial.write(254);
  mySerial.write(128);
  mySerial.write("Celcius: ");
  mySerial.write(str);
 delay(2000);
  
  Serial.print("Celsius: ");
  Serial.println(str);


 

  delay(2000); //just here to slow down the output. You can remove this
}

int getTemperature(){
  Wire.requestFrom(tmp102Address,2); 

  byte MSB = Wire.read();
  byte LSB = Wire.read();

  //it's a 12bit int, using two's compliment for negative
  int TemperatureSum = ((MSB << 8) | LSB) >> 4; 

  int celsius = TemperatureSum*0.0625;
  return celsius;
}
