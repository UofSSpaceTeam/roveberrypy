//      Joystick.cpp
//      
//      Copyright 2009 Arnold G Werschky III <ag@7k6solutions.com>
//**********************************************************************
//Permission is hereby granted, free of charge, to any person
//obtaining a copy of this software and associated documentation
//files (the "Software"), to deal in the Software without
//restriction, including without limitation the rights to use,
//copy, modify, merge, publish, distribute, sublicense, and/or sell
//copies of the Software, and to permit persons to whom the
//Software is furnished to do so, subject to the following
//conditions:

//The above copyright notice and this permission notice shall be
//included in all copies or substantial portions of the Software.
//THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
//EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
//OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
//NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
//HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
//WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
//FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
//OTHER DEALINGS IN THE SOFTWARE.
//*********************************************************************
//include the class definition
#include "Joystick.h"

Joystick::Joystick(uint8_t upDownPin, uint8_t rightLeftPin, uint8_t deadzone){
    this->upDownAxisPin = upDownPin;
    this->rightLeftAxisPin = rightLeftPin;    
    dz = deadzone;
    state = 0;
}
void Joystick::setCenter(void)
{
    upDownAxisCenter = analogRead(upDownAxisPin);
    rightLeftAxisCenter = analogRead(rightLeftAxisPin);
}
bool Joystick::up(void)
{
    return uniquePress(upDownAxisPin, UPCURRENT, upDownAxisCenter, UPSIDE);
}
bool Joystick::down(void)
{
    return uniquePress(upDownAxisPin, DOWNCURRENT, upDownAxisCenter, DOWNSIDE);
}
bool Joystick::right(void)
{
    return uniquePress(rightLeftAxisPin, RIGHTCURRENT, rightLeftAxisCenter, RIGHTSIDE);
}
bool Joystick::left(void)
{
    return uniquePress(rightLeftAxisPin, LEFTCURRENT, rightLeftAxisCenter, LEFTSIDE);
}
int Joystick::upValue(void)
{
    return getMagnitude(upDownAxisPin, upDownAxisCenter, UPSIDE);
}
int Joystick::downValue(void)
{
    return getMagnitude(upDownAxisPin, upDownAxisCenter, DOWNSIDE);
}
int Joystick::rightValue(void)
{
    return getMagnitude(rightLeftAxisPin, rightLeftAxisCenter, RIGHTSIDE);
}
int Joystick::leftValue(void)
{
    return getMagnitude(rightLeftAxisPin, rightLeftAxisCenter, LEFTSIDE);
}
bool Joystick::uniquePress(uint8_t a, uint8_t bit, int c, bool s)
{
    if ((isPressed(a, bit, c, s)) && (!bitRead(state,(bit-1)))) return true;
    else return false;
}
int Joystick::getMagnitude(uint8_t a, int c, bool s)
{
    if (!s) return (-1 * (analogRead(a) - c));
    else return (analogRead(a) - c);
}
bool Joystick::isPressed(uint8_t a, uint8_t bit, int c, bool s)
{
    bitWrite(state,(bit-1),bitRead(state,bit));
    if ((getMagnitude(a,c,s)) > (dz/2)) 
    {
        bitWrite(state,bit,1);
        return true;
    }
    else
    {
        bitWrite(state,bit,0);
        return false;
    }
}

//20100101 - initial release
//20100104 - changed capitalization to be more compliant and happy








