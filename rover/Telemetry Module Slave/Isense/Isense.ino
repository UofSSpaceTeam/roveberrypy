float Isense_raw;
float gain = 10.0/4.7;  //gain of amp
float offset_at_zero = 0.046;  //output of amp with zero current
float current;
int last_update=0;
int refresh_time=10;
int i_pin;  //current sense analog input pin
void setup() {
  

}

void loop() 
{
  if(millis()-last_update > refresh_time)
  {
    Isense_raw = analogRead(i_pin);
    current = (Isense_raw - offset_at_zero)*gain;
  }
  
}
