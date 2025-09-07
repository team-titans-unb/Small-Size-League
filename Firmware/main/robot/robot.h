#ifndef Robot_h
#define Robot_h

#include <Arduino.h>
#include "../motor_control/motor.h"
#include "../config.h"

class Robot {
public:
    explicit Robot(RobotID id);

    void initializeRobot();

    void setMotorFL(int speed, int direction);
    void setMotorBL(int speed, int direction);
    void setMotorFR(int speed, int direction);
    void setMotorBR(int speed, int direction);

    void kick();
    void stopAllMotors();

private:
    explicit Robot(const RobotConfig& config);
    Motor motorFL;
    Motor motorBL;
    Motor motorFR;
    Motor motorBR;

    uint8_t _kickerPin;
};

#endif