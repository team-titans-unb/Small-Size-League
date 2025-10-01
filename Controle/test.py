from vision.client import UDPSocket
import socket
import time

def test_Vision_Detections():
    VISION_IP = '224.5.23.2'
    VISION_PORT = 10006

    while True:
        with UDPSocket(VISION_IP, VISION_PORT, 'vision_client') as vision_client:
            if vision_client.connect():
                sock = vision_client.get_socket()
                try:
                    data, addr = sock.recvfrom(2048)  # Buffer size is 2048 bytes
                    if data:
                        print(f"Received {len(data)} bytes from {addr}")
                except socket.timeout:
                    print("No data received within the timeout period.")
                except Exception as e:
                    print(f"Error receiving data: {e}")
            else:
                print("Fail to connect.")

def test_Vision_Detections_Legacy():
    VISION_IP = '224.5.23.2'
    VISION_PORT = 10005

    while True:
        with UDPSocket(VISION_IP, VISION_PORT, 'vision_legacy_client') as vision_legacy_client:
            if vision_legacy_client.connect():
                sock = vision_legacy_client.get_socket()
                try:
                    data, addr = sock.recvfrom(2048)  # Buffer size is 2048 bytes
                    if data:
                        print(f"Received {len(data)} bytes from {addr}")
                except socket.timeout:
                    print("No data received within the timeout period.")
                except Exception as e:
                    print(f"Error receiving data: {e}")
            else:
                print("Fail to connect.")

def test_Vision_Detections_Tracker():
    VISION_IP = '224.5.23.2'
    VISION_PORT = 10010

    while True:
        with UDPSocket(VISION_IP, VISION_PORT, 'vision_tracker_client') as vision_tracker_client:
            if vision_tracker_client.connect():
                sock = vision_tracker_client.get_socket()
                try:
                    data, addr = sock.recvfrom(2048)  # Buffer size is 2048 bytes
                    if data:
                        print(f"Received {len(data)} bytes from {addr}")
                except socket.timeout:
                    print("No data received within the timeout period.")
                except Exception as e:
                    print(f"Error receiving data: {e}")
            else:
                print("Fail to connect.")

if __name__ == '__main__':
    # ----------- FUNCIONANDO -----------
    print("Testing Vision Detections on port 10006")
    test_Vision_Detections()

    # ----------- FUNCIONANDO -----------
    # print("Testing Vision Detections Legacy on port 10005")
    # test_Vision_Detections_Legacy()

    # --------- NÃO FUNCIONANDO ---------
    # print("Testing Vision Detections Tracker on port 10010")
    # test_Vision_Detections_Tracker()