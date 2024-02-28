#include <FS.h>
#include <SD.h>
#include <SPI.h>

#define SD_CS_PIN 2 // Change this to match your SD card CS pin!

void setup(){
  Serial.begin(115200);
  if(!SD.begin(SD_CS_PIN)){
    Serial.println("Card Mount Failed");
    return;
  }
  File file = SD.open("/test.txt");
  if(!file){
    Serial.println("Failed to open file for reading");
    return;
  }
  
  Serial.println("File Content:");
  while(file.available()){
    Serial.write(file.read());
  }
  file.close();
}

void loop(){

}