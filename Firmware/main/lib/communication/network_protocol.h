#ifndef NETWORK_PROTOCOL_H
#define NETWORK_PROTOCOL_H

#include <stdint.h>

const size_t UDP_PACKET_SIZE = 9;

// A command for a single motor
struct __attribute__((packed)) MotorCommand {
    uint8_t setPoint;
    uint8_t direction;
};

// The main packet, composed of smaller, logical parts
struct __attribute__((packed)) MessagePacket {
    MotorCommand frontLeft;
    MotorCommand frontRight;
    MotorCommand backLeft;
    MotorCommand backRight;
    uint8_t      kickerCommand;
};

// This safety check ensures the memory size is correct for the network
static_assert(sizeof(MessagePacket) == UDP_PACKET_SIZE, "MessagePacket size mismatch!");

#endif // NETWORK_PROTOCOL_H