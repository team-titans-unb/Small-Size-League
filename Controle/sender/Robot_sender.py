FWD = 0
BWD = 1
class RobotSender:
    """
    Abstract interface for sending commands to a robot.
    """
    def send_command(self, fl_s, fl_d, bl_s, bl_d, fr_s, fr_d, br_s, br_d, kicker=False):
        """
        Sends a command to the robot.

        wheel_speeds: dict with keys:
            fl_speed, fl_direction, bl_speed, bl_direction, fr_speed, fr_direction, br_speed, br_direction
        kicker: True/False
        """
        raise NotImplementedError("This method should be implemented in subclasses")

    def motor_test(self, motors, direction=FWD, speed=250, kicker=False):
        """
        Returns a command tuple for a single motor or multiple motors.
        
        motor: str ("fl", "fr", "bl", "br") ou int (1=fl,2=fr,3=bl,4=br)
        direction: 0=forward, 1=backward
        speed: motor speed 0-255
        kicker: True/False
        """
        cmd = [0,0,0,0,0,0,0,0,kicker]
        motor_map = {
            "fl": (0,1), 1: (0,1),
            "bl": (2,3), 3: (2,3),
            "fr": (4,5), 2: (4,5),
            "br": (6,7), 4: (6,7)
        }
        if not isinstance(motors, list):
            motors = [motors]
        for m in motors:
            if m not in motor_map:
                raise ValueError(f"Invalid motor: {m}")
            idx_speed, idx_dir = motor_map[m]
            cmd[idx_speed] = speed
            cmd[idx_dir] = direction
        return tuple(cmd)
