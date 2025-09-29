#include <Arduino.h>
#include <RF24.h>

const uint8_t HEADER[2] = {0xAA, 0x55};
const uint8_t TAIL = 0xFF;
const uint8_t PACKET_LEN = 13; //  Header 1 e 2 + ID(1)+9 dados+checksum(1)+tail(1)
const uint8_t BUFFER_SIZE = 64;

uint8_t buffer[BUFFER_SIZE];
uint8_t head = 0;     // próximo byte a escrever
uint8_t tail_idx = 0; // próximo byte a processar

#define CE_PIN PB0
#define CSN_PIN PA4

RF24 radio(CE_PIN, CSN_PIN);
const byte RADIO_ADDRESS[6] = {'R','o','b','o','1'};

void processBuffer();
uint8_t calc_sum();
uint8_t buffer_len();
void sendToRobot(uint8_t* buffer);

void setup() {
    Serial.begin(115200);
    Serial.println("Iniciando...");
    
    if (!radio.begin()) {
        Serial.println("Radio hardware not responding!");
        while (1);
    }
  
  radio.openWritingPipe(RADIO_ADDRESS); // Set the address to send to
  radio.setPALevel(RF24_PA_LOW); // Power level: LOW, MED, HIGH, MAX
  radio.stopListening(); 
}

void loop() {
    // lê bytes da Serial e coloca no buffer circular
    while (Serial.available()) {
        buffer[head] = Serial.read();
        head = (head + 1) % BUFFER_SIZE; 
        // se o buffer circular estiver cheio, avança tail para não sobrescrever dados
        if (head == tail_idx) {
            tail_idx = (tail_idx + 1) % BUFFER_SIZE;
        }
    }

    processBuffer();
}

void sendToRobot(uint8_t* buffer) {
    bool ok = radio.write(buffer, PACKET_LEN);

    if (!ok) {
        Serial.println("[ERRO] Falha ao enviar via rádio!");
    } else {
        Serial.println("[OK] Pacote enviado com sucesso via rádio!");
    }
}

uint8_t calc_sum(uint8_t* data, uint8_t len) {
    uint8_t sum = 0;
    for (uint8_t i = 0; i < len; i++) sum += data[i];
    return sum % 256;
}

// retorna número de bytes válidos no buffer
uint8_t buffer_len() {
    if (head >= tail_idx) return head - tail_idx;
    return BUFFER_SIZE - tail_idx + head;
}

void processBuffer() {
    while (buffer_len() >= PACKET_LEN) {
        uint8_t idx0 = tail_idx;
        uint8_t idx1 = (tail_idx + 1) % BUFFER_SIZE;

        // verifica header
        if (buffer[idx0] == HEADER[0] && buffer[idx1] == HEADER[1]) {
            Serial.println("Header válido");
            uint8_t checksum_idx = (tail_idx + PACKET_LEN - 1) % BUFFER_SIZE; // tail_idx + 11
            uint8_t tail_packet_idx = (tail_idx + PACKET_LEN) % BUFFER_SIZE; // tail_idx + 12

            if (buffer[tail_packet_idx] == TAIL) {
                Serial.println("Tail válido");
                // extrai dados
                uint8_t data[9];
                uint8_t packetBuffer[PACKET_LEN];

                Serial.print("Pacote: ");
                for (uint8_t i = 0; i < PACKET_LEN; i++){
                    packetBuffer[i] = buffer[(tail_idx + i) % BUFFER_SIZE];
                    Serial.print(packetBuffer[i]); Serial.print(" ");
                }
                Serial.println();
                for (uint8_t i = 0; i < 9; i++)
                    data[i] = buffer[(tail_idx + 3 + i) % BUFFER_SIZE];

                    uint8_t checksum = buffer[checksum_idx];
                    uint8_t calc_checksum = calc_sum(data, 9);
                    Serial.print("Checksum recebido: ");
                    Serial.println(checksum);
                    Serial.print("Checksum calculado: ");
                    Serial.println(calc_checksum);

                if (checksum == calc_checksum) {

                    uint8_t robot_id = buffer[(tail_idx + 2) % BUFFER_SIZE];
                    Serial.print("Pacote válido! ID=");
                    Serial.print(robot_id);
                    Serial.print(" Dados=");
                    for (uint8_t i = 0; i < 9; i++) {
                        Serial.print(data[i]);
                        Serial.print(" ");
                    }
                    Serial.println();
                    
                    sendToRobot(packetBuffer);
                }
                else{
                    Serial.println("Checksum inválido");
                }
                // avança tail pelo tamanho do pacote
                tail_idx = (tail_idx + PACKET_LEN) % BUFFER_SIZE;

            } else {
                // tail inválido → descarta primeiro byte
                tail_idx = (tail_idx + 1) % BUFFER_SIZE;
            }

        } else {
            // header inválido → descarta primeiro byte
            tail_idx = (tail_idx + 1) % BUFFER_SIZE;
        }
    }
}
