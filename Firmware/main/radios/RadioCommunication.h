#ifndef RADIO_COMMUNICATION_H
#define RADIO_COMMUNICATION_H

#include <RF24.h>

class RadioCommunication {
public:
    RadioCommunication(RF24& radio, const byte* address);

    void begin();

    bool receivePacket(void* buffer, size_t bufferSize);

private:
    RF24& _radio;
    const byte* _address;
};

#endif // RADIO_COMMUNICATION_H