#include "robot/robot.h"
#include "communication/communication.h"
#include "robot/robot.cpp"
#include "communication/communication.cpp"
#include "motor_control/motor.cpp"
#include "config.h"

volatile int setPointFL = 0, directionFL = 0;
volatile int setPointBL = 0, directionBL = 0;
volatile int setPointFR = 0, directionFR = 0;
volatile int setPointBR = 0, directionBR = 0;
volatile bool kickerCommand = false;

Robot ssl(MOTOR_FRONT_LEFT_IN1, MOTOR_FRONT_LEFT_IN2, ROBOT_CHANEL_FL1, ROBOT_CHANEL_FL2,
              MOTOR_BACK_LEFT_IN1, MOTOR_BACK_LEFT_IN2, ROBOT_CHANEL_BL1, ROBOT_CHANEL_BL2,
              MOTOR_FRONT_RIGHT_IN1, MOTOR_FRONT_RIGHT_IN2, ROBOT_CHANEL_FR1, ROBOT_CHANEL_FR2,
              MOTOR_BACK_RIGHT_IN1, MOTOR_BACK_RIGHT_IN2, ROBOT_CHANEL_BR1, ROBOT_CHANEL_BR2,
              KICKER_SOLENOID_PIN);

Communication messenger(NETWORK, PASSWORD, PORT);

const size_t UDP_PACKET_SIZE = 9;
uint8_t udpPacketBuffer[UDP_PACKET_SIZE];

void setup() {
    Serial.begin(9600);
    ssl.initializeRobot();
    messenger.begin();
    Serial.println("Robo SSL inicializado e aguardando dados UDP!");
}

void loop() {
    if (messenger.receivePacket(udpPacketBuffer, UDP_PACKET_SIZE)) {
        setPointFL = udpPacketBuffer[0];
        directionFL = udpPacketBuffer[1];
        setPointFR = udpPacketBuffer[2];
        directionFR = udpPacketBuffer[3];
        setPointBL = udpPacketBuffer[4];
        directionBL = udpPacketBuffer[5];
        setPointBR = udpPacketBuffer[6];
        directionBR = udpPacketBuffer[7];
        kickerCommand = (udpPacketBuffer[8] == 1);

        Serial.printf("Received from %s:%d\n", messenger.getRemoteIP().toString().c_str(), messenger.getRemotePort());
        Serial.printf("FL: %d (Dir: %d), BL: %d (Dir: %d)\n", setPointFL, directionFL, setPointBL, directionBL);
        Serial.printf("FR: %d (Dir: %d), BR: %d (Dir: %d)\n", setPointFR, directionFR, setPointBR, directionBR);
        Serial.printf("Kicker: %s\n", kickerCommand ? "Sim" : "Nao");

        ssl.setMotorFL(setPointFL, directionFL);
        Serial.printf("Mandado.");
        ssl.setMotorBL(setPointBL, directionBL);
        Serial.printf("Mandado.");
        ssl.setMotorFR(setPointFR, directionFR);
        Serial.printf("Mandado.");
        ssl.setMotorBR(setPointBR, directionBR);
        Serial.printf("Mandado.");

        if (kickerCommand) {
            ssl.kick();
        }
    }
}
