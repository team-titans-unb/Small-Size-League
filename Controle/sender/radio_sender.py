import serial
import time

from Robot_sender import RobotSender

FWD = 0
BWD = 1

class RadioSender(RobotSender):
    def __init__(self, robot_id, port, baudrate=115200):
        self.robot_id = robot_id
        self.ser = serial.Serial(port, baudrate, timeout=1)
        self.packet_size = 10
        time.sleep(1)
        print(f"RadioSender configured: via {port}@{baudrate}")

    def send_command(self, fl_s, fl_d, bl_s, bl_d, fr_s, fr_d, br_s, br_d, kicker):
        fl_s = max(0, min(255, int(fl_s)))
        fl_d = max(0, min(1, int(fl_d)))
        bl_s = max(0, min(255, int(bl_s)))
        bl_d = max(0, min(1, int(bl_d)))
        fr_s = max(0, min(255, int(fr_s)))
        fr_d = max(0, min(1, int(fr_d)))
        br_s = max(0, min(255, int(br_s)))
        br_d = max(0, min(1, int(br_d)))
        kicker_byte = 1 if kicker else 0

        # monta pacote
        packet = bytearray([
            self.robot_id,
            fl_s, fl_d,
            bl_s, bl_d,
            fr_s, fr_d,
            br_s, br_d,
            kicker_byte
        ])

        try:
            self.ser.write(packet)
            print(f"Pacote enviado p/ robô {self.robot_id}: {packet.hex()}")
        except Exception as e:
            print(f"Erro ao enviar pacote via serial: {e}")


if __name__ == "__main__":
    SERIAL_PORT = "/dev/ttyACM0"
    ROBOT_ID = 1
    sender = RadioSender(ROBOT_ID, SERIAL_PORT)

    # Exemplo: mover front-left para frente
    cmd = sender.motor_test("fl", FWD)
    sender.send_command(*cmd)  # <- aqui desempacota a tupla

    # Exemplo: mover front-left e back-right para trás
    cmd2 = sender.motor_test([1,4], BWD)
    sender.send_command(*cmd2)

    # Exemplo: chute com front-left
    cmd3 = sender.motor_test("fl", FWD, kicker=True)
    sender.send_command(*cmd3)
