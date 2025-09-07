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

struct NetworkConfig {
    const char* ssid;
    const char* password;
    int port;
};

// --- AVAILABLE NETWORK CONFIGURATIONS ---
const NetworkConfig LAB_WIFI_CONFIG = { "labmicro", "l@bm!cro2023", 8080 };
// ...
// Add a new one? Just add it here! No other files need to change. (Except main.ino to choose which one to use)
const NetworkConfig MOBILE_HOTSPOT_CONFIG = { "MyPhone", "12345678", 9000 }; // Example

#define WHEEL_DIAMETER_MM       60

#endif