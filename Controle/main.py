import time
import math
from math import degrees

from vision.client import VisionClient
from vision.data_receiver import VisionDataReceiver

import config

from strategy import Strategy
from controller.motion_controller import MotionController
from controller.omni_calculator import OmniCalculator
from Controle.sender.udp_client import UdpClient
from Controle.sender.tcp_client import TcpClient

TEAM_COLOR = config.TEAM_COLOR
ROBOT_CONFIGS = config.ROBOT_CONFIGS
VISION_DATA_SOURCE_IP = config.VISION_DATA_SOURCE_IP
VISION_DATA_SOURCE_PORT = config.VISION_DATA_SOURCE_PORT
WHEEL_RADIUS_MM = config.WHEEL_RADIUS_MM
ROBOT_RADIUS_MM = config.ROBOT_RADIUS_MM

vision_client = VisionClient(VISION_DATA_SOURCE_IP, VISION_DATA_SOURCE_PORT)
if not vision_client.connect():
    print("ERRO: Não foi possível conectar ao VisionClient. Verifique o IP/Porta e se a SSL-Vision está rodando.")
    exit()

vision_data_receiver = VisionDataReceiver(vision_client)
strategy = Strategy()
omni_calculator = OmniCalculator(wheel_radius_mm=WHEEL_RADIUS_MM, robot_radius_mm=ROBOT_RADIUS_MM)

robot_senders = {}
for robot_id, config in ROBOT_CONFIGS.items():
    robot_senders[robot_id] = UdpClient(robot_ip=config['ip'], robot_port=config['port'])
    print(f"Sender para Robô {robot_id} configurado para {config['ip']}:{config['port']}")


print(f"Aguardando dados da visão em {VISION_DATA_SOURCE_IP}:{VISION_DATA_SOURCE_PORT}")

def main_loop():
    last_print_time = time.time()
    
    while True:
        current_vision_data = vision_data_receiver.receive_data()

        if current_vision_data and current_vision_data.get('detection'):
            detection_data = current_vision_data['detection']
            our_robots_detected = detection_data['robots'].get(TEAM_COLOR, [])
            ball_info = detection_data['balls'][0] if detection_data.get('balls') else None

            for detected_robot_info in our_robots_detected:
                robot_id = detected_robot_info.get('robot_id')
                
                if robot_id is not None and robot_id in ROBOT_CONFIGS:
                    robot_state_for_strategy = {
                        'robot_current_x': detected_robot_info['x'],
                        'robot_current_y': detected_robot_info['y'],
                        'robot_current_orientation': detected_robot_info['orientation'],
                        'ball_pos': ball_info 
                    }
                    
                    target_and_current_data = strategy.decide_action(robot_state_for_strategy, robot_id)
                    
                    command_intent = False
                    command_intent = MotionController.calculate_robot_velocities(target_and_current_data, robot_data)

                    wheel_commands = {
                            'fl_speed': 250, 'fl_direction': 0,
                            'bl_speed': 250, 'bl_direction': 0,
                            'fr_speed': 250, 'fr_direction': 1,
                            'br_speed': 250, 'br_direction': 1,
                            'kicker': False
                    }

                    if command_intent:
                        wheel_commands = omni_calculator.calculate_wheel_speeds(
                            command_intent['vx'],
                            command_intent['vy'],
                            command_intent['w']
                        )
                        wheel_commands['kicker'] = command_intent['kick']

                    if robot_id in robot_senders:
                        udp_sender_for_this_robot = robot_senders[robot_id]
                        udp_sender_for_this_robot.send_command(
                            wheel_commands['fl_speed'], wheel_commands['fl_direction'],
                            wheel_commands['bl_speed'], wheel_commands['bl_direction'],
                            wheel_commands['fr_speed'], wheel_commands['fr_direction'],
                            wheel_commands['br_speed'], wheel_commands['br_direction'],
                            wheel_commands['kicker']
                        )
        else:
            for robot_id_to_stop in ROBOT_CONFIGS:
                if robot_id_to_stop in robot_senders:
                    robot_senders[robot_id_to_stop].send_command(0,0,0,0,0,0,0,0,False)

        if time.time() - last_print_time > 0.1:
            if current_vision_data and current_vision_data.get('detection'):
                detected_robots_info_str = []
                ball_info_str = "N/A"
                if ball_info:
                    ball_info_str = f"({ball_info['x']:.2f}, {ball_info['y']:.2f})"

                for r in current_vision_data['detection'].get(TEAM_COLOR, []):
                    detected_robots_info_str.append(f"ID{r.get('robot_id', 'N/A')}: ({r['x']:.2f}, {r['y']:.2f}, {degrees(r['orientation']):.1f}deg)")
                    if r.get('robot_id') in ROBOT_CONFIGS and robot_senders[r.get('robot_id')]:
                        if r.get('robot_id') == list(ROBOT_CONFIGS.keys())[0]: # Imprime detalhes do primeiro robô configurado
                            target_data = strategy.decide_action(
                                {
                                    'robot_current_x': r['x'], 'robot_current_y': r['y'], 'robot_current_orientation': r['orientation'],
                                    'ball_pos': ball_info
                                },
                                r.get('robot_id')
                            )
                            if target_data:
                                current_intent = MotionController.calculate_robot_velocities(target_data)
                                print(f"  -> Robo {r.get('robot_id')}: Vx={current_intent['vx']:.2f}, Vy={current_intent['vy']:.2f}, W={current_intent['w']:.2f}, Kicker={current_intent['kick']}")

                print(f"Bola: {ball_info_str} | Robôs {TEAM_COLOR}: {', '.join(detected_robots_info_str)}")
            else:
                print("Aguardando dados da visão...")
            last_print_time = time.time()

        time.sleep(0.02)

if __name__ == '__main__':
    try:
        main_loop()
    except KeyboardInterrupt:
        print("\nMente encerrada pelo usuário.")
        wheel_commands = {
            'fl_speed': 0, 'fl_direction': 1,
            'bl_speed': 0, 'bl_direction': 1,
            'fr_speed': 0, 'fr_direction': 1,
            'br_speed': 0, 'br_direction': 1,
            'kicker': False
        }
        for robot_id in robot_senders:
            udp_sender_for_this_robot = robot_senders[robot_id]
            udp_sender_for_this_robot.send_command(
                wheel_commands['fl_speed'], wheel_commands['fl_direction'],
                wheel_commands['bl_speed'], wheel_commands['bl_direction'],
                wheel_commands['fr_speed'], wheel_commands['fr_direction'],
                wheel_commands['br_speed'], wheel_commands['br_direction'],
                wheel_commands['kicker']
            )
    except Exception as e:
        print(f"Um erro inesperado ocorreu: {e}")
    finally:
        if vision_client:
            vision_client.disconnect()