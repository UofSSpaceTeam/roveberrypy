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

// Not working.. I don't know what this is??
/*int messageGet(char * ptr)
{
  bool read = false;
  bool buffer = true;
  int len = 0;
  while(buffer)
  {
    if(Serial.available() > 0)
    {
      char msg = Serial.read();
      if(msg == startByte)
      {
        Serial.println("start");
        read = true;
        int len = (Serial.read() - '0')*10 + (Serial.read() - '0');
        Serial.println(len);
        ptr = new char[len];
      }
      else if(msg == endByte)
      {
        Serial.println("end");
        buffer = false;
      }
      else
      {
        if(read)
        {
          Serial.println("read");
          char buf = Serial.read();
          strcat(ptr, &buf);
        }
      }   
    }
  }
  Serial.println(ptr);
  return len;
}*/

void messageSend(char* message)
{ 
  Serial.print(startByte);
  Serial.print(strlen(message));
  Serial.print(message);
  Serial.print(endByte);
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly: 
  messageSend("Hello World");
}
