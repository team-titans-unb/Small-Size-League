#include <Arduino.h>
#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

// Pinos CE e CSN (ajuste conforme seu hardware)
#define CE_PIN PB0
#define CSN_PIN PA4

RF24 radio(CE_PIN, CSN_PIN);

// Endereços diferentes para cada robô
const byte address[6] = "Robo";

const size_t PACKET_SIZE = 10; // robot_id + 9 bytes de comando
uint8_t packetBuffer[PACKET_SIZE];

void setup() {
    Serial.begin(115200);
    Serial.println("STM head pronto - aguardando pacotes via Serial");

    if (!radio.begin()) {
        Serial.println("Falha ao iniciar o radio!");
        while (1) {}
    }
    
    radio.setPALevel(RF24_PA_LOW);
    radio.stopListening(); // transmissor
    Serial.println("NRF24 pronto.");
    radio.openWritingPipe(address);

}

void sendToRobot(uint8_t robot_id, uint8_t* buffer) {
    if (robot_id < 1 || robot_id > 3) {
        Serial.print("Robot_id inválido: ");
        Serial.println(robot_id);
        return;
    }

    bool ok = radio.write(buffer, PACKET_SIZE);
    if (ok) {
        Serial.print("Pacote enviado para Robo ");
    } else {
        Serial.print("Falha ao enviar para Robo ");
    }
}

void loop() {
    //Serial.println("Aguardando pacote via Serial...");
    if (Serial.available() >= PACKET_SIZE) {
        size_t bytesRead = Serial.readBytes((char*)packetBuffer, PACKET_SIZE);
        
        if (bytesRead == PACKET_SIZE) {
            uint8_t robot_id = packetBuffer[0];

            Serial.print("Pacote recebido para Robo ");
            Serial.print(robot_id);
            Serial.print(": ");
            for (int i = 0; i < PACKET_SIZE; i++) {
                Serial.print(packetBuffer[i], HEX);
                Serial.print(" ");
            }
            Serial.println();

            sendToRobot(robot_id, packetBuffer);
        } else {
            Serial.println("Erro: pacote incompleto recebido.");
        }
    }
}
