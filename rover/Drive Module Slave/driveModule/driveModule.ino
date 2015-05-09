// Code for the Arduino controlling the motor drivers.
// Written for Arduino Micro.

#include <Wire.h>

#define TIMEOUT 750
#define PULSE_TIME 30

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
	All A and B are connected together on each side,
	PWM and CS are per-motor
*/
const byte m_a[] = {7,8,7,8,7,8}; // direction input #1
const byte m_b[] = {4,12,4,12,4,12}; // direction input #2
const byte m_pwm[] = {13,11,10,9,6,5}; // throttle
const byte m_cs[] = {0,1,2,3,4,5}; // current sensing

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
unsigned long timeout;
volatile command cmd;
byte* cmd_ptr = (byte*)(&cmd);
volatile byte cmd_count = 0;
volatile bool new_cmd = false;
volatile bool stall_enable = true; // anti-stall enable/disable
volatile bool spin_enable = true; // anti-wheelspin enable/disable
volatile bool pulseHigh = true; //for stalled motor pulsing
unsigned long prevTime; // for stalled motor pulsing


// function prototypes

// Interrupt handler for receiving a byte via I2C
void receiveEvent(int count);

// function to actually process command
void processCommand();

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
	for(int i = 0; i < sizeof(command); i++)
		cmd_ptr[i] = 0x00;
	
	// arm timeout
	timeout = millis();
        prevTime = millis();
}

void loop()
{
	if(new_cmd)
	{
		processCommand();
		new_cmd = false;
	}
	for(int i = 0; i < 6; i++)
	{	
		getMotorStates(); // update the motor states
		
		if(stall_enable && m_state[i] == STALL)
		{
			// stall handling logic
			//pulse motor
                        int currTime = millis();
                        if(currTime - prevTime >= PULSE_TIME){
                          prevTime = currTime;
                          if(pulseHigh) {
                            //turn m[i] off
                            m_cmd[i] = 0;
                            pulseHigh = false;
                          } else {
                            //don't modify m[i]
                            pulseHigh = true;
                          }
                        }
                          
		}
		
		if(spin_enable && m_state[i] == SPIN)
		{
			// spin handling logic
			m_cmd[i] /= 5;
		}
		
		setMotor(i, m_cmd[i]);
		
		if(millis() - timeout > TIMEOUT)
		{
			Serial.println("TO");
			stopAll();
			timeout = millis();
		}
	}
}

void receiveEvent(int count)
{
	byte in;
	
	if(new_cmd == true)
		return;
	
	while(Wire.available())
	{
		in = Wire.read();
		// wait for header
		if(!cmd_count)
		{
			if(in == CMD_HEADER)
			{
				*cmd_ptr = in;
				cmd_count++;
			}
			continue;
		}
		
		// add middle bytes
		if(cmd_count < sizeof(command))
		{
			cmd_ptr[cmd_count] = in;
			cmd_count++;
		}
		
		// check for complete
		if(cmd_count == sizeof(command))
		{
			if(in == CMD_TRAILER)
			{
				byte csum = cmd.type + cmd.d1 + cmd.d2;
				if(csum == cmd.csum)
					new_cmd = true;
			}
			cmd_count = 0;
		}
	}
}

void processCommand()
{
	// Serial.println("got command");
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
		// Serial.print(cmd.d1);
		// Serial.print(" ");
		// Serial.println(cmd.d2);
		if(cmd.d1 > 255 || cmd.d1 < -255)
			break;
		if(cmd.d2 > 255 || cmd.d2 < -255)
			break;
		m_cmd[1] = cmd.d1;
		m_cmd[3] = cmd.d1;
		m_cmd[5] = cmd.d1;
		m_cmd[0] = cmd.d2;
		m_cmd[2] = cmd.d2;
		m_cmd[4] = cmd.d2;
		timeout = millis();
		break;
		
		case SET_MOTOR:
		if(cmd.d1 < 0 || cmd.d1 > 5)
			break;
		if(cmd.d2 < -255 || cmd.d2 > 255)
			break;
		m_cmd[cmd.d1] = cmd.d2;
		timeout = millis();
		break;
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
		m_power[index] = 0;
		return;
	}
	
	if(index % 2) // left side motor, reverse direction
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
	
	m_power[index] = abs(value);
	analogWrite(m_pwm[index], m_power[index]);
	// Serial.print(index + 1);
	// Serial.print(": ");
	// Serial.println(m_power[index]);
}

void stopAll()
{
	// Serial.println("stopped");
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


