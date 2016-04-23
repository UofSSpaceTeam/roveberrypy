#include <FlexCAN.h>

int led = 13;
FlexCAN CANbus(1000000);
static CAN_message_t txmsg, rxmsg;

void setup() {
  CANbus.begin();
  pinMode(led, OUTPUT);
  digitalWrite(led, 1);

  delay(1000);
  Serial.println("CAN Testing Time!!");

}

void loop() {
  rxmsg.timeout = 10;
  while(CANbus.read(rxmsg));

  Serial.print(rxmsg.id);
  Serial.print(' ');
  for(int i = 0; i < 8; i++) {
    Serial.print((char)rxmsg.buf[i]);
  }
  Serial.print("\r\n");

  txmsg.len = 8;
  txmsg.id = 0x222;

  char* data = "DEADBEEF";

  for(unsigned int i = 0; i < strlen(data); i++){
    txmsg.buf[i] = data[i];
  }

  digitalWrite(led, 1);
  CANbus.write(txmsg);

  delay(10);
  digitalWrite(led, 0);
  delay(10);
}
