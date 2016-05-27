int clk = 14 ; //Set digital pin 14 as clk
int din = 15 ;
int le = 16 ;
int oe = 17 ;
bool pins[8] = {true, true, true, true, true, true, true, true} ;


void setup() {
  // put your setup code here, to run once:

  // set pins as output:
  pinMode(clk, OUTPUT) ;
  pinMode(din, OUTPUT) ;
  pinMode(le, OUTPUT) ;
  pinMode(oe, OUTPUT) ;
}

void loop() {
  // put your main code here, to run repeatedly:
    digitalWrite(le, LOW) ;
  
    for (int i = 7 ; i => 0 ; i--){
      if (pins(i) = true){
          digitalWrite(din, HIGH) ;
      }
      else {
          digitalWrite(din, LOW) ;
      }
      digitalWrite(clk, HIGH) ;
      delay(1) ;
      digitalWrite(clk, LOW) ;
    }
    digitalWrite(le, HIGH) ;
  }
  
}
