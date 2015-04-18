##import serial - not needed

#import the raw values from Arduino
#sample line below
code = "$0,0,0,0,0,0,0,0,0,0,0,0, ,S,0001,0001,0001&"

#remove the $ and & symbols from the line
code = code.strip("$")
code = code.strip("&")

#separate the values
code_list = code.split(',')

#group the values for the same devices
button1 = code_list[0]
button2 = code_list[1]
button3 = code_list[2]
button4 = code_list[3]
button5 = code_list[4]
button6 = code_list[5]
button7 = code_list[6]
button8 = code_list[7]
button9 = code_list[8]
button10 = code_list[9]
button11 = code_list[10]
button12 = code_list[11]
keypad = code_list[12]
joystick = code_list[13]
dial1 = code_list[14]
dial2 = code_list[15]
dial3 = code_list[16]

#convert the values to more usable values
#buttons
if button1 == "0":
	BU1 = "not pressed"
else:
	BU1 = "pressed"
if button2 == "0":
	BU2 = "not pressed"
else:
	BU2 = "pressed"
if button3 == "0":
	BU3 = "not pressed"
else:
	BU3 = "pressed"
if button4 == "0":
	BU4 = "not pressed"
else:
	BU4 = "pressed"
if button5 == "0":
	BU5 = "not pressed"
else:
	BU5 = "pressed"
if button6 == "0":
	BU6 = "not pressed"
else:
	BU6 = "pressed"
if button7 == "0":
	BU7 = "not pressed"
else:
	BU7 = "pressed"
if button8 == "0":
	BU8 = "not pressed"
else:
	BU8 = "pressed"
if button9 == "0":
	BU9 = "not pressed"
else:
	BU9 = "pressed"
if button10 == "0":
	BU10 = "not pressed"
else:
	BU10 = "pressed"
if button11 == "0":
	BU11 = "not pressed"
else:
	BU11 = "pressed"
if button12 == "0":
	BU12 = "not pressed"
else:
	BU12 = "pressed"

#keypad
if keypad == " ":
	KP = "idle"
else:
	KP = keypad
	
#joystick	
if joystick == "S":
	JS = "stationary"
elif joystick == "U":
	JS = "up"
elif joystick == "D":
	JS = "down"
elif joystick == "L":
	JS = "left"
elif joystick == "R":
	JS = "right"
else:
	JS = "not responding"
	
#dials
D1 = int(dial1) - 0001
D2 = int(dial2) - 0001
D3 = int(dial3) - 0001

#display values
print("Button 1 is", BU1)
print("Button 2 is", BU2)
print("Button 3 is", BU3)
print("Button 4 is", BU4)
print("Button 5 is", BU5)
print("Button 6 is", BU6)
print("Button 7 is", BU7)
print("Button 8 is", BU8)
print("Button 9 is", BU9)
print("Button 10 is", BU10)
print("Button 11 is", BU11)
print("Button 12 is", BU12)
print("Keypad registers", KP)
print("Joystick is", JS)
print("Dial 1 is set at", D1)
print("Dial 2 is set at", D2)
print("Dial 3 is set at", D3)