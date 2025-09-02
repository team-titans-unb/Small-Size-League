#include <Arduino.h>
#include "robot.h"

Robot::Robot(uint8_t pin_FL1, uint8_t pin_FL2, uint8_t channel_FL1, uint8_t channel_FL2,
             uint8_t pin_BL1, uint8_t pin_BL2, uint8_t channel_BL1, uint8_t channel_BL2,
             uint8_t pin_FR1, uint8_t pin_FR2, uint8_t channel_FR1, uint8_t channel_FR2,
             uint8_t pin_BR1, uint8_t pin_BR2, uint8_t channel_BR1, uint8_t channel_BR2,
             uint8_t kickerPin)
    : motorFL(pin_FL1, pin_FL2, channel_FL1, channel_FL2),
      motorBL(pin_BL1, pin_BL2, channel_BL1, channel_BL2),
      motorFR(pin_FR1, pin_FR2, channel_FR1, channel_FR2),
      motorBR(pin_BR1, pin_BR2, channel_BR1, channel_BR2),
      _kickerPin(kickerPin)
{
}

void Robot::initializeRobot() {
    motorFL.begin();
    motorBL.begin();
    motorFR.begin();
    motorBR.begin();

    pinMode(_kickerPin, OUTPUT);
    digitalWrite(_kickerPin, LOW);

    Serial.println("Robot initialized: 4 motors and Kicker pins configured.");
}

void Robot::setMotorFL(int speed, int direction) {
    this->motorFL.move(speed, direction);
}

void Robot::setMotorFR(int speed, int direction) {
    this->motorFR.move(speed, direction);
}

void Robot::setMotorBL(int speed, int direction) {
    this->motorBL.move(speed, direction);
}

void Robot::setMotorBR(int speed, int direction) {
    this->motorBR.move(speed, direction);
}

void Robot::kick() {
    digitalWrite(_kickerPin, HIGH);
    delay(100); // AJUSTE ESTE VALOR COM CUIDADO!
    digitalWrite(_kickerPin, LOW);
    Serial.println("Kicker acionado!");
}

void Robot::StopAllMotors() {
    motorFL.stop();
    motorBL.stop();
    motorFR.stop();
    motorBR.stop();
    Serial.println("All motors stopped.");
}