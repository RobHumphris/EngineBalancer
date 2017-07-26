// ADC Settings from http://www.microsmart.co.za/technical/2014/03/01/advanced-arduino-adc/
#include <Arduino.h>
#define NOT_AN_INTERRUPT -1 
#define TRIGGER_TEETH 360
#define _BAUD_RATE 256000
#define BAUD_RATE 115200
#define MODULUS 4
#define RPM_THRESHOLD 100
#define BALANCE_THRESHOLD_MIN 450
#define BALANCE_THRESHOLD_MAX 550

const unsigned char PS_32 = (1 << ADPS2) | (1 << ADPS0);
const unsigned char PS_128 = (1 << ADPS2) | (1 << ADPS1) | (1 << ADPS0);

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

void setupADC() {
  pinMode(A0, INPUT);
  pinMode(A1, INPUT);

  // set up the ADC for higherspeed conversion
  ADCSRA &= ~PS_128;
  ADCSRA |= PS_32;
}

void setupSerial() {
  Serial.begin(BAUD_RATE);
  Serial.println("Setup Complete.");
}

void setup() {
  setupADC();
  
  pinMode(triggerPin, INPUT);
  digitalWrite(triggerPin, HIGH);
  attachInterrupt(digitalPinToInterrupt(triggerPin), triggerPinInterrupt, RISING);

  pinMode(syncPin, INPUT);
  digitalWrite(syncPin, HIGH);
  attachInterrupt(digitalPinToInterrupt(syncPin), syncPinInterrupt, RISING); 
  
  pinMode(directionPin, INPUT);
  digitalWrite(directionPin, HIGH);
  
  setupSerial();
  previousTimeStamp = 0;
}

int min = 999;
int max = -999;

void loop() {
  int i, a, b;
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
      //Serial.print("NO");
      a = analogRead(A0);
      b = analogRead(A1);
      Serial.print("C,");
      Serial.print((int)a);
      Serial.write(',');
      Serial.println((int)b);
      Serial.flush();
    }
    Serial.flush();
    go = false;
  } else {
      /*a = analogRead(A0);
      b = analogRead(A1);
      Serial.print("C,");
      Serial.print((int)a);
      Serial.write(',');
      Serial.println((int)b);
      Serial.flush();*/
  }
  #endif
  #if 0
    a = analogRead(A0);
    b = analogRead(A1);
    min = (a < min) ? a : min;
    max = (a > max) ? a : max;    
    //Serial.print(min);
    //Serial.print(',');
    //Serial.print(max);
    //Serial.print(':');
    Serial.print(a);
    Serial.print("  ");
    Serial.println(b);
  #endif
  #if 0
    unsigned long _start = micros();
    int a = analogRead(A0);
    int b = analogRead(A1);
    unsigned long _stop = micros();
    Serial.println(_stop - _start);
    delay(500);
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

