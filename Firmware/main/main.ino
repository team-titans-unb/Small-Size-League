#include "robot/robot.h"
#include "communication/communication.h"
#include "config.h"

Robot ssl(MOTOR_FRONT_LEFT_IN1, MOTOR_FRONT_LEFT_IN2, ROBOT_CHANEL_FL1, ROBOT_CHANEL_FL2,
              MOTOR_BACK_LEFT_IN1, MOTOR_BACK_LEFT_IN2, ROBOT_CHANEL_BL1, ROBOT_CHANEL_BL2,
              MOTOR_FRONT_RIGHT_IN1, MOTOR_FRONT_RIGHT_IN2, ROBOT_CHANEL_FR1, ROBOT_CHANEL_FR2,
              MOTOR_BACK_RIGHT_IN1, MOTOR_BACK_RIGHT_IN2, ROBOT_CHANEL_BR1, ROBOT_CHANEL_BR2,
              KICKER_SOLENOID_PIN);

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

void setup() {
    Serial.begin(19200);
    ssl.initializeRobot();
    messenger.begin();
    Serial.println("Robo SSL inicializado e aguardando dados UDP!");
}

void loop() {
    MessagePacket packet;
    if (messenger.receivePacket(reinterpret_cast<uint8_t*>(&packet), sizeof(packet))) {
        Serial.printf("Front-left: %d (Dir: %d), Back-left: %d (Dir: %d)\n", packet.setPointFL, packet.directionFL, packet.setPointBL, packet.directionBL);
        Serial.printf("Front-right: %d (Dir: %d), Back-right: %d (Dir: %d)\n", packet.setPointFR, packet.directionFR, packet.setPointBR, packet.directionBR);
        Serial.printf("Kicker: %s\n", packet.kickerCommand == 1 ? "Sim" : "Nao");
        ssl.setMotorFL(packet.setPointFL, packet.directionFL);
        ssl.setMotorBL(packet.setPointBL, packet.directionBL);
        ssl.setMotorFR(packet.setPointFR, packet.directionFR);
        ssl.setMotorBR(packet.setPointBR, packet.directionBR);

        if (packet.kickerCommand == 1) {
            ssl.kick();
        }
    }
    else {
        ssl.StopAllMotors();
    }
}
