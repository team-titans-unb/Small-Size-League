from more_itertools import tail
import serial

FWD = 0
BWD = 1
tx_port = "/tmp/ttyV0"

class RadioSender():
    def __init__(self, robot_id=3, port="/dev/ttyACM0", baudrate=115200):
        self.robot_id = robot_id
        self.packet_size = 10
        self.serial = serial.Serial(port, baudrate, timeout=1)

    def build_packet(self, fl_s, fl_d, bl_s, bl_d, fr_s, fr_d, br_s, br_d, kicker):
        
        # Headers
        packet = bytearray([0xAA, 0x55])
        tail = 0xFF
        packet.append(self.robot_id)
        
        # Validate motor speeds and directions
        fl_s = max(0, min(255, int(fl_s)))
        fl_d = 1 if fl_d else 0
        bl_s = max(0, min(255, int(bl_s)))
        bl_d = 1 if bl_d else 0
        fr_s = max(0, min(255, int(fr_s)))
        fr_d = 1 if fr_d else 0
        br_s = max(0, min(255, int(br_s)))
        br_d = 1 if br_d else 0
        kicker = 1 if kicker else 0

        data = [fl_s, fl_d, fr_s, fr_d, bl_s, bl_d, br_s, br_d, kicker]
        for value in data:
            packet.append(value)
    
        # Calculate checksum
        checksum = sum(data) % 256
        packet.append(checksum)
        packet.append(tail)
        return packet

    def send_command(self, fl_s, fl_d, bl_s, bl_d, fr_s, fr_d, br_s, br_d, kicker):
        packet = self.build_packet(fl_s, fl_d, bl_s, bl_d, fr_s, fr_d, br_s, br_d, kicker)
        self.send_packet(packet)

    def send_packet(self, packet: bytearray):
        self.serial.write(packet)
        self.serial.flush()

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

if __name__ == "__main__":
    sender = RadioSender()
    try:
        while True:
            cmd = sender.motor_test([1,2,3,4], direction=FWD, speed=200)
            sender.send_command(*cmd)
    except KeyboardInterrupt:
        print("Encerrando...")