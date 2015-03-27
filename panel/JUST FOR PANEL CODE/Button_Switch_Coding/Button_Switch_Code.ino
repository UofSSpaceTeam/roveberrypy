//Pin Number: Button/Switch
//2: Switch 1
//3: Switch 2
//4: Switch 3
//5: Switch 4
//6:  Telemetry Control 1
//7:  Telemetry Control 2
//8:  Telemetry Control 3
//9:  Telemetry Control 4
//10: Telemetry Control 5
//11: Telemetry Control 6
//12: Timer
//13: GPS

int inPin[] = {2,7,8,9,10,11};
const int pinCount = 6;
int newstate;
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
      delay (50);
      int reading2 = digitalRead(inPin[i]);
      if (reading = reading2)
      {
        newstate = 0;
      }
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

