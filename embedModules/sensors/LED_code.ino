//Code to control the LED Driver MAX6977

int clk = 14 ; //Set pin as Clock
int din = 15 ; //Set pin as digital input
int le = 16 ; //Set pin as latch
int oe = 17 ; //Set pin as output enable (high forces high impedence, low causes to follow latch)

//boolean to control what to set each pin to
bool pinout[8] = {true, false, false, false, false, false, false, false} ;


void setup() {
  // put your setup code here, to run once:

  // set pins as output:
  pinMode(clk, OUTPUT) ;
  pinMode(din, OUTPUT) ;
  pinMode(le, OUTPUT) ;
  pinMode(oe, OUTPUT) ;
  digitalWrite(oe, LOW) ;
}

void loop() 
{
  // put your main code here, to run repeatedly 
    digitalWrite(le, LOW) ; // Set latch to zero
    
    for (int i = 7 ; i >= 0 ; i--) //outputs written backwards from pin 7 to pin 0.
    {
      //decide output based on boolean
      if (pinout[i] == true)
      {
          digitalWrite(din, HIGH) ;
      }
      else
      {
          digitalWrite(din, LOW) ;
      }
      //tick clock
      digitalWrite(clk, HIGH) ;
      digitalWrite(clk, LOW) ;
    }
    //tick latch once loop over
    digitalWrite(le, HIGH) ;
    digitalWrite(le, LOW) ;

    digitalWrite(oe, LOW) ;
    
}
