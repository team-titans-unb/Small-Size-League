#ifndef ROBOT_CONTROLLER_H
#define ROBOT_CONTROLLER_H

#include "../robot/robot.h"
#include "../communication/network_protocol.h"

void handlePacket(Robot& robot, const MessagePacket& packet);

#endif