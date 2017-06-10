#include "WheatstoneBridge.h"

const int time_step = 500 ; // reading every 0.5s
const int triggerPin = 2;
const int directionPin = 3;
const int syncPin = 4;
const int debugPin = 13;
const int triggerTeeth = 360;

unsigned long revs = 0; 
long time = 0;
unsigned long previousTimeStamp = micros();
unsigned long prevSync = 9999;
unsigned long _rpm = 9999;

bool synced = false;
long toothCount = 0;
int wheelDirection = 0;
int strainSensorA[triggerTeeth];
int strainSensorB[triggerTeeth];

WheatstoneBridge wsbStrainA(A0, 365, 675, 0, 1000);
WheatstoneBridge wsbStrainB(A1, 365, 675, 0, 1000);

void setup() {
  pinMode(triggerPin, INPUT);
  digitalWrite(triggerPin, LOW);

  pinMode(directionPin, INPUT);
  digitalWrite(directionPin, LOW);

  pinMode(syncPin, INPUT);
  digitalWrite(syncPin, LOW);

  pinMode(debugPin, OUTPUT);
  digitalWrite(debugPin, LOW);
  
  attachInterrupt(digitalPinToInterrupt(triggerPin), triggerPinInterrupt, FALLING);
  Serial.begin(9600); //  setup serial baudrate
  Serial.println("Setup Complete.");
}

void loop() {
  //int strain = wsbStrainA.measureForce();
  //int raw = wsbStrainA.getLastForceRawADC();
  
  if(millis() > time_step+time) {
    /*Serial.print("Synced: ");
    Serial.print(synced);

    Serial.print("    ");*/
    Serial.print("Tooth Count: ");
    Serial.print(toothCount);

    Serial.print("    ");
    Serial.print("Revs: ");
    Serial.print(revs);

    
    Serial.print("    ");
    Serial.print("RPM: ");
    Serial.print(_rpm);
    
    /*Serial.print("    ");
    Serial.print("Wheel Direction: ");
    Serial.print(wheelDirection);
    
    Serial.print("    ");
    Serial.print("Strain A: ");
    Serial.print(strain);
    
    Serial.print("    ");
    Serial.print("Raw A: ");
    Serial.print(raw);*/
    
    Serial.print('\n'); 
    time = millis();
  }
}

void checkSyncPin() {
  int sync = digitalRead(syncPin);
  if (sync == LOW) {
    synced = true;
    //toothCount = 0;
  }
}

void countRevs() {
  unsigned long time = millis();
  _rpm = 60000 / (time - prevSync);
  revs++;
  prevSync = time;
}

void checkDirection() {
  int direction = digitalRead(directionPin);
  wheelDirection = (direction == LOW) ? 1 : -1; 
  toothCount += wheelDirection;
  if (toothCount < 0) {
    toothCount = triggerTeeth;
    countRevs();
  } else if (toothCount > triggerTeeth) {
    toothCount = 0;
    countRevs();
  }
}

void  getStrainReadings() {
  //strainSensorA[toothCount] = wsbStrainA.measureForce();
  //strainSensorB[toothCount] = wsbStrainB.measureForce(); 
}

void triggerPinInterrupt() {
  unsigned long timestamp = millis();
  digitalWrite(debugPin, HIGH);
 
  //if (synced) {
  checkDirection();
  //  getStrainReadings();
  //} 
  //checkSyncPin();
  previousTimeStamp = timestamp;
  digitalWrite(debugPin, LOW);
}

