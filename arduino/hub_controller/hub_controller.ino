

#include <Arduino_JSON.h>

#define BUTTON_PIN 10 // btn pin
#define RELAY_PIN 12 // relay pin


void setup() {
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(RELAY_PIN, OUTPUT);

  digitalWrite(RELAY_PIN, LOW);

  Serial.begin(9600);

  // send message so that we know that this is the hub controller
  JSONVar message;
  message["msg"] = "hello";
  String jsonString = JSON.stringify(message);
  Serial.println(jsonString);
}

void loop() {
  // check if skip button is pressed
  int value = digitalRead(BUTTON_PIN);
  if (value == LOW)
  {
    JSONVar message;
    message["msg"] = "button";
    String jsonString = JSON.stringify(message);
    Serial.println(jsonString);
  }
  // check if there's incomming data
  if (Serial.available())
  {
    JSONVar data;
    {
      String incomming = Serial.readStringUntil('\n');// read serial data untill newline
      data = JSON.parse(incomming);
    }
    if (data.hasOwnProperty("msg"))
    {
      bool state = (bool) data["msg"]; // just on or off bool flag in message
      digitalWrite(RELAY_PIN, state ? HIGH : LOW); // depending on message this will turn the relay on or off
    }
  }
}
