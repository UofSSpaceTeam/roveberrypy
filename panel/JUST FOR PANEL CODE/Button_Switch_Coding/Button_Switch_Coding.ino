int inPin[] = {2,3,4,5,6,7,8,9};
int newstate;
const int pinCount = 8;
int state[pinCount];
int thisPin = 0;

void setup() {
  for (int i = 0; i < pinCount; i++)
  {
    pinMode(inPin[i],INPUT_PULLUP);
  }
  Serial.begin(9600);
}

void loop() {
  for(int i = 0; i < pinCount; i++)
  {
    int reading = digitalRead(inPin[i]);
    if (reading == HIGH)
    {
      newstate = 0;
    }
    else
    {
      newstate = 1;
    }
    if (newstate != state[i])
    {
      delay(100);
      Serial.print("Switch: ");
      Serial.print(i+1);
      Serial.print (" ");
      Serial.println(newstate);
      Serial.println("===============");
      state[i] = newstate;
    } 
  }
}
