from client import VisionClient
from data_receiver import VisionDataReceiver

VISION_IP = '224.5.23.2'
VISION_PORT = 10006
UDP_RECEIVE_BUFFER_SIZE = 2048

def run_vision_system():
    vision_client = VisionClient(VISION_IP, VISION_PORT)
    
    if not vision_client.connect():
        print("Não foi possível conectar ao sistema de visão. Verifique o IP/Porta e se a SSL-Vision está rodando.")
        return

    vision_data_receiver = VisionDataReceiver(vision_client)
    print("Sistema de Visão Titans-Vision iniciado. Aguardando dados...")

    try:
        while True:
            vision_info = vision_data_receiver.receive_data()

            if vision_info and vision_info['detection']:
                detection_data = vision_info['detection']
                
                balls = detection_data['balls']
                robots_blue = detection_data['robots']['blue']
                robots_yellow = detection_data['robots']['yellow']

                if balls:
                    print(f"Frame {detection_data['frame_number']} - Bola(s): {len(balls)}")
                    for b in balls:
                        print(f"  - Bola @ X:{b['x']:.2f}, Y:{b['y']:.2f}, Z:{b['z']:.2f}")
                
                if robots_blue:
                    print(f"Frame {detection_data['frame_number']} - Robôs Azuis: {len(robots_blue)}")
                    for r in robots_blue:
                        print(f"  - Azul {r['robot_id']} @ X:{r['x']:.2f}, Y:{r['y']:.2f}, Ori:{r['orientation']:.2f}")
                
                if robots_yellow:
                    print(f"Frame {detection_data['frame_number']} - Robôs Amarelos: {len(robots_yellow)}")
                    for r in robots_yellow:
                        print(f"  - Amarelo {r['robot_id']} @ X:{r['x']:.2f}, Y:{r['y']:.2f}, Ori:{r['orientation']:.2f}")

            time.sleep(0.005)

    except KeyboardInterrupt:
        print("\nSistema de Visão encerrado pelo usuário.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado no sistema de visão: {e}")
    finally:
        vision_client.disconnect()

if __name__ == '__main__':
    run_vision_system()