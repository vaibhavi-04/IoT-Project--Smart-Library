#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "Wokwi-GUEST";
const char* password = "";

// 🔴 Replace with your ngrok URL
const char* serverName = "http://sang-waterborne-bula.ngrok-free.dev/api/data";

// Seat button pins
int seatPins[] = {4, 5, 18, 19, 21, 22, 23, 25, 26, 27};
int totalSeats = 10;

// Potentiometer pin
const int potPin = 34;

// Seat states
bool seatState[10] = {false};
bool lastButtonState[10] = {HIGH};

// Debounce
unsigned long lastPressTime[10] = {0};
const int debounceDelay = 180;

// Timing for sending data
unsigned long lastSendTime = 0;
const int sendInterval = 5000;


// 🔥 Convert potentiometer value → Noise Level
String getNoiseLevel(int value) {
  if (value < 1200) return "Low";
  else if (value < 2800) return "Medium";
  else return "High";
}


void setup() {
  Serial.begin(115200);

  // Setup buttons
  for (int i = 0; i < totalSeats; i++) {
    pinMode(seatPins[i], INPUT_PULLUP);
  }

  // Potentiometer
  pinMode(potPin, INPUT);

  // Connect WiFi
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting...");
  }

  Serial.println("Connected to WiFi");
}


void loop() {

  // 🔁 FAST BUTTON HANDLING
  for (int i = 0; i < totalSeats; i++) {

    bool currentState = digitalRead(seatPins[i]);

    if (lastButtonState[i] == HIGH && currentState == LOW) {

      if (millis() - lastPressTime[i] > debounceDelay) {
        seatState[i] = !seatState[i];
        lastPressTime[i] = millis();

        Serial.print("Seat ");
        Serial.print(i);
        Serial.print(" → ");
        Serial.println(seatState[i] ? "Occupied" : "Free");
      }
    }

    lastButtonState[i] = currentState;
  }

  // 📊 Count occupied seats
  int occupied = 0;
  for (int i = 0; i < totalSeats; i++) {
    if (seatState[i]) occupied++;
  }

  float occupancyPercent = (occupied * 100.0) / totalSeats;

  // 🎛️ READ POTENTIOMETER
  int potValue = analogRead(potPin);
  String noiseLevel = getNoiseLevel(potValue);

  // Serial.print("Pot Value: ");
  // Serial.print(potValue);
  // Serial.print(" → Noise: ");
  // Serial.println(noiseLevel);


  // 🌐 SEND DATA EVERY 5 SECONDS
  if (WiFi.status() == WL_CONNECTED && millis() - lastSendTime > sendInterval) {

    WiFiClient client;
    HTTPClient http;

    http.begin(client, serverName);
    http.addHeader("Content-Type", "application/json");

    String jsonData = "{";

    // Seat array
    jsonData += "\"seats\":[";
    for (int i = 0; i < totalSeats; i++) {
      jsonData += seatState[i] ? "1" : "0";
      if (i < totalSeats - 1) jsonData += ",";
    }
    jsonData += "],";

    jsonData += "\"occupied_seats\":" + String(occupied) + ",";
    jsonData += "\"total_seats\":" + String(totalSeats) + ",";
    jsonData += "\"occupancy_percentage\":" + String(occupancyPercent) + ",";
    jsonData += "\"noise_level\":\"" + noiseLevel + "\",";
    jsonData += "\"noise_raw\":" + String(potValue);

    jsonData += "}";

    Serial.println("Sending:");
    Serial.println(jsonData);

    int response = http.POST(jsonData);

    Serial.print("Response: ");
    Serial.println(response);

    if (response <= 0) {
      Serial.print("Error: ");
      Serial.println(http.errorToString(response));
    }

    http.end();

    lastSendTime = millis();
  }
}