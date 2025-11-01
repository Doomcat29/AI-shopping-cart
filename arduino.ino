int buzzerPin = 2;

void setup() {
  pinMode(buzzerPin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    if (command == "ON") {
      tone(buzzerPin, 1000);
      Serial.println("Buzzer ON");
    } 
    
    if (command == "OFF") {
      noTone(buzzerPin);
      Serial.println("Buzzer OFF");
    }
  }
}
