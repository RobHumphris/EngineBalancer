 #include "WheatstoneBridge.h"
#include <Arduino.h>
#define NOT_AN_INTERRUPT -1 
#define TRIGGER_TEETH 360
#define _BAUD_RATE 256000
#define BAUD_RATE 115200
#define MODULUS 4
#define RPM_THRESHOLD 100
#define BALANCE_THRESHOLD_MIN 450
#define BALANCE_THRESHOLD_MAX 550

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
size_t sensorArraySize = sizeof(sensorArraySize);
bool go = false;
int count = 0;

void setup() {
  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
  
  pinMode(triggerPin, INPUT);
  digitalWrite(triggerPin, HIGH);

  pinMode(directionPin, INPUT);
  digitalWrite(directionPin, HIGH);

  pinMode(syncPin, INPUT);
  digitalWrite(syncPin, HIGH);
  
  attachInterrupt(digitalPinToInterrupt(triggerPin), triggerPinInterrupt, RISING);
  attachInterrupt(digitalPinToInterrupt(syncPin), syncPinInterrupt, RISING); 
  
  Serial.begin(BAUD_RATE);
  Serial.println("Setup Complete.");
  previousTimeStamp = 0;
}

int min = 999;
int max = -999;

void loop() {
  int i;
  #if 1
  if (go) {
    if (synced) {
      if (rpm < RPM_THRESHOLD) {
        Serial.write('P');
        Serial.println(toothCount);
      }
      else {
        if ((rpm > BALANCE_THRESHOLD_MIN) && (rpm < BALANCE_THRESHOLD_MAX)) {
          Serial.write('R');
          Serial.print((int)rpm);
          for(i=0; i<TRIGGER_TEETH-MODULUS; i+=MODULUS) {
            Serial.write(',');
            Serial.print(strainSensorA[i]);
            Serial.write(',');
            Serial.print(strainSensorB[i]);
          }
          Serial.println();
        }
      }
    } else {
      Serial.println("NO");
    }
    Serial.flush();
    go = false;
  }
  #endif
  #if 0
    int a = analogRead(A0);
    int b = analogRead(A1);
    min = (a < min) ? a : min;
    max = (a > max) ? a : max;    
    Serial.print(min);
    Serial.print(',');
    Serial.print(max);
    Serial.print(':');
    Serial.print(a);
    Serial.println();
  #endif
}

void syncPinInterrupt() {
  unsigned long ts = millis();
  synced = true;
  toothCount = (wheelDirection == 1) ? -1 : 360;
  syncCount++;
  rpm = 60000 / (ts - previousTimeStamp);
  previousTimeStamp = ts;
  go = true;
}

void readStrainSensors(int tooth) {
  strainSensorA[toothCount] = analogRead(A0); 
  strainSensorB[toothCount] = analogRead(A1);
}

void triggerPinInterrupt() {
  if (synced) {
    wheelDirection = (digitalRead(directionPin) == LOW) ? -1 : 1; 
    toothCount += wheelDirection;
    if ((toothCount >=0) && (toothCount < TRIGGER_TEETH) && (toothCount % MODULUS == 0)) {
      readStrainSensors(toothCount);
    }
  }
  if (rpm < RPM_THRESHOLD) {
    go = true;
  }
}

