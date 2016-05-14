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

// Basic description of a motor controller's (moc) specifications
typedef struct {
	const uint_t ID;			// ID of the motor controller
	const uint_t PIN_PWM;	// Location of PWM pin
	const uint_t EXT_FB;		// Logical flag indicating external feedback
	const uint_t PIN_EXT_FB;	// Location of analog external feedback
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

#endif
