#include <TinyGPS.h>

TinyGPS gps;

float lat, lon, speed, heading;
unsigned long fix_age;

void setup()
{
	Serial1.begin(9600); // GPS + pi
	Serial.begin(9600);
}

void loop()
{	
	while(Serial1.available())
	{
		if(gps.encode(Serial1.read()))
		{
			gps.f_get_position(&lat, &lon, &fix_age);
			speed = gps.f_speed_mps();
			heading = gps.f_course();
			Serial1.print("@");
			Serial1.print(lat, 8);
			Serial1.print(",");
			Serial1.print(lon, 8);
			Serial1.print(",");
			Serial1.print(speed, 4);
			Serial1.print(",");
			Serial1.print(heading, 3);
			Serial1.print("$");
			
			Serial.println("update");
		}
	}
}

