#include <Arduino.h>

const int LDR_PIN = 2; 
void setup() {
  Serial.begin(115200); 
  analogReadResolution(12); 
}

void loop() {
  int ldrValue = analogRead(LDR_PIN); 
  Serial.print("LDR Wert: ");
  Serial.println(ldrValue);
  delay(500);
}
