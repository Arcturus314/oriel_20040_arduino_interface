#include "pinout.h"

void setup() {
  Serial.begin(9600);

  // See pinout.h for mapping to DB15 connector
  pinMode(db15.halffull, OUTPUT);
  pinMode(db15.en, OUTPUT);
  pinMode(db15.fwdlim, INPUT);
  pinMode(db15.revlim, INPUT);
  pinMode(db15.steppulse, OUTPUT);
  pinMode(db15.fwdrev, OUTPUT);

  Serial.println("INIT DONE");
}

// super basic commands for now. From computer to Arduino:
/*
 * 1: step forward
 * 2: step backward
 * 3: enable
 * 4: disable
 */

 // from Arduino to computer:
 /* 
  * 1: complete, no err
  * 2: rev lim
  * 3: forward lim
  * 4: unrecognized
  */

bool dir = true;

int step(bool setdir) {
  // if setdir = True, step FORWARD one
  // if setdir = False, step BACKWARD one
  // return 2 if at reverse limit, return 3 if at forward limit
  if (setdir != dir) {
    dir = setdir;
    digitalWrite(db15.fwdrev, dir);
    delay(100);
  }

  digitalWrite(db15.steppulse, HIGH);
  delay(25);
  digitalWrite(db15.steppulse, LOW);
  delay(25);

  if (!digitalRead(db15.revlim)) return 2;
  else if (!digitalRead(db15.fwdlim)) return 3;
  else return 1;


}

void loop() {
  // Wait until some serial character is received
  if (Serial.available() > 0) {
    int incomingByte = Serial.read();
    switch (incomingByte) {
      case 0x31:
        Serial.print(step(true));
        break;
      case 0x32:
        Serial.print(step(false));
        break;
      case 0x33:
        digitalWrite(db15.en, HIGH);
        Serial.print(1);
        break;
      case 0x34:
        digitalWrite(db15.en, LOW);
        Serial.print(1);
        break;
      default:
        Serial.print(4);
        break;
    }
  }
}
