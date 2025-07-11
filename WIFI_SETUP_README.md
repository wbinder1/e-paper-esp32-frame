# WiFi Configuration System

This e-paper frame now includes a user-friendly WiFi configuration system that allows users to easily connect the device to their home network without needing to modify code.

## How It Works

### First-Time Setup
1. **Power on the device** - When the device starts for the first time (or if WiFi credentials are not saved), it will automatically enter setup mode.

2. **Connect to setup network** - The device creates its own WiFi network called "E-Paper Frame Setup" with password "12345678".

3. **Access the setup page** - Connect to the setup network and open a web browser. Navigate to `http://frame.local`.

4. **Configure WiFi** - The web interface will:
   - Scan for available WiFi networks
   - Allow you to select your network
   - Enter your WiFi password
   - Test the connection

5. **Automatic restart** - Once connected successfully, the device will restart and automatically connect to your WiFi network.

### Normal Operation
After initial setup, the device will:
- Automatically connect to your saved WiFi network on startup
- Display images according to the schedule
- Only enter setup mode if the WiFi connection fails

## Files Added

### New Source Files
- `wifi_config.h` - Header file for WiFi configuration class
- `wifi_config.cpp` - Implementation of WiFi configuration functionality
- `setup_image_generator.py` - Python script to generate setup instruction images

### Modified Files
- `e-paper-esp32-frame.ino` - Updated to integrate WiFi configuration system

## Dependencies

You'll need to install the following Arduino libraries:
- `ArduinoJson` by Benoit Blanchon (version 6.x)
- `WebServer` (included with ESP32 board package)
- `DNSServer` (included with ESP32 board package)

## Installation

1. **Install required libraries** in Arduino IDE:
   - Go to Tools → Manage Libraries
   - Search for "ArduinoJson" and install version 6.x

2. **Upload the code** to your ESP32

3. **Generate setup image** (optional):
   ```bash
   python3 setup_image_generator.py
   ```
   This creates a `setup_instructions.bmp` file that you can place on the SD card to show setup instructions on the e-paper display.

## Features

### Web Interface
- **Modern, responsive design** that works on mobile devices
- **Network scanning** - Automatically finds available WiFi networks
- **Signal strength display** - Shows RSSI values for each network
- **Real-time feedback** - Shows connection status and progress
- **Error handling** - Displays helpful error messages if connection fails

### Security
- **Captive portal** - Redirects all web requests to the setup page
- **Secure credential storage** - WiFi credentials are stored in ESP32's non-volatile memory
- **No hardcoded credentials** - No WiFi information in the source code

### User Experience
- **Automatic detection** - Device detects when WiFi setup is needed
- **Seamless transition** - Automatically switches from setup mode to normal operation
- **Persistent configuration** - Credentials are saved and reused on restart
- **Fallback mode** - Returns to setup mode if WiFi connection fails

## Troubleshooting

### Device won't connect to WiFi
1. Check that your WiFi network is 2.4GHz (ESP32 doesn't support 5GHz)
2. Ensure the password is correct
3. Check that your router supports WPA/WPA2 encryption
4. Try moving the device closer to the router

### Setup page won't load
1. Make sure you're connected to the "E-Paper Frame Setup" network
2. Try accessing `http://frame.local` directly
3. Clear your browser cache and try again
4. Try using a different device or browser

### Device keeps restarting
1. Check the Serial Monitor for error messages
2. Ensure the SD card is properly formatted and contains valid images
3. Check that all required libraries are installed

## Advanced Configuration

### Changing Setup Network Details
You can modify the setup network name and password in `wifi_config.h`:
```cpp
const char* ap_ssid = "E-Paper Frame Setup";
const char* ap_password = "12345678";
```

### Clearing Saved Credentials
To force the device back into setup mode, you can clear the saved credentials by adding this code temporarily:
```cpp
wifiConfig.clearWiFiCredentials();
```

### Custom Setup Instructions
Modify `setup_image_generator.py` to create custom setup instruction images with your own branding or additional information.

## Technical Details

### Storage
- WiFi credentials are stored in ESP32's NVS (Non-Volatile Storage)
- Uses the "wifi_config" namespace to avoid conflicts with other preferences

### Network Modes
- **Setup Mode**: Creates an Access Point (AP) for configuration
- **Normal Mode**: Connects to saved WiFi network as a Station (STA)

### Power Management
- The setup mode keeps the device awake to handle web requests
- Normal operation continues to use deep sleep for power efficiency

## Future Enhancements

Potential improvements for future versions:
- **WPS support** for even easier setup
- **QR code generation** for mobile setup
- **Multiple network support** with automatic failover
- **OTA updates** for firmware updates over WiFi
- **Web-based image management** interface 