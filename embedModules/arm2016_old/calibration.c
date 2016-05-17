#include "motor.h"

#define N_SAMPLES 10
#define TIME_STEP 100
#define DUTY_CYCLE 100

int main() {
    MotorController* mc = motor;
    uint_t pos[N_SAMPLES];
    uint_t std[N_SAMPLES];
    uint_t i;

    for(i = 0; i < N_SAMPLES/2; ++i) {
        moc_setDirection(mc, FORWARD);
        moc_setSpeed(mc, DUTY_CYCLE);
    }

    while(1) {
        moc_setDirection(mc, FORWARD);
        moc_setSpeed(mc, 75);
        delay(200);
        moc_setSpeed(mc, 150);
        delay(200);
        moc_setSpeed(mc, 255);
        delay(200);
        moc_setSpeed(mc, 150);
        delay(200);
        moc_setSpeed(mc, 75);
        delay(200);
        moc_setSpeed(mc, 0);

        moc_setDirection(mc, REVERSE);
        moc_setSpeed(mc, 75);
        delay(200);
        moc_setSpeed(mc, 150);
        delay(200);
        moc_setSpeed(mc, 255);
        delay(200);
        moc_setSpeed(mc, 150);
        delay(200);
        moc_setSpeed(mc, 75);
        delay(200);
        moc_setSpeed(mc, 0);
        cur = (cur + 1) % 8;
    }
    return 0;
}
