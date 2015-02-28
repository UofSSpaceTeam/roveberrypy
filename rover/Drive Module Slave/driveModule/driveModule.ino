// Code for the Arduino controlling the motor drivers.
// Written for Arduino Micro.

#include <Wire.h>

// definition of structures and enums

enum command_type // instructions from the Pi
{
	STOP, // stop all motors
	STALL_ENABLE, // enable/disable antistall
	SPIN_ENABLE, // enable / disable antispin
	SET_SPEED, // set desired speed for left / right sides
	SET_MOTOR // set desired speed for individual motor
};

typedef struct
{	
	byte header;
	byte type; // actually used as enum command_type, that's ok
	short d1; // 16-bit signed
	short d2;
	byte csum; // sum of cmd_type, d1, d2
	byte trailer;
} command;

enum motor_state // describes possible states of motors
{
	OK,
	STALL,
	SPIN
};

/*
	Wiring connections.
	Note: motors 0-2 are left side, 3-5 are right side.
	All A and B are connected together on each side,
	PWM and CS are per-motor
*/
const byte m_a[] = {0, 1}; // direction input #1
const byte m_b[] = {4, 7}; // direction input #2
const byte m_pwm[] = {5, 6, 9, 10, 11, 13}; // throttle
const byte m_cs[] = {A0, A1, A2, A3, A4, A5}; // current sensing

// arduino address on bus
const byte i2c_address = 0x07;

// traction control data
const int stall_thresh = 1024; // current threshold for stall detection
const float spin_factor = 0.5; // power-relative wheelspin threshold
motor_state m_state[] = {OK, OK, OK, OK, OK, OK}; // current state
short m_power[] = {0, 0, 0, 0, 0, 0}; // current power / direction applied
volatile short m_cmd[] = {0, 0, 0, 0, 0, 0}; // commanded speed commanded

// state information
const byte CMD_HEADER = 0xF7;
const byte CMD_TRAILER = 0xF8;
volatile command cmd;
volatile bool stall_enable = true; // anti-stall enable/disable
volatile bool spin_enable = true; // anti-wheelspin enable/disable


// function prototypes

// Interrupt handler for receiving a byte via I2C
void receiveEvent(int count);

// Could be used to send data to the Pi, watch out for 5v <-> 3.3v issues
void requestEvent();

/*
	sets a single motor to the specified direction and power level.
	index: which motor, [0, 5]
	value: speed and direction, [-255, 255]
*/
void setMotor(byte index, short value);

// stops all motors.
void stopAll();

/*
	updates the state of all motors.
	results are written to m_state array.
*/
void getMotorStates();


// functions

void setup() 
{
	Serial.begin(9600); // debug
	Wire.begin(i2c_address);
	Wire.onReceive(receiveEvent);
	Wire.onRequest(requestEvent);
	
	// initialize outputs
	for(int i = 0; i < 6; i++)
	{
		pinMode(m_a[i], OUTPUT);
		pinMode(m_b[i], OUTPUT);
		pinMode(m_pwm[i], OUTPUT);
	}
	stopAll();
	
	// clear cmd struct
	volatile byte* cmd_ptr = (volatile byte*)&cmd;
	for(int i = 0; i < sizeof(command); i++)
		cmd_ptr[i] = 0x00;
}

void loop()
{
	for(int i = 0; i < 6; i++)
	{	
		getMotorStates(); // update the motor states
		
		if(stall_enable && m_state[i] == STALL)
		{
			// stall handling logic
			;
		}
		
		if(spin_enable && m_state[i] == SPIN)
		{
			// spin handling logic
			;
		}
		
		setMotor(i, m_cmd[i]);
	}
}

void receiveEvent(int count)
{
	// process ALL the bytes
	for(int i = 0; i < count; i++)
	{
		byte* cmd_ptr = (byte*)&cmd;
		// shift new byte in
		for(int j = 0; j < sizeof(command) - 1; j++)
			cmd_ptr[j] = cmd_ptr[j + 1];
		cmd_ptr[sizeof(command) - 1] = Wire.read();
		
		Serial.println(cmd_ptr[sizeof(command) - 1]); // debug
		
		// check for complete packet
		if(cmd.header == CMD_HEADER && cmd.trailer == CMD_TRAILER)
		{
			// verify checksum
			byte csum = cmd.type + cmd.d1 + cmd.d2;
			if(csum != cmd.csum)
			{
				Serial.println("bad checksum"); // debug
				return;
			}
			Serial.println("got packet");
			
			switch(cmd.type)
			{
				case STOP:
				stopAll();
				break;
				
				case STALL_ENABLE:
				if(cmd.d1 == 0)
					stall_enable = false;
				else if(cmd.d1 == 1)
					stall_enable = true;
				break;
				
				case SPIN_ENABLE:
				if(cmd.d1 == 0)
					spin_enable = false;
				else if(cmd.d1 == 1)
					spin_enable = true;
				break;
				
				case SET_SPEED:
				if(cmd.d1 > 255 || cmd.d1 < -255)
					break;
				if(cmd.d2 > 255 || cmd.d2 < -255)
					break;
				m_cmd[0] = cmd.d1;
				m_cmd[1] = cmd.d1;
				m_cmd[2] = cmd.d1;
				m_cmd[3] = cmd.d2;
				m_cmd[4] = cmd.d2;
				m_cmd[5] = cmd.d2;
				break;
				
				case SET_MOTOR:
				if(cmd.d1 < 0 || cmd.d1 > 5)
					break;
				if(cmd.d2 < -255 || cmd.d2 > 255)
					break;
				m_cmd[cmd.d1] = cmd.d2;
				break;
			}
		}
	}
}

void requestEvent()
{
	return;
}

void setMotor(byte index, short value)
{
	if(value == 0) // stop
	{
		digitalWrite(m_pwm[index], LOW);
		digitalWrite(m_a[index], LOW);
		digitalWrite(m_b[index], LOW);
		m_power[index] = 0;
		return;
	}
	
	if(index < 3) // left side motor, reverse direction
		value = -value;
	
	if(value > 0) // forwards
	{
	
		digitalWrite(m_a[index], LOW);
		digitalWrite(m_b[index], HIGH);
	}
	else
	{
		digitalWrite(m_a[index], HIGH);
		digitalWrite(m_b[index], LOW);
	}
	
	m_power[index] = constrain(abs(value), 0, 255);
	digitalWrite(m_pwm[index], m_power[index]);
}

void stopAll()
{
	for(int i = 0; i < 6; i++)
	{
		digitalWrite(m_pwm[i], LOW);
		digitalWrite(m_a[i], LOW);
		digitalWrite(m_b[i], LOW);
		m_power[i] = 0;
		m_cmd[i] = 0;
	}
}

void getMotorStates()
{
	int reading, spin_thresh;
	
	for(int i = 0; i < 6; i++)
		m_state[i] = OK;
	
	for(int i = 0; i < 6; i++)
	{		
		reading = analogRead(m_cs[i]);
		if(stall_enable) // detect stall condition
		{
			if(reading > stall_thresh)
			{
				m_state[i] = STALL;
				continue;
			}
		}
		if(spin_enable) // detect spin condition
		{
			spin_thresh = (int)(m_power[i] * spin_factor);
			if(reading < spin_thresh)
				m_state[i] = SPIN;
		}
	}
}

