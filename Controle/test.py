from vision.clientUDP import UDPClient
from vision.parser import VisionDataParser
from vision.gcparser import GCDataParser
import socket
import threading

def test_Vision_Detections():
    VISION_IP = '224.5.23.2'
    VISION_PORT = 10006

    vision = UDPClient(VISION_IP, VISION_PORT, 'vision')
    vision_thread = threading.Thread(target=vision.run)
    vision_thread.start()
    vision_parser = VisionDataParser()

    while True:
        print("Lastar Detections:")
        data = vision.get_last_data()
        if data:
            vision_parser.parser_loop(data)
        detection = vision_parser.get_last_detection()
        if detection:
            print(f"Frame Number: {detection.get('frame_number')}")
            print(f"Balls: {detection.get('balls')}")
            print(f"Robots Yellow: {detection.get('robots_yellow')}")
            print(f"Robots Blue: {detection.get('robots_blue')}")
            print("-----")
        pass

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

def test_GC_Referee():
    GC_IP = '224.5.23.1'
    GC_PORT = 10003

    gc = UDPClient(GC_IP, GC_PORT, 'gc_referee')
    gc_thread = threading.Thread(target=gc.run)
    gc_thread.start()
    gc_parser = GCDataParser()

    while True:
        print("Last GC Data:")
        data = gc.get_last_data()
        if data:
            gc_parser.parser_loop(data)
        gc_data = gc_parser.get_last_data()
        if gc_data:
            command = gc_data.get('command')
            print(command)
            print("-----")
        pass

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

    # ----------- FUNCIONANDO -----------
    print("Testing GC Referee on port 10003")
    test_GC_Referee()