#include "motor.h"


int main() {
    uint_t cur = 0;

    while(1) {
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
    return 0;
}
