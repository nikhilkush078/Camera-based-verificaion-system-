#include <LiquidCrystal.h>

// RS, EN, D4, D5, D6, D7
// D1, D2, D5, D6, D3, D4 on most NodeMCU boards
LiquidCrystal lcd(5, 4, 14, 12, 0, 2);

void setup() {
  Serial.begin(115200);
  lcd.begin(16, 2);
  lcd.print("SYSTEM ONLINE");
  delay(2000);
  lcd.clear();
  lcd.print("READY TO SCAN");
}

void scrollMessage(String msg) {
  if (msg.length() <= 16) {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("SCAN RESULT:");
    lcd.setCursor(0, 1);
    lcd.print(msg);
    delay(4000);
  } else {
    // Scroll long text from right to left
    String padding = "    "; 
    String fullMsg = msg + padding;
    
    for (int repeat = 0; repeat < 2; repeat++) { // Loop the scroll twice
      for (int i = 0; i < fullMsg.length(); i++) {
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("SCAN RESULT:");
        lcd.setCursor(0, 1);
        lcd.print(fullMsg.substring(i, i + 16));
        delay(350); 
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