/*
  This example connects to an unencrypted WiFi network.
  Then it prints the MAC address of the WiFi module,
  the IP address obtained, and other network details.

  created 13 July 2010
  by dlf (Metodo2 srl)
  modified 31 May 2012
  by Tom Igoe

  Find the full UNO R4 WiFi Network documentation here:
  https://docs.arduino.cc/tutorials/uno-r4-wifi/wifi-examples#connect-with-wpa
 */
#include <WiFiS3.h>
// #include <AsyncTCP.h>
#include "arduino_secrets.h"
///////please enter your sensitive data in the Secret tab/arduino_secrets.h

char ssid[] = SECRET_SSID;  // your network SSID (name)
char pass[] = SECRET_PASS;  // your network password (use for WPA, or use as key for WEP)
int sensorData = 0;
int status = WL_IDLE_STATUS;  // the WiFi radio's status
WiFiServer server(80);        // create webserver listening on port 80

#define WIFI_SSID = SECRET_SSID

// Function prototypes
void printCurrentNet();
void printWifiData();
void printMacAddress(byte mac[]);

extern "C" char* sbrk(int i);  // System call for managing heap on ARM-based systems

int getFreeRam() {
    char top;
    return &top - sbrk(0);  // Estimate free RAM
}

void printWifiData() {
    // print your board's IP address:
    IPAddress ip = WiFi.localIP();
    Serial.print("IP Address: ");

    Serial.println(ip);

    // print your MAC address:
    byte mac[6];
    WiFi.macAddress(mac);
    Serial.print("MAC address: ");
    printMacAddress(mac);
}

void printCurrentNet() {
    // print the SSID of the network you're attached to:
    Serial.print("SSID: ");
    Serial.println(WiFi.SSID());

    // print the MAC address of the router you're attached to:
    byte bssid[6];
    WiFi.BSSID(bssid);
    Serial.print("BSSID: ");
    printMacAddress(bssid);

    // print the received signal strength:
    long rssi = WiFi.RSSI();
    Serial.print("signal strength (RSSI):");
    Serial.println(rssi);

    // print the encryption type:
    byte encryption = WiFi.encryptionType();
    Serial.print("Encryption Type:");
    Serial.println(encryption, HEX);
    Serial.println();
}

void printMacAddress(byte mac[]) {
    for (int i = 0; i < 6; i++) {
        if (i > 0) {
            Serial.print(":");
        }
        if (mac[i] < 16) {
            Serial.print("0");
        }
        Serial.print(mac[i], HEX);
    }
    Serial.println();
}

void setup() {
    // Initialize serial and wait for port to open:
    Serial.begin(9600);
    while (!Serial) {
        ;  // wait for serial port to connect. Needed for native USB port only
    }

    // check for the WiFi module:
    if (WiFi.status() == WL_NO_MODULE) {
        Serial.println("Communication with WiFi module failed!");
        // don't continue
        while (true)
            ;
    }

    String fv = WiFi.firmwareVersion();
    if (fv < WIFI_FIRMWARE_LATEST_VERSION) {
        Serial.println("Please upgrade the firmware");
    }

    // attempt to connect to WiFi network:
    while (status != WL_CONNECTED) {
        Serial.print("Attempting to connect to WPA SSID: ");
        Serial.println(ssid);
        // Connect to WPA/WPA2 network:
        status = WiFi.begin(ssid, pass);

        // wait 10 seconds for connection:
        delay(10000);
    }

    // you're connected now, so print out the data:
    Serial.print("You're connected to the network");
    printCurrentNet();
    printWifiData();

    // Start the webserver
    server.begin();
}

void loop() {
    // check the network connection once every 10 seconds: DISABLED BECAUSE SPAM
    // delay(10000);
    // printCurrentNet();

    WiFiClient client = server.available();
    if (client) {
        // Get the request type out of the HTTP request. (Should be /sensor or /stats)
        String request = client.readStringUntil('\r');
        client.read();  // consume '\n'

        int firstSpace = request.indexOf(' ');
        int secondSpace = request.indexOf(' ', firstSpace + 1);

        String path = request.substring(firstSpace + 1, secondSpace);
        path.trim();

        if (path == "/sensor") {
            // Grab the sensor data.
            sensorData = analogRead(A0);

            client.print("HTTP/1.1 200 OK\r\n");
            client.print("Content-Type: application/json\r\n");
            client.print("Connection: close\r\n");
            client.print("\r\n");
            client.print("{\"sensor\": ");
            client.print(sensorData);
            client.print("}");

        } else if (path == "/stats") {
            int wifiStrength = WiFi.RSSI();
            int freeRam = getFreeRam();

            client.print("HTTP/1.1 200 OK\r\n");
            client.print("Content-Type: application/json\r\n");
            client.print("Connection: close\r\n");
            client.print("\r\n");

            client.print("{");
            client.print("\"wifiStrength\": ");
            client.print(wifiStrength);
            client.print(", \r\n");

            client.print("\"freeRam\": ");
            client.print(freeRam);
            client.print("}");

        } else {
            // Send 404 for unknown endpoints
            client.println("HTTP/1.1 404 Not Found\r\n");
            client.println("Content-Type: application/json\r\n");
            client.println("Connection: close\r\n");
            client.println("\r\n");
            client.println("{\"error\": \"Unknown endpoint\"}");
        }
        client.stop();
    }
}
