#include "time_utils.h"
#include <WiFi.h>
// #include "time.h"
#include <SD.h>
#include <SPI.h>
#include <ArduinoJson.h>

const char* ntpServer = "europe.pool.ntp.org";
const long  gmtOffset_sec = 3600; // GMT+1
const int   daylightOffset_sec = 3600; // Daylight saving time offset
bool wifiWorking = false;
bool timeWorking = false;
struct tm timeinfo;

#define USE_MOCK_TIME 0

#if USE_MOCK_TIME
  bool getMockLocalTime(struct tm *timeinfo) {
      // Simulate obtaining time by setting a fixed time or incrementing a counter
      static time_t mockTime = 1725514140;
      *timeinfo = *localtime(&mockTime);
      return true;
  }
#endif

// Function declarations
// void initializeTime();

// Function definitions
void initializeWifi() {

    // Open setup.json file
    File file = SD.open("/setup.json");
    if (!file) {
        Serial.println("Failed to open setup.json file");
        return;
    }

    // Allocate a buffer to store contents of the file
    size_t size = file.size();
    std::unique_ptr<char[]> buf(new char[size]);

    // Read file contents into buffer
    file.readBytes(buf.get(), size);
    file.close();

    // Parse JSON
    DynamicJsonDocument doc(1024);
    DeserializationError error = deserializeJson(doc, buf.get());
    if (error) {
        Serial.println("Failed to parse setup.json");
        return;
    }

    const char* ssid = doc["ssid"];
    const char* password = doc["password"];
    Serial.println("Connecting to WiFi: " + String(ssid));
    Serial.println("Password: " + String(password));

    // Connect to WiFi
    WiFi.begin(ssid, password);

    int attempts = 0;
    while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      attempts++;
      Serial.print(".");
      if(attempts == 10){
        Serial.println("Failed to connect to WiFi");
        return;
      }
    }
    wifiWorking = true;
    Serial.println("Connected to WiFi");
}
void initializeTime() {
    if(!wifiWorking){
      Serial.println("Failed to obtain time, no wifi connection");
      return;
    }
    configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);

    // Retry in case of failure in getting time
    int attempts = 0; // Reset attempts for time-sync
    while (
      #if USE_MOCK_TIME
              !getMockLocalTime(&timeinfo)
      #else
              !getLocalTime(&timeinfo)
      #endif
    ) { // Increased attempts
      Serial.println("Failed to obtain time, retrying...");
      delay(1000); // Delay before retrying
      attempts++;
      if(attempts == 10){
        Serial.println("Failed to obtain time for good");
        return;
      }
    }
    
    timeWorking = true;
    Serial.println("Time successfully obtained");
    Serial.println(&timeinfo, "Current time: %A, %B %d %Y %H:%M:%S");
}

long getSecondsTillNextImage(long delta, long deltaSinceTimeObtain){

    if(!timeWorking){
      unsigned int totalRuntime = millis() - delta;
      unsigned int totalRuntimeSeconds = totalRuntime / 1000;
      Serial.println("No time sleep time: " + String(24 * 60 * 60 - totalRuntimeSeconds));
      return 24 * 60 * 60 - totalRuntimeSeconds;
    }

    Serial.println(&timeinfo, "Current time: %A, %B %d %Y %H:%M:%S");

    // Calculate the total seconds from midnight to the current time
    unsigned int totalRuntime = millis() - deltaSinceTimeObtain;
    int currentSeconds = timeinfo.tm_hour * 3600 + timeinfo.tm_min * 60 + timeinfo.tm_sec;
    Serial.println("Current seconds: " + String(currentSeconds));
    currentSeconds += (totalRuntime / 1000);
    Serial.println("Current seconds: " + String(currentSeconds));
    // Calculate the total seconds from midnight to 10:00 AM
    int targetSeconds = 10 * 3600;

    // Calculate the time difference
    int timeDiff;
    // If current time is before or exactly 09:00 AM, calculate the difference to 10:00 AM
    if (currentSeconds <= targetSeconds - 60*60) {
      // If current time is before or exactly 10:00 AM
      timeDiff = targetSeconds - currentSeconds;
    } else {
      // If current time is after 10:00 AM, calculate the difference to 10:00 AM the next day
      int secondsInADay = 24 * 3600;
      timeDiff = secondsInADay - currentSeconds + targetSeconds;
    }

    Serial.println("Time difference: " + String(timeDiff) + " seconds");
    Serial.println("Time difference in microseconds: " + String(timeDiff * 1e6));
    return timeDiff;
}
