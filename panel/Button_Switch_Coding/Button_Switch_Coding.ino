int inPin = 1;
int state = 0;
int newstate;

void setup() {
  pinMode(inPin,INPUT_PULLUP);
  Serial.begin(9600);
}

void loop() {
  int reading = digitalRead(inPin);
  if (reading == HIGH)
  {
    newstate = 0;
  }
  else
  {
    newstate = 1;
  }
  if (newstate != state)
  {
    delay(100);
    Serial.print("Switch One:");
    Serial.println(newstate);
    Serial.println("===============");
  }
  state = newstate;
}
