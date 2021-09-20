 void setup() {
  Serial.begin(9600);
}

void loop() {
  delay(60000);
  Serial.println("H:10.0");
  Serial.println("P:10.0");
  Serial.println("F:10.0");
  Serial.println("C:10.0");
  delay(15UL * 60UL * 1000UL);
  Serial.println("H:15.0");
  Serial.println("P:15.0");
  Serial.println("F:15.0");
  Serial.println("C:15.0");
  delay(30UL * 60UL * 1000UL);
  Serial.println("H:30.0");
  Serial.println("P:30.0");
  Serial.println("F:30.0");
  Serial.println("C:30.0");
  delay(60UL * 60UL * 1000UL);
  Serial.println("H:60.0");
  Serial.println("P:60.0");
  Serial.println("F:60.0");
  Serial.println("C:60.0");
}
