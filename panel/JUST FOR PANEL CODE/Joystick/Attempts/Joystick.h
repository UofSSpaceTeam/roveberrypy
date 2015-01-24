
//      Joystick.h
//      
//      Copyright 2009 Arnold G Werschky III <ag@7k6solutions.com>
//
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

#ifndef JOYSTICK_H
#define JOYSTICK_H

#include "Arduino.h"

#define UPCURRENT 7
#define UPPREVIOUS 6
#define DOWNCURRENT 5
#define DOWNPREVIOUS 4
#define RIGHTCURRENT 3
#define RIGHTPREVIOUS 2
#define LEFTCURRENT 1
#define LEFTPREVIOUS 0
#define UPSIDE 1
#define DOWNSIDE 0
#define RIGHTSIDE 0
#define LEFTSIDE 1

class Joystick{
  public:
    Joystick(uint8_t upDownPin,uint8_t rightLeftPin, uint8_t deadzone);
    bool up();
    bool down();
    bool right();
    bool left();
    void setCenter();
    int upValue();
    int downValue();
    int rightValue();
    int leftValue();
  private:
    bool isPressed(uint8_t a, uint8_t bit, int c, bool s);
    bool uniquePress(uint8_t a, uint8_t bit, int c, bool s);
    int getMagnitude(uint8_t a, int c, bool s);
    int rightLeftAxisCenter;    //center value of the joystick
    int upDownAxisCenter;       //center value of the joystick
    uint8_t upDownAxisPin;      //pin that updown axis is analogread on
    uint8_t rightLeftAxisPin;   //pin that rightleft axis is analogread on
    uint8_t dz;                  //deadzone value (this val is divided by 2 -- 1/2 on each side) 
    
    uint8_t state;
};

#endif
//20100101 - initial release
//20100104 - changed capitalization to be more compliant and happy



