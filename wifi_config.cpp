#include "wifi_config.h"
#include <ArduinoJson.h>

WiFiConfig::WiFiConfig() : server(80), dnsServer() {
}

void WiFiConfig::begin() {
    preferences.begin("wifi_config", false);
}

bool WiFiConfig::isWiFiConfigured() {
    String saved_ssid = preferences.getString("wifi_ssid", "");
    String saved_password = preferences.getString("wifi_password", "");
    return (saved_ssid.length() > 0 && saved_password.length() > 0);
}

bool WiFiConfig::connectToWiFi() {
    if (!isWiFiConfigured()) {
        Serial.println("No WiFi credentials stored");
        return false;
    }
    
    String ssid = preferences.getString("wifi_ssid", "");
    String password = preferences.getString("wifi_password", "");
    
    Serial.println("Connecting to WiFi: " + ssid);
    
    WiFi.begin(ssid.c_str(), password.c_str());
    
    int attempts = 0;
    while (WiFi.status() != WL_CONNECTED && attempts < 20) {
        delay(500);
        Serial.print(".");
        attempts++;
    }
    
    if (WiFi.status() == WL_CONNECTED) {
        Serial.println();
        Serial.println("WiFi connected!");
        Serial.println("IP address: " + WiFi.localIP().toString());
        isConnected = true;
        return true;
    } else {
        Serial.println();
        Serial.println("WiFi connection failed");
        isConnected = false;
        return false;
    }
}

void WiFiConfig::startCaptivePortal() {
    Serial.println("Starting Access Point...");
    WiFi.mode(WIFI_AP);
    WiFi.softAP(ap_ssid, ap_password);
    
    Serial.println("Access Point started");
    Serial.println("SSID: " + String(ap_ssid));
    Serial.println("Password: " + String(ap_password));
    Serial.println("IP address: " + WiFi.softAPIP().toString());
    
    // Start DNS server for captive portal with custom domain
    dnsServer.start(dns_port, custom_domain, WiFi.softAPIP());
    
    // Setup web server routes
    server.on("/", HTTP_GET, [this]() {
        server.send(200, "text/html", config_html);
    });
    
    server.on("/scan", HTTP_GET, [this]() {
        Serial.println("Scanning for networks...");
        
        int n = WiFi.scanNetworks();
        DynamicJsonDocument doc(2048);
        JsonArray networks = doc.createNestedArray("networks");
        
        for (int i = 0; i < n; ++i) {
            JsonObject network = networks.createNestedObject();
            network["ssid"] = WiFi.SSID(i);
            network["rssi"] = WiFi.RSSI(i);
            network["encryption"] = WiFi.encryptionType(i);
        }
        
        String response;
        serializeJson(doc, response);
        server.send(200, "application/json", response);
    });
    
    server.on("/connect", HTTP_POST, [this]() {
        String body = server.arg("plain");
        DynamicJsonDocument doc(512);
        deserializeJson(doc, body);
        
        String ssid = doc["ssid"];
        String password = doc["password"];
        
        Serial.println("Attempting to connect to: " + ssid);
        
        // Try to connect
        WiFi.begin(ssid.c_str(), password.c_str());
        
        int attempts = 0;
        while (WiFi.status() != WL_CONNECTED && attempts < 10) {
            delay(1000);
            Serial.print(".");
            attempts++;
        }
        
        DynamicJsonDocument response(256);
        if (WiFi.status() == WL_CONNECTED) {
            Serial.println();
            Serial.println("Connection successful!");
            
            // Save credentials
            saveWiFiCredentials(ssid, password);
            
            response["success"] = true;
            response["message"] = "Connected successfully";
            response["ip"] = WiFi.localIP().toString();
            
            String responseStr;
            serializeJson(response, responseStr);
            server.send(200, "application/json", responseStr);
            
            // Restart after a short delay
            delay(2000);
            ESP.restart();
        } else {
            Serial.println();
            Serial.println("Connection failed");
            
            response["success"] = false;
            response["message"] = "Failed to connect to network";
            
            String responseStr;
            serializeJson(response, responseStr);
            server.send(400, "application/json", responseStr);
        }
    });
    
    // Handle all other requests (captive portal)
    server.onNotFound([this]() {
        server.sendHeader("Location", "http://" + String(custom_domain), true);
        server.send(302, "text/plain", "");
    });
    
    server.begin();
    Serial.println("Web server started");
}

void WiFiConfig::handleClient() {
    dnsServer.processNextRequest();
    server.handleClient();
}

void WiFiConfig::stopCaptivePortal() {
    dnsServer.stop();
    server.close();
    WiFi.softAPdisconnect(true);
    WiFi.mode(WIFI_STA);
}

void WiFiConfig::saveWiFiCredentials(const String& ssid, const String& password) {
    preferences.putString("wifi_ssid", ssid);
    preferences.putString("wifi_password", password);
    Serial.println("WiFi credentials saved");
}

void WiFiConfig::clearWiFiCredentials() {
    preferences.remove("wifi_ssid");
    preferences.remove("wifi_password");
    Serial.println("WiFi credentials cleared");
} 