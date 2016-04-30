#include <Servo.h>
#include <FlexCAN.h>
Servo servo1, servo2, servo3;
FlexCAN CANbus(1000000);
static CAN_message_t  rxmsg;
int pin_1 = 9;
int pin_2 = 10;
int pin_3 = 11;
int cmd_open = 400;
int cmd_close = 401;
int val_open = 0;
int val_close = 90;
char* data = (char*)malloc(sizeof(char)*8);
void setup() {
  // put your setup code here, to run once:
  CANbus.begin();
  servo1.attach(pin_1);
  servo2.attach(pin_2);
  servo3.attach(pin_3);
}

void loop() {
  // put your main code here, to run repeatedly:
  rxmsg.timeout = 10;
  while(CANbus.read(rxmsg));
  cmd = rxmsg.id;
  
  for(int i = 0; i < 8; i++) {
    data[i] = rxmsg.buf[i];
  }
  val = atoi(data);
  if(cmd == cmd_open){
    Serial.println("open");
    Serial.println(val);
    //Serial.println(count++);
    if(val == 1)
      servo1.write(val_open);
    else if(val == 2)
      servo2.write(val_open);
    else if(val == 3)
      servo3.write(val_open);
    }
  if(cmd == cmd_close){
    Serial.println("close");
    Serial.println(val);
    //Serial.println(count++);
    if(val == 1)
      servo1.write(val_close);
    else if(val == 2)
      servo2.write(val_close);
    else if(val == 3)
      servo3.write(val_close);
    }
    cmd = 0;
    rxmsg.id = 0;

}
