#ifndef Robot_h
#define Robot_h

#include <Arduino.h>
#include "../motor_control/motor.h"

class Robot {
public:
    Robot(uint8_t pin_FL1, uint8_t pin_FL2, uint8_t channel_FL1, uint8_t channel_FL2,
          uint8_t pin_BL1, uint8_t pin_BL2, uint8_t channel_BL1, uint8_t channel_BL2,
          uint8_t pin_FR1, uint8_t pin_FR2, uint8_t channel_FR1, uint8_t channel_FR2,
          uint8_t pin_BR1, uint8_t pin_BR2, uint8_t channel_BR1, uint8_t channel_BR2,
          uint8_t kickerPin);

    void initializeRobot();

    void setMotorFL(int speed, int direction);
    void setMotorBL(int speed, int direction);
    void setMotorFR(int speed, int direction);
    void setMotorBR(int speed, int direction);

    void kick();
    void StopAllMotors();

private:
    Motor motorFL;
    Motor motorBL;
    Motor motorFR;
    Motor motorBR;

    uint8_t _kickerPin;
};

#endif