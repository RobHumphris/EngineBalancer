
#define TRIGGER_TEETH 360
#define BAUD_RATE 115200
int strainSensorA[TRIGGER_TEETH];
int strainSensorB[TRIGGER_TEETH];

void setup() {
  populateArrays();
  Serial.begin(BAUD_RATE);
  Serial.println("Setup Complete.");
}

void loop() {
  int i;
  for (i=0; i<25; i++) {
    // Not synced
    Serial.println("NO");
    delay(100);
  }
  
  for (i=0; i<359; i++) {
    // Slowspeed Angle
    Serial.write('P');
    Serial.println(i);
    delay(100);
  }

  for (i=0; i<50; i++) {
    Serial.write('R');
    Serial.print("500");
    for(i=0; i<TRIGGER_TEETH; i++) {
      Serial.write(',');
      Serial.print(strainSensorA[i]);
      Serial.write(',');
      Serial.print(strainSensorB[i]);
    }  
    Serial.println();
  }
}

void populateArrays() {
  int i;

  for(i=0; i<360; i++) {
    strainSensorA[i] = sin(i)*50;
    strainSensorB[i] = cos(i)*50;
  }
}


