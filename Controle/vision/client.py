import socket
import struct
from utils.logger import setup_logger

TIMEOUT = 1.5  # seconds

class UDPSocket:
    def __init__(self, ip, port, filename):
        self.ip = ip
        self.port = port
        self.sock = None
        self.logger = setup_logger(filename, f'logs/{filename}.log')

    def connect(self):        
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind(('', self.port))

            # Join multicast group
            mreq = struct.pack("4sl", socket.inet_aton(self.ip), socket.INADDR_ANY)
            self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

            self.sock.settimeout(TIMEOUT)
            self.logger.info(f"UDP Socket conectado e escutando em {self.ip}:{self.port}")
            return True
        except Exception as e:
            self.logger.error(f"Erro ao conectar UDP Socket: {e}")
            self.sock = None
            return False

    def get_socket(self):
        return self.sock

    def disconnect(self):
        if self.sock:
            self.sock.close()
            self.sock = None
            self.logger.info("UDP Socket desconectado.")

    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()