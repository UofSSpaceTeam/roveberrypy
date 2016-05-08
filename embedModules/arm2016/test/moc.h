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

#define EXTERNAL_FB 1
#define INTERNAL_FB 0
#define INVALID_U ((uint_t) -1)

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
void moc_select(const MOC_SPEC * moc);

/// Set the direction of the given motor controller
// @param moc The motor controller to be modified
// @param dir The direction to write to the motor controller
void moc_setDirection(const MOC_SPEC * moc, uint_t dir);

// Set the duty cycle to the given motor modified
// @param moc The motor controller to be selected
// @param dc The duty cycle to set
void moc_setSpeed(const MOC_SPEC * moc, uint_t dc);

// Read the position of the auxillary connected to the given motor controller
// @param moc The associated motor controller
uint_t moc_readPosition(const MOC_SPEC * moc);

// Reset the internal feedback for the given motor controller
// @param moc The motor controller to be modified
void moc_resetCount(const MOC_SPEC * moc);


///////////////////////////////////////////////////////////////////////////////
//					Implementation
///////////////////////////////////////////////////////////////////////////////

uint_t _MOCHI_CURMOC = 9;

void moc_select(const MOC_SPEC * moc) {
	uint_t i, sel;
	// Check if `moc is already the current motor controller
	if(_MOCHI_CURMOC == moc->ID)
		return;
	// Write the ID of `moc to the select bits
	for(i = 0; i < 3; ++i){
		sel = moc->ID & 1 << i;
    if(sel > 0) {
		  digitalWriteFast(_MOCHI_SEL[i], HIGH);
    } else {
      digitalWriteFast(_MOCHI_SEL[i], LOW);
    }
	}
	// Record the current motor controller and delay to guarantee valid access
	_MOCHI_CURMOC = moc->ID;
	delayMicroseconds(_MOCHI_DELAY_US);
}

void moc_setDirection(const MOC_SPEC * moc, uint_t dir) {
	moc_select(moc);
	// Write dir to data bit
  if(dir > 0) {
	  digitalWriteFast(_MOCHI_DAT, HIGH);
    Serial.println("Writing data HIGH");
  } else {
    digitalWriteFast(_MOCHI_DAT, LOW);
    Serial.println("Writing data LOW");
  }
	// Write the data bit motor controller registers
	digitalWriteFast(_MOCHI_WRT, HIGH);
 delayMicroseconds(_MOCHI_DELAY_US);
	digitalWriteFast(_MOCHI_WRT, LOW);
}

void moc_setSpeed(const MOC_SPEC * moc, uint_t dc) {
	// Set the duty cycle
	analogWrite(moc->PIN_PWM, 255 - dc);
}

uint_t _moc_readExtFb(const MOC_SPEC * moc){
	return (uint_t) analogRead(moc->PIN_EXT_FB);
}

uint_t _moc_readIntFb(const MOC_SPEC * moc) {
	uint_t i, j, msb, lsb, count;
	moc_select(moc);
	// Loop through [`msb:`lsb] and write bits to `count
	msb = moc->IFB_MSB;
	lsb = moc->IFB_LSB;
	count = 0;
	for(i = msb; i >= lsb; --i){
		// Select bit `i and then delay to guarantee valid access
		for(j = 0; j < 4; ++j)
			digitalWriteFast(_MOCHI_CSEL[j], i & 1 << j);
		delayMicroseconds(_MOCHI_DELAY_US);
		// Write the bit `i of `count
		count |= digitalReadFast(_MOCHI_CRD) << i;
	}
	return count;
}

uint_t moc_readPosition(const MOC_SPEC * moc) {
	if(moc->EXT_FB)
		return _moc_readExtFb(moc);
	else
		return _moc_readIntFb(moc);
}

void moc_resetCount(const MOC_SPEC * moc) {
	// If `moc uses external feedback then do nothing
	if(moc->EXT_FB)
		return;
	moc_select(moc);
	// Write to internal count reset bit
	digitalWriteFast(_MOCHI_CRST, 1);
	delayMicroseconds(_MOCHI_DELAY_US);
	digitalWriteFast(_MOCHI_CRST, 0);
}


#endif
