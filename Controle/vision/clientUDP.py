import socket
import struct
from utils.logger import setup_logger
import threading

TIMEOUT = 1.5  # seconds

class UDPClient:
    def __init__(self, ip, port, filename):
        self.ip = ip
        self.port = port
        self.sock = None
        self.data = None
        self._is_running = threading.Event()
        self._lock = threading.Lock()
        self.logger = setup_logger(filename, f'logs/{filename}.log')

    def run(self):
        if not self._is_running.is_set():
            self._is_running.set()      
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind(('', self.port))

            # Join multicast group
            mreq = struct.pack("4sl", socket.inet_aton(self.ip), socket.INADDR_ANY)
            self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

            self.sock.settimeout(TIMEOUT)

            try:
                data, _ = self.sock.recvfrom(2048)
                with self._lock:
                    self.data = data
                self.logger.info(f"Received {len(data)} bytes from {self.ip}:{self.port}")
            except Exception as e:
                self.logger.error(f"Error receiving data: {e}")

        except Exception as e:
            self.logger.error(f"Error initializing UDP Socket: {e}")
            self.sock = None

    def get_last_data(self):
        with self._lock:
            return self.data