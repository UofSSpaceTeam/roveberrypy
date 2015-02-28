#include <Wire.h>

//Framework for a drive module slave
int stall_current = 1000; //current threshold for stalling
int freespin_current = 0; //current threshold for freespinning
int master_spd_cntr[6] = {100,100,100,100,100,100}; //value obtained from drive module master for speed control
int motor_spd[6] = {0,0,0,0,0,0};
int current_pins[6] = {0,1,2,3,4,5}; //analog pins for reading current from mc
int m_write[6] = {13,11,10,9,6,5}; //digital output pins for controlling speed
int m_current[6]; //motor's measured current
int dir_pinA[6] = {4,8,4,8,4,8};  //motor forward direction pins
int dir_pinB[6] = {7,12,7,12,7,12}; //motor reverse direction pins
int forward = 1;  //pretty sure high on the dir pin is forward and low is reverse
int reverse = 0;
bool m_stall[6] = {0,0,0,0,0,0}; //stall state of motor
bool m_freespin[6] = {0,0,0,0,0,0}; //freespin state of motor
  
  
//Framework for I2C Communications
byte slave_address = 07;

// Motor sub-addresses for manual mode
const byte RF = 0xF1;
const byte RC = 0xF2;
const byte RR = 0xF3;
const byte LF = 0xF4;
const byte LC = 0xF5;
const byte LR = 0xF6;

// Commands
const byte STOP = 0xF7; 
const byte OS = 0xF8; //one-stick
const byte TS = 0xF9; //two-stick
const byte MAN = 0xF0; //manual mode
const byte A = 0xFA; //stick A
const byte B = 0xFB; //stick B

// Memory to process commands in interrupt
byte last = 0x00;
bool trac = true; //auto mode or manual
bool stickMode = true; //one stick or two
  
void setup() 
{
  //Serial.begin(9600);
  Wire.begin(slave_address);
  Wire.onReceive(receiveEvent);
  Wire.onRequest(requestEvent);
  
  //PWM Pins
  pinMode(13, OUTPUT); //M1
  pinMode(11, OUTPUT); //M2
  pinMode(10, OUTPUT); //M3
  pinMode(9, OUTPUT);  //M4
  pinMode(6, OUTPUT);  //M5
  pinMode(5, OUTPUT);  //M6
  
  //Direction Pins
  //Note that due to motor orientation, directions are opposite on the right side
  pinMode(12, OUTPUT); //LSB
  pinMode(8, OUTPUT);  //LSA
  pinMode(7, OUTPUT);  //RSA
  pinMode(4, OUTPUT);  //RSB
  
  //Current Sense Pins
  //Not Needed for setup
  // A0 = M1
  // A1 = M2
  // A2 = M3
  // A3 = M4
  // A4 = M4
  // A5 = M6
}

void loop() {  
  
  for(int i = 0; i < 6; i++)
  {
    //get all of the motor currents
    m_current[i] = getMotorCurrent(i); 
    //Checks for freespinning via comparison with a threshold
    if (m_current[i] >= stall_current)
      {
        m_stall[i] = true;
      }
    else
    {
      m_stall[i] = false; 
      //will only work if rechecks require a new loop; could use another threshold
      //later in the loop to recheck
    } 
      //Checks for freespinning via comparison with a threshold
    if (m_current[i] <= freespin_current)
    {
      m_freespin[i] = true;
    }
    else
    {
      m_freespin[i] = false; //will only work if rechecks require a new loop; could use another threshold
    }                     //later in the loop to recheck
    //set the motor speeds
    Serial.print("Sending speed to ");
    Serial.println(i);
    setMotorSpeed(i);
  }
}

// Interrupt called when the I2C bus receives a byte
// Most events are handled within the first few cases
void receiveEvent(int howMany){
  byte cmd = Wire.read();
  //Serial.println(cmd); // debug
  
  if(cmd == STOP){
    //send stop all signal to all motors
	return;
  }

  if(last == A){
        //send cmd to right side motors
        last = cmd;
        master_spd_cntr[0] = cmd;
        master_spd_cntr[2] = cmd;
        master_spd_cntr[4] = cmd;
        return;
  }
  
  if(last == B){
	//send cmd to left side motors;
        last = cmd;
        master_spd_cntr[1] = cmd;
        master_spd_cntr[3] = cmd;
        master_spd_cntr[5] = cmd;
        return;
  }
  
  //The rest of these commands are extra and generally will not be run
  //Not used at this time
  if(cmd == OS){
	stickMode = true;
        last = cmd;
        return;
  }
  //Not used at this time
  if(cmd == TS){
	stickMode = false;
        last = cmd;
        return;
  }
  
  if(cmd == MAN)
  {
	trac = !trac;
        last = cmd;
        return;
  }
  
  if(!trac)
  {
	if (last == RF){
	  //set the motor speed for RF directly
	  last = cmd;
          master_spd_cntr[0] = cmd;
          return;
	}
    if (last == RC){
	  //etc
	  last = cmd;
          master_spd_cntr[1] = cmd;
          return;
	}
	if (last == RR){
	  //etc
          last = cmd;
	  master_spd_cntr[2] = cmd;
          return;
	}
	if (last == LF){
	  //etc
          last = cmd;
	  master_spd_cntr[3] = cmd;
          return;
	}
	if (last == LC){
	  //etc
          last = cmd;
          master_spd_cntr[4] = cmd;
	  return;
	}
	if (last == LR){
	  //etc
          last = cmd;
          master_spd_cntr[5] = cmd;
	  return;
	}
    }
    last = cmd;
}

// This can be used to send current data or diagnostic data to the main controller
// Keep in mind, if we end up using a 5V controller with the Pi, this will not be possible
void requestEvent() {
  return;
}

void setMotorSpeed(int i)
{
  motor_spd[i] = master_spd_cntr[i]-100;
  if(motor_spd[i] > 0)
  {
    digitalWrite(dir_pinA[i], HIGH);
    digitalWrite(dir_pinB[i], LOW);
  }
  else
  {
    digitalWrite(dir_pinA[i], LOW);
    digitalWrite(dir_pinB[i], HIGH);
  }
  if(!m_stall[i] && !m_freespin[i])
  {
    //may need some math here to convert speed cmd to actual speed
    //also need to select direction
      analogWrite(m_write[i], abs(motor_spd[i]));
      Serial.println(motor_spd[i]);
  }
  /*else if(m_stall[i])
  {
    puslate stalled wheels
      digitalWrite(dir_pin[i],forward);
      analogWrite(m_write[i],255);
      digitalWrite(dir_pin[i],reverse);
      analogWrite(m_write[i],255);
  }
  else if(m_freespin[i])
  {
      analogWrite(m_write[i],master_spd_cntr[i] - 50);  
  }*/
}

int getMotorCurrent(int wheel_num)
{
  //will probably need some math here...
  int current = analogRead(current_pins[wheel_num]);
  return current;
}

