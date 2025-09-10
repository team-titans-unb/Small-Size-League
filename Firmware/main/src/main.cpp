#include <Arduino.h>
#include <robot.h>
#include <communication.h>
#include <network_protocol.h>
#include <robot_controller.h>
#include <RadioCommunication.h>
#include <config.h>
#include <RF24.h>

const RobotID CURRENT_ROBOT = SIMON;
Robot robot(CURRENT_ROBOT);

// NRF24
RF24 radio(2, 5);
const byte RADIO_ADDRESS[6] = "Robo"; 
RadioCommunication messenger(radio, RADIO_ADDRESS);

// --- Estrutura do pacote ---
struct CommandPacket {
    uint8_t robot_id;
    uint8_t fl_s, fl_d;
    uint8_t bl_s, bl_d;
    uint8_t fr_s, fr_d;
    uint8_t br_s, br_d;
    uint8_t kicker;
};

const size_t PACKET_SIZE = sizeof(CommandPacket);
CommandPacket packet;

unsigned long lastPacketTime = 0;

void setup() {
    Serial.begin(115200);
    robot.initializeRobot();
    messenger.begin();
    Serial.println("Robot pronto e aguardando comandos...");
}

// Função para processar o pacote de forma segura
void processPacket(const CommandPacket& pkt) {
    if (pkt.robot_id != CURRENT_ROBOT) return;

    lastPacketTime = millis();

    // Debug resumido
    Serial.print("Pacote recebido p/ Robo "); Serial.println(pkt.robot_id);
    Serial.print("FL: "); Serial.print(pkt.fl_s); Serial.print(" dir="); Serial.print(pkt.fl_d);
    Serial.print(" | BL: "); Serial.print(pkt.bl_s); Serial.print(" dir="); Serial.print(pkt.bl_d);
    Serial.print(" | FR: "); Serial.print(pkt.fr_s); Serial.print(" dir="); Serial.print(pkt.fr_d);
    Serial.print(" | BR: "); Serial.print(pkt.br_s); Serial.print(" dir="); Serial.println(pkt.br_d);
    Serial.print("Kicker: "); Serial.println(pkt.kicker);

    // Comandos aos motores (descomentar quando estiver pronto)
    /*
    robot.setMotorSpeed(FRONT_LEFT,  pkt.fl_s, pkt.fl_d);
    robot.setMotorSpeed(BACK_LEFT,   pkt.bl_s, pkt.bl_d);
    robot.setMotorSpeed(FRONT_RIGHT, pkt.fr_s, pkt.fr_d);
    robot.setMotorSpeed(BACK_RIGHT,  pkt.br_s, pkt.br_d);
    if (pkt.kicker) robot.kick();
    */
}

void loop() {
    // Recebe pacote do rádio
    if (messenger.receivePacket((uint8_t*)&packet, PACKET_SIZE)) {

        // Verifica se o pacote é para este robô
        if (packet.robot_id != 2) {
            Serial.println("Pacote fora de sincronia, ignorando...");
            return;
        }
        processPacket(packet);
    }

    // Failsafe: se passar 500ms sem pacote, parar os motores
    if (millis() - lastPacketTime > 500) {
        // robot.stopAllMotors(); // descomentar quando estiver pronto
    }
}
