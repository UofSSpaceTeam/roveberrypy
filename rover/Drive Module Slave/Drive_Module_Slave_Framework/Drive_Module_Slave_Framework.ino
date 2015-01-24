//Framework for a drive module slave
  int stall_current; //current threshold for stalling
  int freespin_current; //current threshold for freespinning
  int master_spd_cntr[6]; //value obtained from drive module master for speed control
  int current_pins[6] = {1,2,3,4,5,6}; //analog pins for reading current from mc
  int m_write[6] = {1,2,3,4,5,6}; //digital output pins for controlling speed
  int m_current[6]; //motor's measured current
  int dir_pin[6] = {1,2,3,4,5,6};  //motor direction pins
  int forward = 1;  //pretty sure high on the dir pin is forward and low is reverse
  int reverse = 0;
  bool m_stall[6] = {0,0,0,0,0,0}; //stall state of motor
  bool m_freespin[6] = {0,0,0,0,0,0}; //freespin state of motor
  
void setup() 
{
  
}

void loop() 
{  
  
  for(int i = 0;i = 5; i++)
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
      analogWrite(m_write[i],master_spd_cntr);
  }
  else if(m_stall[i])
  {
    //puslate stalled wheels
      digitalWrite(dir_pin[i],forward);
      analogWrite(m_write,255);
      digitalWrite(dir_pin[i],reverse);
      analogWrite(m_write,255);
  }
  else if(m_freespin[i])
  {
      analogWrite(m_write[i],master_spd_cntr - 50);  
  }
  return
}

int getMotorCurrent(int wheel_num)
{
  //will probably need some math here...
  current = analogRead(current_pins[wheel_num]};
  return current;
}

