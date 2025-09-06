#ifndef CONFIG_H
#define CONFIG_H

struct MotorPins {
    int in1_pin;
    int in2_pin;
    int channel1;
    int channel2;
};

struct RobotConfig {
    MotorPins frontLeft;
    MotorPins backLeft;
    MotorPins frontRight;
    MotorPins backRight;
    int kickerPin;
};

enum RobotID {
    ALVIN,
    SIMON,
    THEODORE
};

// PINS FOR ALVIN
const RobotConfig ALVIN_CONFIG = {
    .frontLeft  = {26, 25, 0, 1}, // {IN1, IN2, CHAN1, CHAN2}
    .backLeft   = {21, 19, 2, 3},
    .frontRight = {32, 33, 4, 5},
    .backRight  = {4, 18, 6, 7},
    .kickerPin  = 27
};

// PINS FOR SIMON
const RobotConfig SIMON_CONFIG = {
    .frontLeft  = {26, 25, 0, 1}, // {IN1, IN2, CHAN1, CHAN2}
    .backLeft   = {21, 19, 2, 3},
    .frontRight = {32, 33, 4, 5},
    .backRight  = {4, 18, 6, 7},
    .kickerPin  = 27
};

// PINS FOR THEODORE
const RobotConfig THEODORE_CONFIG = {
    .frontLeft  = {26, 25, 0, 1}, // {IN1, IN2, CHAN1, CHAN2}
    .backLeft   = {21, 19, 2, 3},
    .frontRight = {32, 33, 4, 5},
    .backRight  = {4, 18, 6, 7},
    .kickerPin  = 27
};

#define NETWORK                 "labmicro"
#define PASSWORD                "l@bm!cro2023"
#define PORT                    8080

#define WHEEL_DIAMETER_MM       60

#endif