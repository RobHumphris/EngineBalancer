#define LED_PIN LED_BUILTIN
#define SENSOR_ONE_PIN PIN_A0
#define SENSOR_TWO_PIN PIN_A1

void setup() {
  Serial.begin(115200);
  for (auto startNow = millis() + 2500; !Serial && millis() < startNow; delay(500));
  
  pinMode(LED_PIN, OUTPUT);
  pinMode(SENSOR_ONE_PIN, INPUT);
  pinMode(SENSOR_TWO_PIN, INPUT);
  analogReadResolution(14);
}

void loop() {
  int analogValueOne = 0;
  int analogValueTwo = 0;
  for (int i=0; i<10; i++) {
    analogValueOne += analogRead(SENSOR_ONE_PIN);
    analogValueTwo += analogRead(SENSOR_TWO_PIN);
    delay(1);
  }
  
  float averageValueOne = (analogValueOne / 10);
  float averageValueTwo = (analogValueTwo / 10);

  Serial.print(averageValueOne);
  Serial.print(",");
  Serial.print(analogValueTwo);
  Serial.println();
}
