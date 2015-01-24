//Framework for a drive module slave
  int stall_current; //current threshold for stalling
  int freespin_current; //current threshold for freespinning
  int value; //value obtained from drive module master for speed control
  int current_pin; //an analog input pin for reading current
  int pwm_pin; //a digital output pin for controlling speed
  int m_current; //motor's measured current
  bool m_stall = false; //stall state of motor
  bool m_freespin = false; //freespin state of motor
  //These variables can be copied for controlling multiple motors
void setup() {
}

void loop() {
  analogWrite(pwm_pin, value); //sets motor speed
  m_current = analogRead(current_pin); //reads current of motor
  //Checks for stalling via comparing current with a threshold
  if (m_current >= stall_current)
  {
    m_stall = true;
  }
  else
  {
    m_stall = false; //will only work if rechecks require a new loop; could use another threshold
  }                  //later in the loop to recheck 
  //Checks for freespinning via comparison with a threshold
  if (m_current <= freespin_current)
  {
    m_freespin = true;
  }
  else
  {
    m_freespin = false; //will only work if rechecks require a new loop; could use another threshold
  }                     //later in the loop to recheck
  //Deals with a stalled wheel
  if (m_stall = true)
  { //Go forwards and backwards to try and un-stall the wheel
    analogWrite(pwm_pin, 255); //will send '255' to 'IN A' pin on driver
    delay(100);
    analogWrite(pwm_pin, -255); //will really send '255' to 'In B' pin on driver
    //delay(100); //these 2 lines are for if we have to stop the wheel first
    //analogWrite(pwm_pin, 0);
  }
  //Deals with a freespinning wheel
  if (m_freespin = true)
  { //I honestly have no idea how to deal with this; this is just a rough idea
    analogWrite(pwm_pin, value - 50);
  }
}

