#ifndef WIFI_CONFIG_H
#define WIFI_CONFIG_H

#include <WiFi.h>
#include <WebServer.h>
#include <DNSServer.h>
#include <Preferences.h>
#include <SPIFFS.h>

class WiFiConfig {
private:
    WebServer server;
    DNSServer dnsServer;
    Preferences preferences;
    
    const char* ap_ssid = "E-Paper Frame Setup";
    const char* ap_password = "12345678";
    const char* custom_domain = "frame.local";
    const int dns_port = 53;
    const int web_port = 80;
    
    bool isConfigured = false;
    bool isConnected = false;
    
    // HTML for the configuration page
    const char* config_html = R"rawliteral(
<!DOCTYPE html>
<html>
<head>
    <title>E-Paper Frame Setup</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            width: 100%;
            max-width: 400px;
        }
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 30px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            color: #555;
            font-weight: bold;
        }
        input, select {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            box-sizing: border-box;
            transition: border-color 0.3s;
        }
        input:focus, select:focus {
            outline: none;
            border-color: #667eea;
        }
        button {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.2s;
        }
        button:hover {
            transform: translateY(-2px);
        }
        .status {
            margin-top: 20px;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            font-weight: bold;
        }
        .success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        .loading {
            background: #d1ecf1;
            color: #0c5460;
            border: 1px solid #bee5eb;
        }
        .networks {
            max-height: 200px;
            overflow-y: auto;
            border: 2px solid #ddd;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        .network-item {
            padding: 10px;
            border-bottom: 1px solid #eee;
            cursor: pointer;
            transition: background-color 0.2s;
        }
        .network-item:hover {
            background-color: #f8f9fa;
        }
        .network-item:last-child {
            border-bottom: none;
        }
        .refresh-btn {
            background: #28a745;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📱 E-Paper Frame Setup</h1>
        
        <div id="status" class="status" style="display: none;"></div>
        
        <form id="wifiForm">
            <div class="form-group">
                <label for="ssid">WiFi Network:</label>
                <button type="button" class="refresh-btn" onclick="scanNetworks()">🔄 Scan Networks</button>
                <div id="networks" class="networks" style="display: none;"></div>
                <input type="text" id="ssid" name="ssid" placeholder="Enter WiFi network name" required>
            </div>
            
            <div class="form-group">
                <label for="password">Password:</label>
                <input type="password" id="password" name="password" placeholder="Enter WiFi password" required>
            </div>
            
            <button type="submit">Connect to WiFi</button>
        </form>
    </div>

    <script>
        function showStatus(message, type) {
            const status = document.getElementById('status');
            status.textContent = message;
            status.className = 'status ' + type;
            status.style.display = 'block';
        }

        function scanNetworks() {
            showStatus('Scanning for networks...', 'loading');
            fetch('/scan')
                .then(response => response.json())
                .then(data => {
                    const networksDiv = document.getElementById('networks');
                    networksDiv.innerHTML = '';
                    
                    if (data.networks && data.networks.length > 0) {
                        data.networks.forEach(network => {
                            const item = document.createElement('div');
                            item.className = 'network-item';
                            item.textContent = network.ssid + ' (' + network.rssi + ' dBm)';
                            item.onclick = () => {
                                document.getElementById('ssid').value = network.ssid;
                                networksDiv.style.display = 'none';
                            };
                            networksDiv.appendChild(item);
                        });
                        networksDiv.style.display = 'block';
                        showStatus('Found ' + data.networks.length + ' networks', 'success');
                    } else {
                        showStatus('No networks found', 'error');
                    }
                })
                .catch(error => {
                    showStatus('Error scanning networks', 'error');
                });
        }

        document.getElementById('wifiForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const data = {
                ssid: formData.get('ssid'),
                password: formData.get('password')
            };
            
            showStatus('Connecting to WiFi...', 'loading');
            
            fetch('/connect', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showStatus('Connected successfully! Device will restart...', 'success');
                    setTimeout(() => {
                        showStatus('Restarting device...', 'loading');
                    }, 2000);
                } else {
                    showStatus('Connection failed: ' + data.message, 'error');
                }
            })
            .catch(error => {
                showStatus('Connection error', 'error');
            });
        });

        // Auto-scan on page load
        window.onload = function() {
            scanNetworks();
        };
    </script>
</body>
</html>
    )rawliteral";

public:
    WiFiConfig();
    void begin();
    bool isWiFiConfigured();
    bool connectToWiFi();
    void startCaptivePortal();
    void handleClient();
    void stopCaptivePortal();
    void saveWiFiCredentials(const String& ssid, const String& password);
    void clearWiFiCredentials();
};

#endif 