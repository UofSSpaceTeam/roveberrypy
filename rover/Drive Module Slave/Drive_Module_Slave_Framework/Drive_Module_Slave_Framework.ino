//Framework for a drive module slave
  #include <Wire.h>
  
  int stall_current; //current threshold for stalling
  int freespin_current; //current threshold for freespinning
  byte master_spd_cntr[6] = {0x00, 0x00, 0x00, 0x00, 0x00, 0x00}; //value obtained from drive module master for speed control
  byte spd_address = 7; //address for getting speed values //might be a different value
  byte spd_data[2] = {0x00, 0x00}; //intermediary array for target motor and speed values
  int current_pins[6] = {1,2,3,4,5,6}; //analog pins for reading current from mc
  int m_write[6] = {1,2,3,4,5,6}; //digital output pins for controlling speed
  int m_current[6]; //motor's measured current
  byte m_address[6] = {0x00, 0x00, 0x00, 0x00, 0x00, 0x00}; //motor's address
  int dir_pin[6] = {1,2,3,4,5,6};  //motor direction pins
  int forward = 1;  //pretty sure high on the dir pin is forward and low is reverse
  int reverse = 0;
  bool m_stall[6] = {0,0,0,0,0,0}; //stall state of motor
  bool m_freespin[6] = {0,0,0,0,0,0}; //freespin state of motor
  
void setup() 
{
  Wire.begin(spd_address);
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
    receiveData();
    master_spd_cntr[(int)spd_data[0]] = spd_data[1];
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

void receiveData()
{
  if (Wire.available())
  {
      spd_data[0] = Wire.read();
      spd_data[1] = Wire.read();
  }
}
