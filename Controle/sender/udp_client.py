import socket

class UdpClient:
    def __init__(self, robot_ip, robot_port):
        self.robot_ip = robot_ip
        self.robot_port = robot_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.packet_size = 9

        print(f"UdpClient configurado para enviar para {self.robot_ip}:{self.robot_port}")

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

        packet = bytearray([
            fl_s, fl_d,
            bl_s, bl_d,
            fr_s, fr_d,
            br_s, br_d,
            kicker_byte
        ])

        try:
            self.sock.sendto(packet, (self.robot_ip, self.robot_port))
            print(f"Pacote enviado para {self.robot_ip}:{self.robot_port}: {packet.hex()}")
        except Exception as e:
            print(f"Erro ao enviar pacote UDP para {self.robot_ip}:{self.robot_port}: {e}")

if __name__ == '__main__':
    import time
    ROBOT_TEST_IP = '10.74.1.122'
    ROBOT_TEST_PORT = 8080

    client_test = UdpClient(ROBOT_TEST_IP, ROBOT_TEST_PORT)
    print(f"\nIniciando teste de envio UDP para {ROBOT_TEST_IP}:{ROBOT_TEST_PORT}")
    print("Verifique a saída serial do seu ESP32 para confirmar o recebimento.")

    try:
        # print("\nTeste 1: Chutar (velocidade 0, kicker True)")
        # client_test.send_command(0, 0, 0, 0, 0, 0, 0, 0, True)
        # time.sleep(0.1)
        # print("\nDesativando o kicker")
        # client_test.send_command(0, 0, 0, 0, 0, 0, 0, 0, False)
        # time.sleep(1)

        # print("\nTeste 2: Mover roda da frente-esquerda para frente")
        # client_test.send_command(250, 0, 0, 0, 0, 0, 0, 0, False)
        # time.sleep(10)
        # print("\nDesativando todas as rodas")
        # client_test.send_command(0, 0, 0, 0, 0, 0, 0, 0, False)
        # time.sleep(2)

        # print("\nTeste 3: Mover roda da frente-esquerda para trás")
        # client_test.send_command(250, 1, 0, 0, 0, 0, 0, 0, False)
        # time.sleep(10)
        # print("\nDesativando todas as rodas")
        # client_test.send_command(0, 0, 0, 0, 0, 0, 0, 0, False)
        # time.sleep(2)
        
        # print("\nTeste 4: Mover roda da frente-direita para frente")
        # client_test.send_command(0, 0, 250, 0, 0, 0, 0, 0, False)
        # time.sleep(10)
        # print("\nDesativando todas as rodas")
        # client_test.send_command(0, 0, 0, 0, 0, 0, 0, 0, False)
        # time.sleep(2)

        # print("\nTeste 5: Mover roda da frente-direita para trás")
        # client_test.send_command(0, 0, 250, 1, 0, 0, 0, 0, False)
        # time.sleep(10)
        # print("\nDesativando todas as rodas")
        # client_test.send_command(0, 0, 0, 0, 0, 0, 0, 0, False)
        # time.sleep(2)

        # print("\nTeste 6: Mover roda da traseira-esquerda para frente")
        # client_test.send_command(0, 0, 0, 0, 250, 0, 0, 0, False)
        # time.sleep(10)
        # print("\nDesativando todas as rodas")
        # client_test.send_command(0, 0, 0, 0, 0, 0, 0, 0, False)
        # time.sleep(2)

        # print("\nTeste 7: Mover roda da traseira-esquerda para trás")
        # client_test.send_command(0, 0, 0, 0, 250, 1, 0, 0, False)
        # time.sleep(10)
        # print("\nDesativando todas as rodas")
        # client_test.send_command(0, 0, 0, 0, 0, 0, 0, 0, False)
        # time.sleep(2)

        # print("\nTeste 8: Mover roda da traseira-direita para frente")
        # client_test.send_command(0, 0, 0, 0, 0, 0, 250, 0, False)
        # time.sleep(10)
        # print("\nDesativando todas as rodas")
        # client_test.send_command(0, 0, 0, 0, 0, 0, 0, 0, False)
        # time.sleep(2)

        # print("\nTeste 9: Mover roda da traseira-direita para trás")
        # client_test.send_command(0, 0, 0, 0, 0, 0, 250, 1, False)
        # time.sleep(10)
        # print("\nDesativando todas as rodas")
        # client_test.send_command(0, 0, 0, 0, 0, 0, 0, 0, False)
        # time.sleep(2)

        print("\nTeste 10: Mover todas as rodas para frente")
        client_test.send_command(250, 0, 250, 0, 250, 0, 250, 0, False)
        time.sleep(4)
        print("\nDesativando todas as rodas")
        client_test.send_command(0, 0, 0, 0, 0, 0, 0, 0, False)
        time.sleep(2)

        print("\nTeste 11: Mover todas as rodas para trás")
        client_test.send_command(250, 1, 250, 1, 250, 1, 150, 1, False)
        time.sleep(4)
        print("\nDesativando todas as rodas")
        client_test.send_command(0, 0, 0, 0, 0, 0, 0, 0, False)
        time.sleep(2)
    except KeyboardInterrupt:
        print("\nTeste interrompido pelo usuário.")
    except Exception as e:
        print(f"\nOcorreu um erro durante o teste: {e}")
    finally:
        print("\nTeste do UdpClient concluído.")