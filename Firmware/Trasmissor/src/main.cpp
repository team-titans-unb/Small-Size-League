#include <Arduino.h>
#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#include "RadioCommunication.h"

// Pinos CE e CSN (ajuste conforme seu hardware)
#define CE_PIN PB0
#define CSN_PIN PA4

RF24 radio(CE_PIN, CSN_PIN);
const byte RADIO_ADDRESS[6] = {'R','o','b','o','1'};

RadioCommunication radioComm(radio, RADIO_ADDRESS);

const size_t PACKET_SIZE = 10; // robot_id + 9 bytes de comando
uint8_t packetBuffer[PACKET_SIZE];

void setup() {
    Serial.begin(115200);
    Serial.println("STM head pronto - aguardando pacotes via Serial");
    
    radioComm.beginTX();
}

void sendToRobot(uint8_t* buffer) {

    bool ok = radio.write(buffer, PACKET_SIZE);
    if (ok) {
        Serial.println("Sucesso ao enviar!");
    } else {
        Serial.println("Falha no envio!!!!!!");
    }
}

void loop() {
    //Serial.println("Aguardando pacote via Serial...");
    if (Serial.available() >= PACKET_SIZE) {
        size_t bytesRead = Serial.readBytes((char*)packetBuffer, PACKET_SIZE);
        
        if (bytesRead == PACKET_SIZE) {
            uint8_t robot_id = packetBuffer[0];

            Serial.print("Pacote recebido do PC: ");
            for (int i = 0; i < PACKET_SIZE; i++) {
                Serial.print(packetBuffer[i], HEX);
                Serial.print(" ");
            }
            Serial.println();

            sendToRobot(packetBuffer);
        } else {
            Serial.println("Erro: pacote incompleto recebido.");
        }
    }
}
