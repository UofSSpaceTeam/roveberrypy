////////////////////////////////////////////////////////////////////////////////
// File: 	moc.c
// Author: 	Liam Bindle <liam.bindle@gmail.com>
// Date:	April 21, 2016
// Status:	*Untested*
//
// This file provides the Arduino implementation for motor low-level motor
// controller functionality for the robotic arm controller board designed by
// Carl Hofmeiser and Liam Bindle for the USST.
////////////////////////////////////////////////////////////////////////////////
#include "moc.h"
#include "moc_hi.h"

uint_t _MOCHI_CURMOC = _MOCHI_MAX_ID + 1;

void moc_select(const MOC_SPEC *const moc) {
	uint_t i, sel;
	// Check if `moc is already the current motor controller
	if(_MOCHI_CURMOC == moc->ID)
		return;
	// Write the ID of `moc to the select bits
	for(i = 0; i < 3; ++i){
		sel = moc->ID & 1 << i;
		digitalWrite(_MOCHI_SEL[i], sel);
	}
	// Record the current motor controller and delay to guarantee valid access
	_MOCHI_CURMOC = moc->ID;
	delayMicroseconds(_MOCHI_PROPDELAY_MOC_SELECT);
}

void moc_setDirection(const MOC_SPEC *const moc, uint_t dir) {
	moc_select(moc);
	// Write dir to data bit
	digitalWrite(_MOCHI_DAT, dir);
	// Write the data bit motor controller registers
	digitalWrite(_MOCHI_WRT, 1);
	delayMicroseconds(_MOCHI_PROPDELAY_MOC_DATWRT);
	digitalWrite(_MOC_WRITE_PIN, 0);
}

void moc_setSpeed(const MOC_SPEC *const moc, uint_t dc) {
	// Set the duty cycle
	analogWrite(moc->PIN_PWM, dc);
}

uint_t _moc_readExtFb(const MOC_SPEC *const moc){
	uint_t i, wp, sum;
	// Get the pin of the attached external analog feedback pin
	wp = moc->PIN_EXT_FB;
	// Calculate the mean ADC reading
	sum = 0;
	for(i = 0; i < _MOCHI_EXTFB_NUMSAMPLES; ++i)
		sum += analogRead(wp);
	return sum/ADC_NUM_SAMPLES;
}

uint_t _moc_readIntFb(const MOC_SPEC *const moc) {
	uint_t i, j, val, msb, lsb, count;
	moc_select(moc);
	// Loop through [`msb:`lsb] and write bits to `count
	msb = moc->IFB_MSB;
	lsb = moc->IFB_LSB;
	count = 0;
	for(i = msb; i >= lsb; --i){
		// Select bit `i and then delay to guarantee valid access
		for(j = 0; j < 4; ++j)
			digitalWrite(_MOCHI_CSEL[j], i & 1 << j);
		delayMicroseconds(_MOCHI_PROPDELAY_MOC_CSELECT);
		// Write the bit `i of `count
		count |= digitalRead(_MOCHI_CRD) << i;
	}
	return count;
}

uint_t moc_readPosition(const MOC_SPEC *const moc) {
	if(moc->EXT_FB)
		return _moc_readExtFb(moc);
	else
		return _moc_readIntFb(moc);
}

void moc_resetCount(const MOC_SPEC *const moc) {
	// If `moc uses external feedback then do nothing
	if(moc->EXT_FB)
		return;
	moc_select(moc);
	// Write to internal count reset bit
	digitalWrite(_MOCHI_CRST, 1);
	delayMicroseconds(_MOCHI_PROPDELAY_MOC_RSTWRT);
	digitalWrite(_MOCHI_CRST, 0);
}

void moc_init(const MOC_SPEC *const moc) {
	moc_setDirection(moc, 0);
	moc_setSpeed(moc, 0);
	moc_resetCount(moc);
}
