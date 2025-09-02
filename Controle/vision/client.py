import socket
import struct

class VisionClient:
    def __init__(self, vision_ip, vision_port):
        self.vision_ip = vision_ip
        self.vision_port = vision_port
        self.sock = None

    def connect(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            self.sock.bind(('', self.vision_port))

            mreq = struct.pack("4sl", socket.inet_aton(self.vision_ip), socket.INADDR_ANY)
            self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

            self.sock.settimeout(0.1)
            print(f"VisionClient conectado e escutando em {self.vision_ip}:{self.vision_port}")
            return True
        except Exception as e:
            print(f"Erro ao conectar VisionClient: {e}")
            self.sock = None
            return False

    def get_socket(self):
        return self.sock

    def disconnect(self):
        if self.sock:
            self.sock.close()
            self.sock = None
            print("VisionClient desconectado.")

if __name__ == '__main__':
    VISION_IP = '224.5.23.2'
    VISION_PORT = 10006

    client = VisionClient(VISION_IP, VISION_PORT)
    if client.connect():
        print("Cliente de visão configurado. Tente enviar dados para ele.")
        try:
            while True:
                data, addr = client.get_socket().recvfrom(2048)
                print(f"Dado bruto recebido de {addr}: {len(data)} bytes")
        except socket.timeout:
            pass
        except KeyboardInterrupt:
            print("Interrompido pelo usuário.")
        finally:
            client.disconnect()