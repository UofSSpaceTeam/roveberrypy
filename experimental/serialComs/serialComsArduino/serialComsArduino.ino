char startByte = '@';
char endByte = '~';
char escapeByte = '$';

char test(const char* message, int n)
{
  char sum = 0x00;
  for(int i = 0; i < n; i++)
  {
    sum ^= message[i];
  }
  return sum;
}

void messageSend(const char* message)
{ 
  Serial.print(startByte);
  Serial.print(message);
  Serial.print(endByte);
  Serial.print(test(message, strlen(message)));
}

char messageGet()
{
  boolean readMessage = false;
  boolean buffer = true;
  
  char messageBuffer[75] = "";
  
  while(buffer == true)
  {
    char chr = Serial.read(1);
    if(chr == startByte)
    {
      readMessage = true;
    }
    else if(chr == stopByte)
    {
      if(Serial.read(1) != test(messageBuffer, strlen(messageBuffer)))
      {
        messageBuffer = "-1";
      }
      buffer = false;
    }
    else
    {
      if(readMessage == true)
      {
        messageBuffer += chr;
      }
    }
  }
  
  return messageBuffer;
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly: 
  const char* message = "Hello My Name is Austin and the GPS is 101122wersdfs001121201";
  messageSend(message);
  
  delay(1000);
}
