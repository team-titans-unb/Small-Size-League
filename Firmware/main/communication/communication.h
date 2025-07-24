#ifndef COMMUNICATION_H
#define COMMUNICATION_H

#include <WiFi.h>
#include <WiFiUdp.h>

class Communication {
public:
    Communication(const char* ssid, const char* password, int port);

    void begin(); 

    bool receivePacket(uint8_t* buffer, size_t bufferSize);

    IPAddress getRemoteIP();
    int getRemotePort();

private:
    const char* _ssid;
    const char* _password;
    int _port;
    WiFiUDP Udp;
    IPAddress _remoteIP;
    int _remotePort;
};

#endif