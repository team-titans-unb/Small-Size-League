#include <Arduino.h>
#include "communication.h"

Communication::Communication(const char* ssid, const char* password, int port)
    : _ssid(ssid), _password(password), _port(port) {}

void Communication::begin() {
    Serial.print("Conectando-se a ");
    Serial.println(_ssid);

    WiFi.begin(_ssid, _password);
    int attempts = 0;
    while (WiFi.status() != WL_CONNECTED && attempts < 20) {
        delay(500);
        Serial.print(".");
        attempts++;
    }

    if (WiFi.status() == WL_CONNECTED) {
        Serial.println("\nWiFi conectado!");
        Serial.print("Endereco IP: ");
        Serial.println(WiFi.localIP());

        if (Udp.begin(_port)) {
            Serial.print("UDP escutando na porta ");
            Serial.println(_port);
        } else {
            Serial.println("Falha ao iniciar UDP!");
        }
    } else {
        Serial.println("\nFalha ao conectar ao WiFi!");
    }
}

bool Communication::receivePacket(uint8_t* buffer, size_t bufferSize) {
    int packetSize = Udp.parsePacket();
    if (packetSize) {
        _remoteIP = Udp.remoteIP();
        _remotePort = Udp.remotePort();

        int len = Udp.read(buffer, bufferSize);
        if (len > 0) {
            if (len < bufferSize) {
                memset(buffer + len, 0, bufferSize - len);
            }
            return true;
        }
    }
    return false;
}

IPAddress Communication::getRemoteIP() {
    return _remoteIP;
}

int Communication::getRemotePort() {
    return _remotePort;
}