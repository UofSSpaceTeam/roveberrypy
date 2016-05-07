#ifndef __MOTOR_H__
#define __MOTOR_H__

#include "moc.h"
#define EXTERNAL_FB 1
#define INTERNAL_FB 0
#define INVALID_U (1 << (8*sizeof(uint_t)-1))-1

enum EDirection {
    REVERSE,
    FORWARD
};

typedef struct {
    const MOC_SPEC const* moc;
	uint_t pos;
	uint_t velo;
    uint_t[2] calib_coeff;
    uint_t limit_lower;
    uint_t limit_upper;
    EDirection dir;
    uint_t duty_cycle;
} MotorController;

static const MOC_SPEC moc_spec[8];
moc_spec[0] = {0, -1, EXTERNAL_FB, -1, INVALID_U, INVALID_U};
moc_spec[1] = {1, -1, EXTERNAL_FB, -1, INVALID_U, INVALID_U};
moc_spec[2] = {2, -1, INTERNAL_FB, -1, 15, 0};
moc_spec[3] = {3, -1, INTERNAL_FB, -1, 15, 0};
moc_spec[4] = {4, -1, INTERNAL_FB, -1, 15, 0};
moc_spec[5] = {5, -1, INTERNAL_FB, -1, 15, 0};
moc_spec[6] = {6, -1, INTERNAL_FB, -1, 15, 0};
moc_spec[7] = {7, -1, INTERNAL_FB, -1, 15, 0};

static MotorController motor[8];
motor[0] = {moc_spec, INVALID_U, INVALID_U, {INVALID_U, INVALID_U}, 0, 100, FORWARD, 0};
motor[1] = {moc_spec + 1, INVALID_U, INVALID_U, {INVALID_U, INVALID_U}, 0, 100, FORWARD, 0};
motor[2] = {moc_spec + 2, INVALID_U, INVALID_U, {INVALID_U, INVALID_U}, 0, 100, FORWARD, 0};
motor[3] = {moc_spec + 3, INVALID_U, INVALID_U, {INVALID_U, INVALID_U}, 0, 100, FORWARD, 0};
motor[4] = {moc_spec + 4, INVALID_U, INVALID_U, {INVALID_U, INVALID_U}, 0, 100, FORWARD, 0};
motor[5] = {moc_spec + 5, INVALID_U, INVALID_U, {INVALID_U, INVALID_U}, 0, 100, FORWARD, 0};
motor[6] = {moc_spec + 6, INVALID_U, INVALID_U, {INVALID_U, INVALID_U}, 0, 100, FORWARD, 0};
motor[7] = {moc_spec + 7, INVALID_U, INVALID_U, {INVALID_U, INVALID_U}, 0, 100, FORWARD, 0};


#endif
