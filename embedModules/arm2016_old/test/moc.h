////////////////////////////////////////////////////////////////////////////////
// File: 	moc.h
// Author: 	Liam Bindle <liam.bindle@gmail.com>
// Date:	April 21, 2016
// Status:	*Untested*
//
// Declaration of low-level functionality provided for the USST(2016) robotic
// arm controller board designed by Carl Hofmeiser and Liam Bindle.
////////////////////////////////////////////////////////////////////////////////
#ifndef __MOC_H__
#define __MOC_H__

#include "moc_hi.h"
#include "Arduino.h"

// Basic description of a motor controller's (moc) specifications
typedef struct {
	const uint_t ID;		// ID of the motor controller
	const uint_t PIN_PWM;	// Location of PWM pin
	const uint_t EXT_FB;	// Logical flag indicating external feedback
	const uint_t PIN_EXT_FB;// Location of analog external feedback
	const uint_t IFB_MSB;	// MSB of internal feedback
	const uint_t IFB_LSB;	// LSB of internal feedback
} MOC_SPEC;

// Select the given motor controller
// @param moc The motor controller to be selected
void moc_select(const MOC_SPEC *const moc);

/// Set the direction of the given motor controller
// @param moc The motor controller to be modified
// @param dir The direction to write to the motor controller
void moc_setDirection(const MOC_SPEC *const moc, uint_t dir);

// Set the duty cycle to the given motor modified
// @param moc The motor controller to be selected
// @param dc The duty cycle to set
void moc_setSpeed(const MOC_SPEC *const moc, uint_t dc);

// Read the position of the auxillary connected to the given motor controller
// @param moc The associated motor controller
uint_t moc_readPosition(const MOC_SPEC *const moc);

// Reset the internal feedback for the given motor controller
// @param moc The motor controller to be modified
void moc_resetCount(const MOC_SPEC *const moc);

/// Initialize the given motor controller
// @param moc The motor controller to be initialized
void moc_init(const MOC_SPEC *const moc);


///////////////////////////////////////////////////////////////////////////////
//					Implementation
///////////////////////////////////////////////////////////////////////////////

uint_t _MOCHI_CURMOC;

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
	digitalWrite(_MOCHI_WRT, 0);
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
	return sum/_MOCHI_EXTFB_NUMSAMPLES;
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

#endif
