#include "motor.h"

uint_t cur = 0;

void setup() {
  // put your setup code here, to run once:

}

void loop() {
  // put your main code here, to run repeatedly:
  moc_setDirection(motor[cur].moc, FORWARD);
  moc_setSpeed(motor[cur].moc, 75);
  delay(200);
  moc_setSpeed(motor[cur].moc, 150);
  delay(200);
  moc_setSpeed(motor[cur].moc, 255);
  delay(200);
  moc_setSpeed(motor[cur].moc, 150);
  delay(200);
  moc_setSpeed(motor[cur].moc, 75);
  delay(200);
  moc_setSpeed(motor[cur].moc, 0);

  moc_setDirection(motor[cur].moc, REVERSE);
  moc_setSpeed(motor[cur].moc, 75);
  delay(200);
  moc_setSpeed(motor[cur].moc, 150);
  delay(200);
  moc_setSpeed(motor[cur].moc, 255);
  delay(200);
  moc_setSpeed(motor[cur].moc, 150);
  delay(200);
  moc_setSpeed(motor[cur].moc, 75);
  delay(200);
  moc_setSpeed(motor[cur].moc, 0);
  cur = (cur + 1) % 8;
}
