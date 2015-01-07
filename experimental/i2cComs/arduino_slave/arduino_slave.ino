#include <Wire.h>

#define LED_PIN 13

byte slave_address = 7;
byte CMD_ON = 0x00;
byte CMD_OFF = 0x01;

void setup() {
  // Start I2C Bus as Slave
  Wire.begin(slave_address);
  Wire.onReceive(receiveEvent);
  
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);  

}

void loop() {

}

void receiveEvent(int howMany) {
  byte cmd = Wire.read();
  if (cmd == CMD_ON){
    digitalWrite(LED_PIN, HIGH);
  }else if(cmd == CMD_OFF){
    digitalWrite(LED_PIN, LOW);
  }
}

