#include <FlexCAN.h>
#include <Servo.h>

#define TIMEOUT 750

FlexCAN CANbus(500000);
static CAN_message_t txmsg, rxmsg;

byte drillPin = 9;
byte elevPin = 10;
Servo drillMotor;
short drillSpeed = 0;
short desiredDrillSpeed = 0;
Servo elevMotor;
short elevSpeed = 0;
short desiredElevSpeed = 0;
byte moisture = A0;
byte x = A1;

static int cmd_drill = 600;
static int cmd_elev = 601;
static int cmd_moisture = 602;
static int cmd_x = 603;

unsigned long timeout;
int cmd = 0;
int val = 0;
char* data = (char*)malloc(sizeof(char)*8);

void updateDrill();
void updateElev();
void stopAll();

void setup() {
  // put your setup code here, to run once:
  CANbus.begin();
  pinMode(moisture, INPUT);
  pinMode(x, INPUT);
  drillMotor.attach(drillPin);
  elevMotor.attach(elevPin);
  stopAll();
    
  timeout = millis();
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
  if(cmd == cmd_drill){
    Serial.println("drill");
    Serial.println(val);
    desiredDrillSpeed = val;
    updateDrill();
    timeout = millis();
    }
  else if(cmd == cmd_elev){
    Serial.println("elev");
    Serial.println(val);
    desiredElevSpeed = val;
    updateElev();
    timeout = millis();
    }
  if(millis() - timeout > TIMEOUT)
  {
    Serial.println("TIME OUT");
    stopAll();
    timeout = millis();
  }
  cmd = 0;
  rxmsg.id = 0;

  txmsg.len = 8;
  txmsg.id = cmd_moisture;
  val = analogRead(moisture);
  itoa(val, data, 10);
  Serial.println("moisture");
  Serial.println(data);
  for(unsigned int i = 0; i < strlen(data); i++){
    txmsg.buf[i] = data[i];
  }
  CANbus.write(txmsg);

  txmsg.len = 8;
  txmsg.id = cmd_x;
  val = analogRead(x);
  itoa(val, data, 10);
  Serial.println("x");
  Serial.println(data);
  for(unsigned int i = 0; i < strlen(data); i++){
    txmsg.buf[i] = data[i];
  }
  CANbus.write(txmsg);
}

void updateDrill()
{
  if(desiredDrillSpeed == 0)
  {
    drillMotor.writeMicroseconds(1500);
    drillSpeed = 0;
    return;
  }
  else if(abs(desiredDrillSpeed - drillSpeed) < 5)
    drillSpeed = desiredDrillSpeed;
  else if(desiredDrillSpeed > drillSpeed)
    drillSpeed += 5;
  else
    drillSpeed -= 5;
  drillMotor.writeMicroseconds(map(drillSpeed, -255, 255, 900, 2100));
}
  
void updateElev()
{
  if(desiredElevSpeed == 0)
  {
    elevMotor.writeMicroseconds(1500);
    elevSpeed = 0;
    return;
  }
  else if(abs(desiredElevSpeed - elevSpeed) < 5)
    elevSpeed = desiredElevSpeed;
  else if(desiredElevSpeed > elevSpeed)
    elevSpeed += 5;
  else
    elevSpeed -= 5;
  elevMotor.writeMicroseconds(map(elevSpeed, -255, 255, 900, 2100));
}

void stopAll()
{
  Serial.println("stopped");
  drillSpeed = 0;
  desiredDrillSpeed = 0;
  elevSpeed = 0;
  desiredElevSpeed = 0;
  drillMotor.writeMicroseconds(1500);
  elevMotor.writeMicroseconds(1500);
}
