#include <FlexCAN.h>
#include <Servo.h>

int led = 13;
FlexCAN CANbus(500000);
static CAN_message_t txmsg, rxmsg;
int mode = 5;
int pin_up_down = 6;  //range 130-220
int pin_left_right = 9;  //range 50-130, 90->stop
Servo myservo;
int cmd = 0;
int val = 0;
int cmd_up_down = 300;
int cmd_left_right = 301;
int count = 0;
char* data = (char*)malloc(sizeof(char)*8);
void setup() {
  CANbus.begin();
  pinMode(led, OUTPUT);
  pinMode(mode, OUTPUT);
  pinMode(pin_up_down, OUTPUT);
  myservo.attach(pin_left_right);
  
  
  digitalWrite(led, 1);
  analogWrite(mode, 120);
  
  delay(1000);
  //Serial.println("CAN Testing Time!!");

}

void loop() {
  digitalWrite(led, 1);
  rxmsg.timeout = 10;
  while(CANbus.read(rxmsg));
  
  //Serial.print(rxmsg.id);
  //Serial.print(' ');
  /*for(int i = 0; i < 8; i++) {
    Serial.print((char)rxmsg.buf[i]);
  }
  Serial.print("\r\n");*/
  cmd = rxmsg.id;
  
  for(int i = 0; i < 8; i++) {
    data[i] = rxmsg.buf[i];
  }
  val = atoi(data);
  if(cmd == cmd_up_down){
    Serial.println("up_down");
    Serial.println(val);
    Serial.println(count++);
    analogWrite(pin_up_down,val);
    }
  if(cmd == cmd_left_right){
    Serial.println("left_right");
    Serial.println(val);
    Serial.println(count++);
    myservo.write(val);
    }
    digitalWrite(led, LOW);
    
   cmd = 0;
   rxmsg.id = 0;

  /*txmsg.len = 8;
  txmsg.id = 0x222;

  char* data = "DEADBEEF";

  for(unsigned int i = 0; i < strlen(data); i++){
    txmsg.buf[i] = data[i];
  }

  digitalWrite(led, 1);
  CANbus.write(txmsg);

  delay(10);
  digitalWrite(led, 0);
  delay(10);*/
}
