#include "time_utils.h"
#include <WiFi.h>
#include <ezTime.h>
#include <SD.h>
#include <SPI.h>
#include <ArduinoJson.h>

const char* ntpServer = "europe.pool.ntp.org";
const long  gmtOffset_sec = 3600; // GMT+1
const int   daylightOffset_sec = 3600; // Daylight saving time offset
bool timeWorking = false;

// Function declarations
// void initializeTime();

// Function definitions
void initializeTime() {

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
      if(attempts == 3){
        Serial.println("Failed to connect to WiFi");
        return;
      }
    }
    // Init and get the time
    configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);

    // Check if time was successfully obtained
    struct tm timeinfo;
    if (!getLocalTime(&timeinfo)) {
        Serial.println("Failed to obtain time");
        return;
    }
    timeWorking = true;
    Serial.println("Time successfully obtained");
}


long getSecondsTillNextImage(long delta){

    struct tm timeinfo;
    if(!timeWorking || !getLocalTime(&timeinfo)){
      unsigned int totalRuntime = millis() - delta;
      Serial.println("No wifi sleep time: " + String(24 * 60 * 60e6 - totalRuntime * 1000));
      return 24 * 60 * 60e6 - totalRuntime * 1000;
    }

    Serial.println(&timeinfo, "Current time: %A, %B %d %Y %H:%M:%S");

    // Calculate the total seconds from midnight to the current time
    int currentSeconds = timeinfo.tm_hour * 3600 + timeinfo.tm_min * 60 + timeinfo.tm_sec;

    // Calculate the total seconds from midnight to 10:00 AM
    int targetSeconds = 10 * 3600;

    // Calculate the time difference
    int timeDiff;
    if (currentSeconds <= targetSeconds) {
      // If current time is before or exactly 10:00 AM
      timeDiff = targetSeconds - currentSeconds;
    } else {
      // If current time is after 10:00 AM, calculate the difference to 10:00 AM the next day
      int secondsInADay = 24 * 3600;
      timeDiff = secondsInADay - currentSeconds + targetSeconds;
    }

    Serial.println("Time difference: " + String(timeDiff) + " seconds");
    return timeDiff;
}
