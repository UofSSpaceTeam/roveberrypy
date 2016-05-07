#include "motor.h"

uint_t cur = 0;
int dir = 0;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.println("starting arm board");
  pinMode(_MOCHI_SEL[0], OUTPUT);
  pinMode(_MOCHI_SEL[1], OUTPUT);
  pinMode(_MOCHI_SEL[2], OUTPUT);
  pinMode(_MOCHI_DAT, OUTPUT);
  pinMode(_MOCHI_DAT, OUTPUT);
  pinMode(_MOCHI_WRT, OUTPUT);
  pinMode(20, OUTPUT);
  
  digitalWrite(_MOCHI_WRT, LOW);
  delay(1000);
  digitalWrite(_MOCHI_SEL[0], LOW);
  digitalWrite(_MOCHI_SEL[1], LOW);
  digitalWrite(_MOCHI_SEL[2], HIGH);
  delay(1000);
  Serial.println("Starting");
}

void loop() {
  // put your main code here, to run repeatedly:

/*
  for(int i = 0; i < 200; ++i) {
    analogWrite(20, i);
    delay(10);
  }
    dir ^= 0x01;
  digitalWrite(_MOCHI_DAT, dir);
  digitalWrite(_MOCHI_WRT, HIGH);
  delay(1);
  digitalWrite(_MOCHI_WRT, LOW);
  for(int i = 200; i > 0; --i) {
    analogWrite(20, i);
    delay(10);
  }*/
  for(int b = 0; b < 4; ++b)
  {
    digitalWrite(_MOCHI_CSEL[b], HIGH);
    delay(1000);
    Serial.print(1<<b);
    Serial.print(";");
    delay(500);
    int foo = digitalRead(_MOCHI_CRD);
    Serial.println(foo);
    
    digitalWrite(_MOCHI_CSEL[b], LOW);
  }
  uint_t count = moc_readPosition(moc_spec+4);
  Serial.print("Count = ");
  Serial.println(count);
  delay(1000);
}
