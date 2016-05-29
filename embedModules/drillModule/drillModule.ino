#include <FlexCAN.h>
#include <Servo.h>

#define TIMEOUT 1000
#define DURATION 1000

FlexCAN CANbus(500000);
static CAN_message_t txmsg, rxmsg;

int drill_IN1 = 5;
int drill_IN2 = 6;
int elev_IN1 = 7;
int elev_IN2 = 8;
int drill_PWM = 9; //D2
int elev_PWM = 10;
int EN = 11;
int drill_PWM2 = 0;  //D1
int elev_PWM2 = 1;

//moisture
int decagon_pin = A1;
float V = 3.3 ;

//moisture
float coef1 = 0 ;
float coef2 = 2.97*pow(10,-9) ;
float coef3 = -7.37*pow(10,-6) ;
float coef4 = 6.69*pow(10,-3) ;
float coef5 = -1.92 ;

//temperature
float temperature ;
int temp_pin = A0;

static int cmd_drill = 500;
static int cmd_elev = 501;
static int cmd_moisture = 502;
static int cmd_temp = 503;

unsigned long timeout;
unsigned long moisture_timeout;
unsigned long temp_timeout;
int cmd = 0;
int val = 0;
char* data = (char*)malloc(sizeof(char)*8);



void setup() {
  // put your setup code here, to run once:
  CANbus.begin();
  pinMode(drill_IN1, OUTPUT);
 pinMode(drill_IN2, OUTPUT);
 pinMode(elev_IN1, OUTPUT);
 pinMode(elev_IN2, OUTPUT);
 pinMode(drill_PWM, OUTPUT);
 pinMode(elev_PWM, OUTPUT);
 pinMode(drill_PWM2, OUTPUT);
 pinMode(elev_PWM2, OUTPUT);
 pinMode(EN, OUTPUT);
 pinMode(13, OUTPUT);

 pinMode(decagon_pin, INPUT);
 
 digitalWrite(EN, LOW);
 digitalWrite(drill_PWM2, LOW);
 digitalWrite(elev_PWM2, LOW);
 
  timeout = millis();
  moisture_timeout = millis();
  temp_timeout = millis();
}

void loop() {
  // put your main code here, to run repeatedly:
  rxmsg.timeout = 0;
  if (CANbus.read(rxmsg)){
  cmd = rxmsg.id;
  for(int i = 0; i < 8; i++) {
    data[i] = rxmsg.buf[i];
  }
  val = atoi(data);
  if(cmd == cmd_drill){
    Serial.println("drill");
    Serial.println(val);
    if(val == 0){
      analogWrite(drill_PWM, 0);
      }
    else if(val < 0){
      digitalWrite(drill_IN1, HIGH);
      digitalWrite(drill_IN2, LOW);
      analogWrite(drill_PWM, abs(val));
      digitalWrite(EN, HIGH);
      }
    else {
      digitalWrite(drill_IN1, LOW);
      digitalWrite(drill_IN2, HIGH);
      analogWrite(drill_PWM, abs(val));
      digitalWrite(EN, HIGH);
      }
    timeout = millis();
    }
  else if(cmd == cmd_elev){
    Serial.println("elev");
    Serial.println(val);
    if(val == 0){
      analogWrite(elev_PWM, 0);
      }
    else if(val < 0){
      digitalWrite(elev_IN1, LOW);
      digitalWrite(elev_IN2, HIGH);
      analogWrite(elev_PWM, abs(val));
      digitalWrite(EN, HIGH);
      }
    else {
      digitalWrite(elev_IN1, HIGH);
      digitalWrite(elev_IN2, LOW);
      analogWrite(elev_PWM, abs(val));
      digitalWrite(EN, HIGH);
      }
    timeout = millis();
    }
  }
  if(millis() - timeout > TIMEOUT)
  {
    Serial.println("TIME OUT");
    digitalWrite(EN, LOW);
    timeout = millis();
  }
  cmd = 0;
  rxmsg.id = 0;
  

  //moisture
  if(millis() - moisture_timeout > DURATION){
  int raw_moisture_reading = analogRead(decagon_pin) ;

  //code to convert to raw voltage (in mV)
  //float mV = (raw_moisture_reading/1023.0)*950.0+300.0 ;
  //Note: Teensy uses 3.3 V as VRef by default, other boards may use different reference voltages
  float mV = raw_moisture_reading*(3.3/1.0240) ;

  //code to calibrate (curve provided in datasheet)
  float moisture_reading = 100*(coef1*pow(mV,4)+coef2*pow(mV,3)+coef3*pow(mV,2)+coef4*mV+coef5) ;
  //float moisture_reading = mV*57.0 ;
  txmsg.len = 8;
  txmsg.id = cmd_moisture;
  sprintf(data, "%f", moisture_reading);
  //Serial.println("moisture");
  //Serial.println(data);
  for(unsigned int i = 0; i < 8; i++){
    txmsg.buf[i] = data[i];
  }
  CANbus.write(txmsg);
  moisture_timeout = millis();
  }

  //temperature
  if(millis() - temp_timeout > DURATION){
  int rawData = analogRead(temp_pin) ;

  // Convert value to voltage by scaling between 0.0 and 5.0
  float Vout = rawData * (3.3 / 1023.0) ;

  // Datasheet says temperature roughly linear (Provides polynomial for more realistic values, look later)
  temperature = Vout/0.005 ;
  
  txmsg.len = 8;
  txmsg.id = cmd_temp;
  sprintf(data, "%f", temperature);
  //Serial.println("temperature");
  
  for(unsigned int i = 0; i < 8; i++){
    txmsg.buf[i] = data[i];
  }
  //Serial.println(txmsg.buf);
  CANbus.write(txmsg);
  temp_timeout = millis();
  }

  
}


