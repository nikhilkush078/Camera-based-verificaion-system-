#include <LiquidCrystal.h>

// RS, EN, D4, D5, D6, D7
// Standard NodeMCU Pins: D1, D2, D5, D6, D3, D4
LiquidCrystal lcd(5, 4, 14, 12, 0, 2);

// Pin Definitions
#define BUZZER_PIN 16 // D0
#define RED_LED    15 // D8
#define GREEN_LED  13 // D7

void setup() {
  Serial.begin(115200);
  
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(RED_LED, OUTPUT);
  pinMode(GREEN_LED, OUTPUT);
  
  // Ensure everything is off at start
  digitalWrite(BUZZER_PIN, LOW);
  digitalWrite(RED_LED, LOW);
  digitalWrite(GREEN_LED, LOW);

  lcd.begin(16, 2);
  lcd.print("SYSTEM ONLINE");
  delay(2000);
  lcd.clear();
  lcd.print("READY TO SCAN");
}

void successFeedback() {
  digitalWrite(GREEN_LED, HIGH);
  // Access Granted Tone: Two short high beeps
  digitalWrite(BUZZER_PIN, HIGH);
  delay(150);
  digitalWrite(BUZZER_PIN, LOW);
  delay(50);
  digitalWrite(BUZZER_PIN, HIGH);
  delay(150);
  digitalWrite(BUZZER_PIN, LOW);
  
  delay(2000); // Keep LED on for 2 seconds
  digitalWrite(GREEN_LED, LOW);
}

void failFeedback() {
  digitalWrite(RED_LED, HIGH);
  // Access Denied Tone: One long low beep
  digitalWrite(BUZZER_PIN, HIGH);
  delay(1000);
  digitalWrite(BUZZER_PIN, LOW);
  
  delay(1000); // Keep LED on for 1 more second
  digitalWrite(RED_LED, LOW);
}

void scrollMessage(String msg) {
  // Check if access was granted or denied based on Python response
  bool accessGranted = (msg.indexOf("WELCOME") >= 0);
  
  if (accessGranted) {
    successFeedback();
  } else if (msg.indexOf("DENIED") >= 0) {
    failFeedback();
  }

  // Handle LCD Scrolling
  if (msg.length() <= 16) {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("SCAN RESULT:");
    lcd.setCursor(0, 1);
    lcd.print(msg);
    delay(3000);
  } else {
    String padding = "    "; 
    String fullMsg = msg + padding;
    for (int repeat = 0; repeat < 1; repeat++) { 
      for (int i = 0; i < fullMsg.length(); i++) {
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("SCAN RESULT:");
        lcd.setCursor(0, 1);
        lcd.print(fullMsg.substring(i, i + 16));
        delay(300); 
      }
    }
  }
  
  lcd.clear();
  lcd.print("READY TO SCAN");
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    data.trim();
    if (data.length() > 0) {
      scrollMessage(data);
    }
  }
}
