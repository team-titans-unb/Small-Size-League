#include "RadioCommunication.h"
#include <Arduino.h>

#define CHANNE 110
#define DATARATE RF24_250KBPS
RadioCommunication::RadioCommunication(RF24& radio, const byte* address)
    : _radio(radio), _address(address) {}

// Inicializa para receber
void RadioCommunication::beginRX() {
    Serial.println("Iniciando comunicacao via radio...");

    if (!_radio.begin()) {
        Serial.println("Falha ao iniciar o radio! Verifique a fiacao.");
        while (1){}
    }

    _radio.openReadingPipe(1, _address);
    _radio.setPALevel(RF24_PA_HIGH);
    _radio.setDataRate(DATARATE);
    _radio.setChannel(CHANNE);
    _radio.startListening();

    Serial.println("Radio pronto para receber pacotes.");
    _radio.printDetails();
}

// Inicializa para transmitir
void RadioCommunication::beginTX() {
    Serial.println("Iniciando comunicacao via radio...");

    if (!_radio.begin()) {
        Serial.println("Falha ao iniciar o radio!");
        while (1) {}
    }

    _radio.setDataRate(DATARATE);
    _radio.setPALevel(RF24_PA_LOW);
    _radio.setChannel(CHANNE);
    _radio.setRetries(5, 8);

    _radio.openWritingPipe(_address);
    _radio.stopListening();

    Serial.println("Radio pronto para transmitir pacotes.");
    _radio.printDetails();
}

bool RadioCommunication::receivePacket(void* buffer, size_t bufferSize) {
    if (_radio.available()) {
        _radio.read(buffer, bufferSize);
        return true;
    }
    return false;
}
