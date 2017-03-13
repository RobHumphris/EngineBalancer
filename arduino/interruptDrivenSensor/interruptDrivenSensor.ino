#include "WheatstoneBridge.h"

const int time_step = 500 ; // reading every 0.5s
const int triggerPin = 2;
const int directionPin = 3;
const int syncPin = 4;
const int triggerTeeth = 4; // 180;

long time = 0;
unsigned long previousTimeStamp = micros();

bool synced = false;
long toothCount = 0;
int wheelDirection = 0;
int strainSensorA[triggerTeeth];
int strainSensorB[triggerTeeth];

WheatstoneBridge wsbStrainA(A0, 365, 675, 0, 1000);
WheatstoneBridge wsbStrainB(A1, 365, 675, 0, 1000);

void setup() {
  pinMode(triggerPin, INPUT);
  digitalWrite(triggerPin, HIGH);

  pinMode(directionPin, INPUT);
  digitalWrite(directionPin, HIGH);

  pinMode(syncPin, INPUT);
  digitalWrite(syncPin, HIGH);
  
  attachInterrupt(digitalPinToInterrupt(triggerPin), triggerPinInterrupt, RISING);
  Serial.begin(9600); //  setup serial baudrate
  Serial.println("Setup Complete.");
}

void loop() {
  int strain = wsbStrainA.measureForce();
  int raw = wsbStrainA.getLastForceRawADC();
  
  if(millis() > time_step+time) {
    Serial.print("Synced: ");
    Serial.print(synced);
    
    Serial.print("\tTooth Count: ");
    Serial.print(toothCount);
    
    Serial.print("\tWheel Direction: ");
    Serial.print(wheelDirection);

    Serial.print("\tStrain A: ");
    Serial.print(strain);

    Serial.print("\tRaw A: ");
    Serial.print(raw);
    
    Serial.println('\n'); 
    time = millis();
  }
}

void checkSyncPin() {
  int sync = digitalRead(syncPin);
  if (sync == LOW) {
    synced = true;
    toothCount = 0;
  }
}

void checkDirection() {
  int direction = digitalRead(directionPin);
  wheelDirection = (direction == LOW) ? 1 : -1; 
  toothCount += wheelDirection;
  if (toothCount < 0) {
    toothCount = triggerTeeth;
  } else if (toothCount > triggerTeeth) {
    toothCount = 0;
  }
}

void  getStrainReadings() {
  //strainSensorA[toothCount] = wsbStrainA.measureForce();
  //strainSensorB[toothCount] = wsbStrainB.measureForce(); 
}

void triggerPinInterrupt() {
  unsigned long timestamp = micros();
  if (synced) {
    checkDirection();
    getStrainReadings();
  } 
  checkSyncPin();
  previousTimeStamp = timestamp;
}

