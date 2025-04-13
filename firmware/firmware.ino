/* 
 * Program to make what is effectively a telegram on an arduino. 
 * 
 * This program needs to be able to: 
 *   - Read a bit from serial every 20ms 
 *     |-> Buzz or don't buzz for 20ms, depending on what was recieved
 * 
 *   - Write a bit to the serial every 20ms
 *     |-> If a 1 was written, buzz 
 *     |-> If a 0 was written, don't buzz 
 * 
 * All buzzing needs to be non-blocking (tone() is non blocking)
 * 
*/

#define BUZZER_PIN 11
#define BUTTON_PIN 8
#define BAUD_RATE 115200
#define REFRESH_RATE 20 // ms
#define FREQ 600 // hz

bool serialState = 0;
bool buttonState = 0;

void setup() {
    pinMode(BUZZER_PIN, OUTPUT);
    pinMode(BUTTON_PIN, INPUT_PULLUP);
    Serial.begin(BAUD_RATE);

    digitalWrite(BUZZER_PIN, LOW);
}

void loop() {
    if (Serial.available() > 0) {
        char c = Serial.read();
        serialState = (c == '1') ? 1 : 0;
    } else {
        serialState = 0;
    }
    
    buttonState = !digitalRead(BUTTON_PIN);
    Serial.println(buttonState == 1 ? "1" : "0");

    if (serialState == 1 || buttonState == 1) {
        tone(BUZZER_PIN, FREQ, REFRESH_RATE - 100);
    } else {
        noTone(BUZZER_PIN);
    }

    delay(REFRESH_RATE);
}
