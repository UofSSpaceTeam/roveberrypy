// USST Rover 2015 - Manual Laser Test
// Use serial command line to turn lasers on and off
// Gaelene Lerat
// Last Updated May 13th, 2015

// digital pins for laser output
int laser980_pin = 5;
int laser1310_pin = 4;
int laser1550_pin = 6;

void setup() {
  // digital pin mode as output
  pinMode(laser980_pin, OUTPUT);
  pinMode(laser1310_pin, OUTPUT);
  pinMode(laser1550_pin, OUTPUT);
  
  // initial states all lasers off
  digitalWrite(laser980_pin, HIGH);
  delay(1000); 
  digitalWrite(laser1310_pin, LOW);
  delay(1000); 
  digitalWrite(laser1550_pin, LOW);
  delay(1000); 
  
  // serial setup, blah blah blah
  Serial.begin(9600);
  while (! Serial); // wait until serial is ready (important for micro)
  Serial.println("Get Ready to do some SCIENCE"); // message because improving morale is important
  Serial.println("Enter Laser Number:");
  Serial.println("'0' = 980nm");
  Serial.println("'1' = 1310nm");
  Serial.println("'2' = 1550nm");
  Serial.println("'x' = clear all");
  Serial.println("Remember to clear before any power off");
  Serial.println("because sensitive laser is sensitive");
}

void loop() {
  if (Serial.available())
  {
    char ch = Serial.read();
    if (ch == '0')
    {
      digitalWrite(laser980_pin, LOW);
      delay(1000);  // delay for slow start laser to turn on  
      Serial.println("Firing 980nm");
    }
    if (ch == '1')
    {
      digitalWrite(laser1310_pin, HIGH);
      delay(1000);  // delay for slow start laser to turn on  
      Serial.println("Firing 1310nm");
    }
    if (ch == '2')
    {
      digitalWrite(laser1550_pin, HIGH);
      delay(1000);  // delay for slow start laser to turn on  
      Serial.println("Firing 1550nm");
    }
    if (ch == 'x')
    {
      digitalWrite(laser980_pin, HIGH);
      delay(1000); 
      digitalWrite(laser1310_pin, LOW);
      delay(1000); 
      digitalWrite(laser1550_pin, LOW);
      delay(1000); 
      Serial.println("ALL OFF");
    }
  }

}
