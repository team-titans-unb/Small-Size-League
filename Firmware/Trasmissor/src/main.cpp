    #include <Arduino.h>
    #include <SPI.h>
    #include <nRF24L01.h>
    #include <RF24.h>

    // Pinos CE e CSN (ajuste conforme seu hardware)
    #define CE_PIN PB0
    #define CSN_PIN PA4

    RF24 radio(CE_PIN, CSN_PIN);

    // Endereços diferentes para cada robô
    const byte addresses[][6] = {"Robo1", "Robo2", "Robo3"};

    const size_t PACKET_SIZE = 10; // robot_id + 9 bytes de comando
    uint8_t packetBuffer[PACKET_SIZE];

    void setup() {
        Serial.begin(115200);
        Serial.println("ESP Head pronta - aguardando pacotes via Serial");

        if (!radio.begin()) {
            Serial.println("Falha ao iniciar o radio!");
            while (1) {}
        }

        radio.setPALevel(RF24_PA_LOW);
        radio.stopListening(); // transmissor
        Serial.println("NRF24 pronto.");
    }

    void sendToRobot(uint8_t robot_id, uint8_t* buffer) {
        if (robot_id < 1 || robot_id > 3) {
            Serial.print("Robot_id inválido: ");
            Serial.println(robot_id);
            return;
        }

        // Abre o pipe correspondente
        radio.openWritingPipe(addresses[robot_id - 1]);

        bool ok = radio.write(buffer, PACKET_SIZE);
        if (ok) {
            Serial.print("Pacote enviado para Robo ");
            Serial.println(robot_id);
        } else {
            Serial.print("Falha ao enviar para Robo ");
            Serial.println(robot_id);
        }
    }

    void loop() {
        Serial.println("Aguardando pacote..l.");
        // Verifica se chegou pacote pela Serial
        if (Serial.available() >= PACKET_SIZE) {
            // Lê exatamente PACKET_SIZE bytes
            Serial.readBytes((char*)packetBuffer, PACKET_SIZE);

            uint8_t robot_id = packetBuffer[0]; // Primeiro byte = destino
            sendToRobot(robot_id, packetBuffer);
        }
    }
