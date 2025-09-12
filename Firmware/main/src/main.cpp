#include <Arduino.h>
#include <robot.h>
#include <communication.h>
#include <network_protocol.h>
#include <robot_controller.h>
#include "RadioCommunication.h"
#include <config.h>
#include <RF24.h>

const RobotID CURRENT_ROBOT = SIMON;
Robot robot(CURRENT_ROBOT);

#define CE_PIN  2
#define CSN_PIN 5

RF24 radio(CE_PIN, CSN_PIN);
const byte RADIO_ADDRESS[5] = {'R','o','b','o','1'}; 
RadioCommunication messenger(radio, RADIO_ADDRESS);

// --- Estrutura do pacote ---
struct __attribute__((packed)) CommandPacket {
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
    Serial.begin(19200);
    robot.initializeRobot();
    messenger.beginRX();
    Serial.println("Robot pronto e aguardando comandos...");
    Serial.print("I am ");
    Serial.println(robot.getId());
}

void processPacket(const CommandPacket& pkt) {
    lastPacketTime = millis();

    // Debug detalhado
    Serial.print("Pacote recebido. Robo: "); Serial.println(pkt.robot_id);
    Serial.print("FL: "); Serial.print(pkt.fl_s); Serial.print(" dir="); Serial.print(pkt.fl_d);
    Serial.print(" | BL: "); Serial.print(pkt.bl_s); Serial.print(" dir="); Serial.print(pkt.bl_d);
    Serial.print(" | FR: "); Serial.print(pkt.fr_s); Serial.print(" dir="); Serial.print(pkt.fr_d);
    Serial.print(" | BR: "); Serial.print(pkt.br_s); Serial.print(" dir="); Serial.println(pkt.br_d);
    Serial.print("Kicker: "); Serial.println(pkt.kicker);

    // Comandos aos motores
    
    robot.setMotorFL(pkt.fl_s, pkt.fl_d);
    robot.setMotorBL(pkt.bl_s, pkt.bl_d);
    robot.setMotorFR(pkt.fr_s, pkt.fr_d);
    robot.setMotorBR(pkt.br_s, pkt.br_d);
    if (pkt.kicker) robot.kick();
    
}

void loop() {
    if (radio.available()) {
        radio.read(&packet, PACKET_SIZE);

        if (packet.robot_id != robot.getId()){
            Serial.println("Pacote ignorado");
            return;
        } 
        Serial.println("Comando recebido!");
        processPacket(packet);
    }
}
