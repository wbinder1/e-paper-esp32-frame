#define LED_BUILTIN 2 // Define built-in LED pin for ESP32

void setup() {
  pinMode(LED_BUILTIN, OUTPUT); // Initialize digital pin as an output.
}

void loop() {
  digitalWrite(LED_BUILTIN, HIGH); // Turn the LED on (HIGH is the voltage level)
  delay(1000); // Wait for a second
  digitalWrite(LED_BUILTIN, LOW); // Turn the LED off by making the voltage LOW
  delay(1000); // Wait for a second
}