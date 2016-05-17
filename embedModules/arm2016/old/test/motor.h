//#ifndef __MOTOR_H__
//#define __MOTOR_H__
//
//#include "moc.h"
//
//enum EDirection {
//    REVERSE,
//    FORWARD
//};
//
//typedef struct {
//    const MOC_SPEC* moc;
//	uint_t pos;
//	uint_t velo;
//    uint_t calib_coeff[2];
//    uint_t limit_lower;
//    uint_t limit_upper;
//    EDirection dir;
//    uint_t duty_cycle;
//} MotorController;
//
//static MotorController motor[] = {
//    {moc_spec    , INVALID_U, INVALID_U, {INVALID_U, INVALID_U}, INVALID_U, INVALID_U, FORWARD, 0},
//    {moc_spec + 1, INVALID_U, INVALID_U, {INVALID_U, INVALID_U}, INVALID_U, INVALID_U, FORWARD, 0},
//    {moc_spec + 2, INVALID_U, INVALID_U, {INVALID_U, INVALID_U}, INVALID_U, INVALID_U, FORWARD, 0},
//    {moc_spec + 3, INVALID_U, INVALID_U, {INVALID_U, INVALID_U}, INVALID_U, INVALID_U, FORWARD, 0},
//    {moc_spec + 4, INVALID_U, INVALID_U, {INVALID_U, INVALID_U}, INVALID_U, INVALID_U, FORWARD, 0},
//    {moc_spec + 5, INVALID_U, INVALID_U, {INVALID_U, INVALID_U}, INVALID_U, INVALID_U, FORWARD, 0},
//    {moc_spec + 6, INVALID_U, INVALID_U, {INVALID_U, INVALID_U}, INVALID_U, INVALID_U, FORWARD, 0},
//    {moc_spec + 7, INVALID_U, INVALID_U, {INVALID_U, INVALID_U}, INVALID_U, INVALID_U, FORWARD, 0},
//};
//
//void moc_initializePins() {
//     pinMode(_MOCHI_SEL[0],     OUTPUT);
//     pinMode(_MOCHI_SEL[1],     OUTPUT);
//     pinMode(_MOCHI_SEL[2],     OUTPUT);
//     pinMode(_MOCHI_DAT,        OUTPUT);
//     pinMode(_MOCHI_WRT,        OUTPUT);
//     pinMode(_MOCHI_CSEL[0],    OUTPUT);
//     pinMode(_MOCHI_CSEL[1],    OUTPUT);
//     pinMode(_MOCHI_CSEL[2],    OUTPUT);
//     pinMode(_MOCHI_CSEL[3],    OUTPUT);
//     pinMode(_MOCHI_CRD,        INPUT);
//     pinMode(_MOCHI_CRST,       OUTPUT);
//     for(uint_t i = 0; i < 8; ++i) {
//         pinMode(moc_spec[i].PIN_PWM, OUTPUT);
//         moc_setSpeed(moc_spec + i, 0);
//         if (moc_spec[i].EXT_FB) {
//            pinMode(moc_spec[i].PIN_EXT_FB, INPUT);
//        }
//     }
//     _MOCHI_CURMOC = INVALID_U;
//}
//
//#endif
