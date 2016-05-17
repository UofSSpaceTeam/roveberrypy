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

// Configuration settings
#define _MOCHI_MAX_ID 8             // Maximum ID number of motor controllers
#define _MOCHI_EXTFB_NUMSAMPLES 5   // Number of sample when reading external
                                    // feedback
// Initial state description
#define _MOCHI_INIT_DIR 0           // Initial direction to set motor
                                    // controller's to

// Propogation delay constants to be used to guarantee valid i/o
#define _MOCHI_PROPDELAY_MOC_SELECT  100
#define _MOCHI_PROPDELAY_MOC_DATWRT  100
#define _MOCHI_PROPDELAY_MOC_CSELECT 50
#define _MOCHI_PROPDELAY_MOC_RSTWRT  100

// Pin definitions for hardware-interface with motor controller board
                                                        // Motor controller:
static const uint_t *const  _MOCHI_SEL  = {0, 0, 0};    // Select bits
static const uint_t         _MOCHI_DAT  = 0;            // Data bit
static const uint_t         _MOCHI_WRT  = 0;            // Write bit

                                                        // Internal feedback:
static const uint_t *const  _MOCHI_CSEL = {0, 0, 0, 0}; // IFB count select bits
static const uint_t         _MOCHI_CRD  = 0;            // Count data bit
static const uint_t         _MOCHI_CRST = 0;            // Count reset bit

#endif
