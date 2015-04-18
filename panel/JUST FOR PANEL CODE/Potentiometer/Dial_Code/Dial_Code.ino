int potPin = A2;    // select the input pin for the potentiometer
int val = 1;       // variable to store the value coming from the sensor

void setup() {
  Serial.begin(9600);
}

void loop() {
  val = analogRead(potPin)+1;    // read the value from the sensor

  for(int i=1; i < 4 - log10(val); i++) 
  Serial.print('0'); 
  Serial.println(val,DEC);
}
