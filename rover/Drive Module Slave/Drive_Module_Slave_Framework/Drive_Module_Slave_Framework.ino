#include <Wire.h>

//Framework for a drive module slave
int stall_current = 6; //current threshold for stalling
int freespin_current = 2; //current threshold for freespinning
int master_spd_cntr[6] = {0}; //value obtained from drive module master for speed control
int current_pins[6] = {1,2,3,4,5,6}; //analog pins for reading current from mc
int m_write[6] = {1,2,3,4,5,6}; //digital output pins for controlling speed
int m_current[6]; //motor's measured current
int dir_pin[6] = {1,2,3,4,5,6};  //motor direction pins
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
  
  //Probably want to call pinMode commands here as well
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

  else if(last == A){
	if(stickMode){
		//send cmd to all motors
                last = cmd;
                Serial.print("sent: ");
                Serial.print(cmd);
                Serial.println(" to all motors");
                return;
	}
	else{
		//send cmd to right side motors
		last = cmd;
                return;
	}
  }
  
  else if(last == B){
	//send cmd to left side motors;
        last = cmd;
        return;
  }
  
  //The rest of these commands are extra and generally will not be run
  if(cmd == OS){
	stickMode = true;
        last = cmd;
        return;
  }
  
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
          return;
	}
    if (last == RC){
	  //etc
	  last = cmd;
          return;
	}
	if (last == RR){
	  //etc
          last = cmd;
	  return;
	}
	if (last == LF){
	  //etc
          last = cmd;
	  return;
	}
	if (last == LC){
	  //etc
          last = cmd;
	  return;
	}
	if (last == LR){
	  //etc
          last = cmd;
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

void loop() 
{  
  
  for(int i = 0; i <= 5; i++)
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
    setMotorSpeed(i);
  }

}

void setMotorSpeed(int i)
{
  if(!m_stall[i] && !m_freespin[i])
  {
    //may need some math here to convert speed cmd to actual speed
    //also need to select direction
      analogWrite(m_write[i],master_spd_cntr[i]);
  }
  else if(m_stall[i])
  {
    //puslate stalled wheels
      digitalWrite(dir_pin[i],forward);
      analogWrite(m_write[i],255);
      digitalWrite(dir_pin[i],reverse);
      analogWrite(m_write[i],255);
  }
  else if(m_freespin[i])
  {
      analogWrite(m_write[i],master_spd_cntr[i] - 50);  
  }
}

int getMotorCurrent(int wheel_num)
{
  //will probably need some math here...
  int current = analogRead(current_pins[wheel_num]);
  return current;
}

