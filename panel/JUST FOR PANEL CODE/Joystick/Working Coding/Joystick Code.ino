int analogPin2 = 2; 
int analogPin0 = 0;    // potentiometer wiper (middle terminal) connected to analog pin 3
                       // outside leads to ground and +5V
int val2 = 0;
int val0 = 0;          // variable to store the value read

void setup()
{
  Serial.begin(9600);          //  setup serial
}

void loop()
{
  val2 = analogRead(analogPin2);    // read the input pin
  val0 = analogRead(analogPin0);

if (val2 > 700) {
  Serial.println("Up");
}
else if (val2 < 300) {
  Serial.println("Down");
}
else if (val0 > 800) {
  Serial.println("Right");
}
else if (val0 < 300) {
  Serial.println("Left");
}
else {
  Serial.println("Stationary");
}
}
