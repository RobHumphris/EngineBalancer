// #define LED_PIN LED_BUILTIN
// #define SENSOR_ONE_PIN PIN_A0
// #define SENSOR_TWO_PIN PIN_A1
// #define ACCELEROMETER_ONE_PIN PIN_A2

// #define ADC_AMPLITUDE 16383
// #define ZERO_Z 1.25
// #define SENSITIVITY 0.25
// #define ADC_REF 3.3

// void setup() {
//   Serial.begin(115200);
//   for (auto startNow = millis() + 2500; !Serial && millis() < startNow; delay(500));
  
//   pinMode(LED_PIN, OUTPUT);
//   pinMode(ACCELEROMETER_ONE_PIN, INPUT);
//   analogReadResolution(14);
// }

// const int loopCount = 10;
// int acc[10];
// int arrayIndex = 0;
// bool filling = true;

// void readAccelerometer() {
//   unsigned long start = micros();
//   acc[arrayIndex++]=analogRead(ACCELEROMETER_ONE_PIN);
//   delayMicroseconds(3000-(micros()-start));
//   arrayIndex = arrayIndex < 10 ? arrayIndex : 0;
// }

// float getMovingAverage() {
//   long sum = acc[0]+acc[1]+acc[2]+acc[3]+acc[4]+acc[5]+acc[6]+acc[7]+acc[8]+acc[9];
//   long avg = sum/10;
//   float voltage = (float)avg * ADC_REF / ADC_AMPLITUDE;
//   return (voltage - ZERO_Z) / SENSITIVITY;
// }

// void loop() {
//   if (filling) {
//     for (int i=0; i<10; i++) {
//       readAccelerometer();
//     }
//     filling = false;
//   }
//   readAccelerometer();
//   Serial.print("3.0000");
//   Serial.print(",");
//   Serial.print(getMovingAverage());
//   Serial.print(",");
//   Serial.print("3.0000");
//   Serial.println();
// }

///////////////////////////////////////////////////////////////////////////////
//
//  Hardware Configuration:
//  -----
//  Arduino Nano R4
//  Adafruit PCA9546 4-Channel STEMM https://learn.adafruit.com/adafruit-pca9546-4-channel-stemma-qt-multiplexer
//  Adafruit NAU7802 24-bit ADC - ST
#include <Adafruit_NAU7802.h>

Adafruit_NAU7802 nau;
const byte numChars = 32;
char receivedChars[numChars];   // an array to store the received data
boolean newData = false;

void setup() {
  Serial.begin(115200);
  Serial.println("NAU7802");
  if (!nau.begin(&Wire1)) {
    Serial.println("Failed to find NAU7802");
    while (1) {;
      Serial.println("Failed to find NAU7802");
      delay(1000);  // Don't proceed.
    }
  }
  Serial.println("Found NAU7802");

  nau.setLDO(NAU7802_4V5);
  nau.setGain(NAU7802_GAIN_32);
  nau.setRate(NAU7802_RATE_320SPS); 
}

void getFeatures() {
  Serial.print("LDO voltage set to ");
  switch (nau.getLDO()) {
    case NAU7802_4V5:  Serial.println("4.5V"); break;
    case NAU7802_4V2:  Serial.println("4.2V"); break;
    case NAU7802_3V9:  Serial.println("3.9V"); break;
    case NAU7802_3V6:  Serial.println("3.6V"); break;
    case NAU7802_3V3:  Serial.println("3.3V"); break;
    case NAU7802_3V0:  Serial.println("3.0V"); break;
    case NAU7802_2V7:  Serial.println("2.7V"); break;
    case NAU7802_2V4:  Serial.println("2.4V"); break;
    case NAU7802_EXTERNAL:  Serial.println("External"); break;
  }

  Serial.print("Gain set to ");
  switch (nau.getGain()) {
    case NAU7802_GAIN_1:  Serial.println("1x"); break;
    case NAU7802_GAIN_2:  Serial.println("2x"); break;
    case NAU7802_GAIN_4:  Serial.println("4x"); break;
    case NAU7802_GAIN_8:  Serial.println("8x"); break;
    case NAU7802_GAIN_16:  Serial.println("16x"); break;
    case NAU7802_GAIN_32:  Serial.println("32x"); break;
    case NAU7802_GAIN_64:  Serial.println("64x"); break;
    case NAU7802_GAIN_128:  Serial.println("128x"); break;
  }

  Serial.print("Conversion rate set to ");
  switch (nau.getRate()) {
    case NAU7802_RATE_10SPS:  Serial.println("10 SPS"); break;
    case NAU7802_RATE_20SPS:  Serial.println("20 SPS"); break;
    case NAU7802_RATE_40SPS:  Serial.println("40 SPS"); break;
    case NAU7802_RATE_80SPS:  Serial.println("80 SPS"); break;
    case NAU7802_RATE_320SPS:  Serial.println("320 SPS"); break;
  }
}

void loop() {
  int32_t chan0, chan1;

  nau.setChannel(0);
  while (! nau.available()) {
    delay(1);
  }
  chan0 = nau.read()/10;

  nau.setChannel(1);
  while (! nau.available()) {
    delay(1);
  }
  chan1 = nau.read()/10;
  Serial.print(chan0); Serial.print(","); Serial.println(chan1);
  delay(3);
}







// #include "Wire.h"
// #include <Adafruit_NAU7802.h>

// #define TCAADDR 0x70
// #define NAUADDR 0x20

// #define IC2WIRE Wire1

// void setup() {
//     while (!Serial);
//     delay(1000);
//     Serial.begin(115200);
//     setupMultiplexer();
// }

// void tcaselect(uint8_t i) {
//   if (i > 3) return;
//   IC2WIRE.beginTransmission(TCAADDR);
//   IC2WIRE.write(1 << i);
//   IC2WIRE.endTransmission();  
// }

// void setupMultiplexer()
// {
//     IC2WIRE.begin();
//     Serial.println("\nTCA I2C Enumeration starting");
    
//     for (uint8_t t=0; t<4; t++) {
//       tcaselect(t);
//       Serial.print("TCA Port #"); Serial.println(t);

//       for (uint8_t addr = 0; addr<=127; addr++) {
//         if (addr == TCAADDR) continue;

//         IC2WIRE.beginTransmission(addr);
//         if (!IC2WIRE.endTransmission()) {
//           Serial.print("Found I2C 0x");  Serial.println(addr,HEX);
//         }
//       }
//     }
//     Serial.println("\nTCA I2C Enumeration complete");
// }


// void loop() {

// }

// void setupADC() {
//   Serial.println("\nNAU7802 Setup starting");
//   if (! nau.begin()) {
//     Serial.println("Failed to find NAU7802");
//     while (1) delay(10);  // Don't proceed.
//   }
//   Serial.println("Found NAU7802");

//   nau.setLDO(NAU7802_3V0);
//   Serial.print("LDO voltage set to ");
//   switch (nau.getLDO()) {
//     case NAU7802_4V5:  Serial.println("4.5V"); break;
//     case NAU7802_4V2:  Serial.println("4.2V"); break;
//     case NAU7802_3V9:  Serial.println("3.9V"); break;
//     case NAU7802_3V6:  Serial.println("3.6V"); break;
//     case NAU7802_3V3:  Serial.println("3.3V"); break;
//     case NAU7802_3V0:  Serial.println("3.0V"); break;
//     case NAU7802_2V7:  Serial.println("2.7V"); break;
//     case NAU7802_2V4:  Serial.println("2.4V"); break;
//     case NAU7802_EXTERNAL:  Serial.println("External"); break;
//   }

//   nau.setGain(NAU7802_GAIN_128);
//   Serial.print("Gain set to ");
//   switch (nau.getGain()) {
//     case NAU7802_GAIN_1:  Serial.println("1x"); break;
//     case NAU7802_GAIN_2:  Serial.println("2x"); break;
//     case NAU7802_GAIN_4:  Serial.println("4x"); break;
//     case NAU7802_GAIN_8:  Serial.println("8x"); break;
//     case NAU7802_GAIN_16:  Serial.println("16x"); break;
//     case NAU7802_GAIN_32:  Serial.println("32x"); break;
//     case NAU7802_GAIN_64:  Serial.println("64x"); break;
//     case NAU7802_GAIN_128:  Serial.println("128x"); break;
//   }

//   nau.setRate(NAU7802_RATE_10SPS);
//   Serial.print("Conversion rate set to ");
//   switch (nau.getRate()) {
//     case NAU7802_RATE_10SPS:  Serial.println("10 SPS"); break;
//     case NAU7802_RATE_20SPS:  Serial.println("20 SPS"); break;
//     case NAU7802_RATE_40SPS:  Serial.println("40 SPS"); break;
//     case NAU7802_RATE_80SPS:  Serial.println("80 SPS"); break;
//     case NAU7802_RATE_320SPS:  Serial.println("320 SPS"); break;
//   }

//   // Take 10 readings to flush out readings
//   for (uint8_t i=0; i<10; i++) {
//     while (! nau.available()) delay(1);
//     nau.read();
//   }

//   while (! nau.calibrate(NAU7802_CALMOD_INTERNAL)) {
//     Serial.println("Failed to calibrate internal offset, retrying!");
//     delay(1000);
//   }
//   Serial.println("Calibrated internal offset");

//   while (! nau.calibrate(NAU7802_CALMOD_OFFSET)) {
//     Serial.println("Failed to calibrate system offset, retrying!");
//     delay(1000);
//   }
//   Serial.println("Calibrated system offset");
// }

