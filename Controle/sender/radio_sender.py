import serial
import time

class RadioSender:
    def __init__(self, port, baudrate=115200):
        self.ser = serial.Serial(port, baudrate, timeout=1)
        self.packet_size = 10
        print(f"RadioSender configurado: via {port}@{baudrate}")

    def send_command(self,robot_id, fl_s, fl_d, bl_s, bl_d, fr_s, fr_d, br_s, br_d, kicker):
        # clamp values
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
            robot_id,
            fl_s, fl_d,
            bl_s, bl_d,
            fr_s, fr_d,
            br_s, br_d,
            kicker_byte
        ])

        try:
            self.ser.write(packet)
            print(f"Pacote enviado p/ robô {robot_id}: {packet.hex()}")
        except Exception as e:
            print(f"Erro ao enviar pacote via serial: {e}")


if __name__ == '__main__':
    SERIAL_PORT = '/dev/ttyUSB0'  # altere para a porta real
    ROBOT_ID = 1

    sender_test = RadioSender(SERIAL_PORT, 115200)

    print(f"\nIniciando teste de envio para robô {ROBOT_ID} via {SERIAL_PORT}")

    try:
        # Função helper para simplificar testes
        def test_cmd(string_cmd, *args, delay: float = 2):
            print(f"\n[ROBO {ROBOT_ID}] {string_cmd}")
            sender_test.send_command(*args)
            time.sleep(delay)
            print(f"[ROBO {ROBOT_ID}] Desativando todas as rodas")
            sender_test.send_command(ROBOT_ID,0,0,0,0,0,0,0,0,0)
            time.sleep(1)

        test_cmd("Chutar", 0,0,0,0,0,0,0,0,True, delay=0.1)
        test_cmd("Roda frente-esquerda frente", 250,0,0,0,0,0,0,0,False, delay=5)
        test_cmd("Roda frente-esquerda trás", 250,1,0,0,0,0,0,0,False, delay=5)
        test_cmd("Todas rodas frente", 250,0,250,0,250,0,250,0,False, delay=5)
        test_cmd("Todas rodas trás", 250,1,250,1,250,1,150,1,False, delay=5)

    except KeyboardInterrupt:
        print("\nTeste interrompido pelo usuário.")
    except Exception as e:
        print(f"\nOcorreu um erro durante o teste: {e}")
    finally:
        print("\nTestes concluídos.")
