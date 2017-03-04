int time_step = 500 ; // reading every 0.5s
int optoPin = 2;
int directionPin = 3;
int syncPin = 4;

long time = 0;
long count = 0;

void setup() {
  pinMode(optoPin, INPUT);
  attachInterrupt(digitalPinToInterrupt(optoPin), optoInterrupt, FALLING);
  Serial.begin(9600); //  setup serial baudrate
  Serial.println("Setup Complete.");
}

void loop() {
  // millis returns the number of milliseconds since the board started the current program
  //digitalWrite(ledPin, digitalRead(optoPin));

  if(millis() > time_step+time) {
    Serial.print("Time step : ");
    Serial.print(time);     // display strain 1 reading
    Serial.print('\t');
    Serial.print(" Interrupts : ");
    Serial.print(count);
    Serial.print(" Current state : ");
    if (digitalRead(optoPin) == HIGH) {
      Serial.print("HIGH");
    } else {
      Serial.print("LOW");
    }
    Serial.println('\n'); 
    time = millis();
  }
}

void optoInterrupt() {
  count++;
}

