#ifndef TIME_UTILS_H
#define TIME_UTILS_H

#include <WiFi.h>
#include <SD.h>
#include <SPI.h>
// #include "time.h"
#include <ArduinoJson.h>

#define USE_MOCK_TIME 0

#if USE_MOCK_TIME
bool getMockLocalTime(struct tm *timeinfo);
#endif

// External variable declarations
extern const char* ntpServer;
extern const long gmtOffset_sec;
extern const int daylightOffset_sec;
extern bool wifiWorking;
extern bool timeWorking;
extern struct tm timeinfo;

// Function declarations
void initializeWifi();
void initializeTime();
long getSecondsTillNextImage(long delta, long deltaSinceTimeObtain);

#endif // TIME_UTILS_H