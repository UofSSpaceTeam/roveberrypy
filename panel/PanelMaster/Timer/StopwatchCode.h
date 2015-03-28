#define buttonPin 

int buttonState ;
int lastButtonState ;
long startTime ;
long elapsedTime ;

void setup ()
{
		
	serial.begin (9600) ;
	pinMode (buttonPin, INPUT) ;
	digitalWrite(buttonPin, HIGH) ;
	
}

void loop()
{
	buttonState - digitalRead(buttonPin) ;
	
	if (buttonState == LOW && lastButtonState == HIGH) {
		
		
		startTime = millis() ;
		
		delay (5) ;
		
		lastButtonState = buttonState ;
		
		
	}
	
	else if (buttonState == LOW && lastButtonState == HIGH) {
		
		
		elapsedTime = millis() - startTime ;
		
		lastButtonState = buttonState ;
		
		