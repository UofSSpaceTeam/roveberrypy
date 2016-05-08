////////////////////////////////////////////////////////////////////////////////
// File: 	moc.h
// Author: 	Liam Bindle <liam.bindle@gmail.com>
// Date:	April 21, 2016
// Status:	*Not finished*
//
// Definitions for hardware-interface with USST robotic arm board designed by
// Carl Hofmeiser and Liam Bindle for the USST.
////////////////////////////////////////////////////////////////////////////////
#ifndef __MOC_HI_H__
#define __MOC_HI_H__

// Propogation delay constants to be used to guarantee valid i/o
#define _MOCHI_DELAY_US  1000

// Unsigned int typede
typedef unsigned int uint_t;

// Pin definitions for hardware-interface with motor controller board
                                                        // Motor controller:
static const uint_t _MOCHI_SEL[]  = {0, 1, 2};   // Select bits
static const uint_t _MOCHI_DAT    = 13;            // Data bit
static const uint_t _MOCHI_WRT    = 15;            // Write bit

                                                        // Internal feedback:
static const uint_t _MOCHI_CSEL[] = {19, 18, 17, 16}; // IFB count select bits
static const uint_t _MOCHI_CRD    = 11;            // Count data bit
static const uint_t _MOCHI_CRST   = 26;            // Count reset bit

#endif
