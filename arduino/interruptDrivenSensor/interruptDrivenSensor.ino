#include "WheatstoneBridge.h"
#include <Arduino.h>
#define NOT_AN_INTERRUPT -1 
#define TRIGGER_TEETH 360

const int triggerPin = 2;
const int syncPin = 3;
const int directionPin = 4;

unsigned long previousTimeStamp;
bool synced = false;
long toothCount = 0;
long syncCount = 0;
float rpm = 0;
int wheelDirection = 0;
int strainSensorA[TRIGGER_TEETH];
int strainSensorB[TRIGGER_TEETH];
bool go = false;

//WheatstoneBridge wsbStrainA(A0, 365, 675, 0, 1000);
//WheatstoneBridge wsbStrainB(A1, 365, 675, 0, 1000);

WheatstoneBridge wsb_strain1(A0, 365, 675, 0, 1000);
WheatstoneBridge wsb_strain2(A1, 365, 675, 0, 1000);

void setup() {
  pinMode(triggerPin, INPUT);
  digitalWrite(triggerPin, HIGH);

  pinMode(directionPin, INPUT);
  digitalWrite(directionPin, HIGH);

  pinMode(syncPin, INPUT);
  digitalWrite(syncPin, HIGH);
  
  //attachInterrupt(digitalPinToInterrupt(triggerPin), triggerPinInterrupt, RISING);
  //attachInterrupt(digitalPinToInterrupt(syncPin), syncPinInterrupt, RISING); 
  
  Serial.begin(115200);
  Serial.println("Setup Complete.");
  previousTimeStamp = 0;
}

void loop() {
  int i;
  #if 0
  if (go) {
    if (synced) {
      if (rpm < 200) {
        // Below 200 rpm we return Angle
        Serial.write('P');
        Serial.println(toothCount);
      }
      else {
        // Above 
        Serial.write('R');
        Serial.print(rpm);
        for(i=0; i<TRIGGER_TEETH; i++) {
          Serial.write(',');
          Serial.print(strainSensorA[i]);
          Serial.write(',');
          Serial.print(strainSensorB[i]);
        }  
        Serial.println();
      }
    } else {
      Serial.println("NO");
    }
    go = false;
  }
  else {
    Serial.print("Strain A: ");
    Serial.print(wsb_strain1.measureForce());
    Serial.print("\tStrain B: ");
    Serial.println(wsb_strain2.measureForce());
  }
  #endif
  
  //Serial.print(wsb_strain1.measureForce());
  //Serial.print(",");
  Serial.println(wsb_strain1.measureForce());
}

void syncPinInterrupt() {
  unsigned long ts = millis();
  synced = true;
  toothCount = (wheelDirection == 1) ? -1 : 360;
  syncCount++;
  rpm = 60000 /( ts - previousTimeStamp);
  previousTimeStamp = ts;
  go = true;
}

void triggerPinInterrupt() {
  if (synced) {
    wheelDirection = (digitalRead(directionPin) == LOW) ? -1 : 1; 
    toothCount += wheelDirection;
    if ((toothCount >=0) && (toothCount < TRIGGER_TEETH)) {
      strainSensorA[toothCount] = wsb_strain1.measureForce();
      strainSensorB[toothCount] = wsb_strain2.measureForce(); 
    }
  } 
  if (rpm < 200) {
    go = true;
  }
}

