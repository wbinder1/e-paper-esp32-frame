#ifndef TIME_UTILS_H
#define TIME_UTILS_H

#include <WiFi.h>
#include <ezTime.h>

// External variable declarations
extern const char* ntpServer;
extern const long gmtOffset_sec;
extern const int daylightOffset_sec;
extern bool  timeWorking;

// Function declarations
void initializeTime();
long getSecondsTillNextImage(long delta);

#endif // TIME_UTILS_H