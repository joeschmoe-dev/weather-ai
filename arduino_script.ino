#include <Wire.h>
#include <Adafruit_AHTX0.h>

Adafruit_AHTX0 aht;

void setup() {
  Serial.begin(9600);
  if (!aht.begin()) {
    Serial.println("AHT20 sensor not found. Check wiring!");
    while (1);
  }
  //Utilize this lower line only for testing the I2C connection
  //Having this line uncommented will cause errors when running with the python script
  //Serial.println("AHT20 sensor initialized.");
}

void loop() {
  sensors_event_t humidity, temp;
  aht.getEvent(&humidity, &temp);

  if (Serial.available() > 0) {
    String msg = Serial.readStringUntil('\n');
    msg.trim();
    if (msg == "read") {
      Serial.print(temp.temperature);
    }
    Serial.read();
  }

}
