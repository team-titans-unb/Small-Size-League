#include <RadioCommunication.h>
#include <SPI.h>

RadioCommunication::RadioCommunication(RF24& radio, const byte* address)
    : _radio(radio), _address(address) {}

void RadioCommunication::begin() {
    Serial.println("Iniciando comunicacao via radio...");

    if (!_radio.begin()) {
        Serial.println("Falha ao iniciar o radio! Verifique a fiacao.");
        while (1){}
    }

    _radio.openReadingPipe(1, _address);
    _radio.setPALevel(RF24_PA_LOW);     
    _radio.startListening();             
    Serial.println("Radio pronto para receber pacotes.");
    _radio.printDetails(); 
}

bool RadioCommunication::receivePacket(void* buffer, size_t bufferSize) {
    if (_radio.available()) {
        _radio.read(buffer, bufferSize);
        return true;
    }
    return false;
}