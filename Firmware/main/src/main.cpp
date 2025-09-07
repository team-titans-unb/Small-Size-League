#include <Arduino.h>
#include <robot.h>
#include <communication.h>
#include <network_protocol.h>
#include <robot_controller.h>
#include <config.h>

// --- Configuration Section ---
const RobotID CURRENT_ROBOT = SIMON; // Change to ALVIN, SIMON, or THEODORE
Robot robot(CURRENT_ROBOT);

Communication messenger(LAB_WIFI_CONFIG);
// --- End Configuration Section ---

unsigned long lastPacketTime = 0;

void setup() {
    Serial.begin(19200);
    robot.initializeRobot();
    messenger.begin();
    Serial.println("Robot ready and waiting for commands...");
}

/**
 * Main loop function
 * 
 * - Continuously checks for incoming message packets.
 * - If a packet is received, updates the timestamp and dispatches the packet to the robot controller.
 * - If no packet is received for more than 500 milliseconds, stops all robot motors as a safety measure.
 */
void loop() {
    MessagePacket packet;
    if (messenger.receivePacket(packet)) {
        lastPacketTime = millis();
        handlePacket(robot, packet);
    }
    if (millis() - lastPacketTime > 500) {
        robot.stopAllMotors();
    }
}