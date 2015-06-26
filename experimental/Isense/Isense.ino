float Isense_raw;
float current;
float amp_gain = 10.0/4.7;
float sensor_sensitivity = 0.02;  // in V/A
float sensitivity = amp_gain*sensor_sensitivity;
int last_update=0;
int refresh_time=500;
int i_pin=0;  //current sense analog input pin
void setup() 
{
  Serial.begin(9600);

}

void loop() 
{
  if(millis()-last_update > refresh_time)
  {
    Isense_raw = analogRead(i_pin);
    Isense_raw = Isense_raw/1023*3.3;
    current = (Isense_raw)/sensitivity;
    Serial.println(current);
    last_update = millis();
  }
  
}
