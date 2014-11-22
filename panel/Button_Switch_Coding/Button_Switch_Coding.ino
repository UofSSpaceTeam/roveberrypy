int inPinOne = 2;
int stateOne = 0;
int newstateOne;

void setup() {
  pinMode(inPinOne,INPUT_PULLUP);
  Serial.begin(9600);
}

void loop() {
  int readingOne = digitalRead(inPinOne);
  if (readingOne == HIGH)
  {
    newstateOne = 0;
  }
  else
  {
    newstateOne = 1;
  }
  if (newstateOne != stateOne)
  {
    delay(100);
    Serial.print("Switch One:");
    Serial.println(newstateOne);
    Serial.println("===============");
  }
  stateOne = newstateOne;
}
