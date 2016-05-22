This is just a quick list of things I can think of that we still need to do on the arm board


TODO
====
- [X] Finish duty-cycle manager but for the time being we can just set everything to +/- 255 depending on the direction. **NEEDS TESTING**
- [X] Test communication
- [X] Finish control file
- [X] Fill in pinout
- [X] Test feedback
- [X] Write .ino file
- [X] Find proper resistance to add to L1 (4.7k)
- [X] Calibrate arm
- [X] Add limits.
- [X] Figure out how to determine if a motor should be shut off until the next command for inverse kin. Always on and use tolerance
- [X] Inverse kinematics ** NEEDS TESTING**
- [ ] Look into whether position ranges need to be normalized
- [ ] Make it so that the arm can send back its position data to the rover **NEW**
- [ ] Implement the encoder feedback for the base rotation ** NEW **
- [ ] Look at automating some basic movements **NEW*
- [ ] Lots of wiring
- [ ] Testing, testing, testing!!

There's probably more but this is what I could think of off the top of my head.
