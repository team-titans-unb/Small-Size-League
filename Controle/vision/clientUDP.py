import socket
import struct
import threading
from utils.logger import setup_logger

TIMEOUT = 1.5  # seconds

class UDPClient:
    def __init__(self, ip, port, log_name):
        self.ip = ip
        self.port = port
        self.sock = None
        self.data = None
        self._is_running = threading.Event()
        self._lock = threading.Lock()
        self.logger = setup_logger(log_name, f'logs/UDPClient.log')

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind(('', self.port))

            mreq = struct.pack("4sl", socket.inet_aton(self.ip), socket.INADDR_ANY)
            self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
            
            self.sock.settimeout(TIMEOUT)
            self.logger.info(f"UDP Client initialized for {self.ip}:{self.port}")
        except Exception as e:
            self.logger.error(f"Error initializing UDP Socket: {e}")
            self.sock = None


    def run(self):
        if not self.sock:
            self.logger.error("Socket not initialized. Exiting run method.")
            return
        
        if not self._is_running.is_set():
            self._is_running.set()

        while self._is_running.is_set():
            try:
                data, _ = self.sock.recvfrom(2048)
                if data:
                    with self._lock:
                        self.data = data
            
            except socket.timeout:
                self.logger.warning(f"Timeout on {self.ip}:{self.port}. Retrying...")
                pass
            except Exception as e:
                self.logger.error(f"Error receiving data: {e}")
                pass
        
        try:
            self.sock.close()
        except:
            pass

    def get_last_data(self):
        with self._lock:
            return self.data
        
    def stop(self):
        self._is_running.clear()
        try:
            self.sock.close()
        except:
            pass