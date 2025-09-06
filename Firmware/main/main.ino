#include "robot/robot.h"
#include "communication/communication.h"
#include "config.h"

const RobotID CURRENT_ROBOT = SIMON;

Robot ssl(CURRENT_ROBOT);

Communication messenger(NETWORK, PASSWORD, PORT);

const size_t UDP_PACKET_SIZE = 9;
struct __attribute__((packed)) MessagePacket {
    uint8_t setPointFL;
    uint8_t directionFL;
    uint8_t setPointFR;
    uint8_t directionFR;
    uint8_t setPointBL;
    uint8_t directionBL;
    uint8_t setPointBR;
    uint8_t directionBR;
    uint8_t kickerCommand; // Use 1 for kick, 0 for no kick
};

static_assert(sizeof(MessagePacket) == UDP_PACKET_SIZE, "MessagePacket size mismatch!");

unsigned long lastPacketTime = 0;

void setup() {
    Serial.begin(19200);
    ssl.initializeRobot();
    messenger.begin();
    Serial.println("Robo SSL inicializado e aguardando dados UDP!");
}

void loop() {
    MessagePacket packet;
    if (messenger.receivePacket(reinterpret_cast<uint8_t*>(&packet), sizeof(packet))) {
        lastPacketTime = millis();
        
        ssl.setMotorFL(packet.setPointFL, packet.directionFL);
        ssl.setMotorBL(packet.setPointBL, packet.directionBL);
        ssl.setMotorFR(packet.setPointFR, packet.directionFR);
        ssl.setMotorBR(packet.setPointBR, packet.directionBR);

        if (packet.kickerCommand == 1) {
            ssl.kick();
        }
    }
    if (millis() - lastPacketTime > 500) {
        ssl.StopAllMotors();
    }
}
