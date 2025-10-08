# system_logic.py (VERSÃO FINAL PARA O MODELO GOAT)
import time
from sender.radio_sender import RadioSender
from vision.client import VisionClient
from vision.data_receiver import VisionDataReceiver
from strategy import Strategy
from controller.pid import OmniCalculator
from sender.udp_sender import UdpSender
import config
from constants import VISION_IP, VISION_PORT, ROBOT_CONFIGS

USE_RADIO = True

def create_sender(robot_id, cfg):
    if USE_RADIO:
        return RadioSender(robot_id=robot_id)
    else:
        return UdpSender(robot_ip=cfg['ip'], robot_port=cfg['port'])

def initialize_system():
    print("Initializing system...")
    vision_client = VisionClient(VISION_IP, VISION_PORT)
    if not vision_client.connect(): return None
    vision_receiver = VisionDataReceiver(vision_client)
    print(f"Connected to Vision at {VISION_IP}:{VISION_PORT}")
    robot_senders = {}
    for robot_id, cfg in ROBOT_CONFIGS.items():
        sender = create_sender(robot_id, cfg)
        robot_senders[robot_id] = sender
        print(f"Sender for Robot {robot_id} -> {sender.__class__.__name__}")

    return {
        'vision_client': vision_client,
        'vision_receiver': vision_receiver,
        'strategy': Strategy(),
        'omni_calculator': OmniCalculator(
            wheel_radius_mm=config.WHEEL_RADIUS_MM,
            robot_radius_mm=config.ROBOT_RADIUS_MM
        ),
        'robot_senders': robot_senders
    }

def process_robot_logic(robot_info, ball_info, components):
    robot_id = robot_info.get('robot_id')
    if robot_id not in ROBOT_CONFIGS: return

    target_data = components['strategy'].decide_action({
        'robot_current_x': robot_info['x'],
        'robot_current_y': robot_info['y'],
        'robot_current_orientation': robot_info['orientation'],
        'ball_pos': ball_info
    }, robot_id)

    if target_data:
        wheel_speeds = components['omni_calculator'].calculate_wheel_speeds(target_data)
        should_kick = target_data.get('kick_command', False)
    else:
        wheel_speeds = {'fl_speed': 0, 'bl_speed': 0, 'fr_speed': 0, 'br_speed': 0,
                        'fl_direction': 0, 'bl_direction': 0, 'fr_direction': 0, 'br_direction': 0}
        should_kick = False

    sender = components['robot_senders'].get(robot_id)
    if sender:
        # ORDEM ORIGINAL E CORRETA: FL, FR, BL, BR
        sender.send_command(
            wheel_speeds['fl_speed'], wheel_speeds['fl_direction'],
            wheel_speeds['fr_speed'], wheel_speeds['fr_direction'],
            wheel_speeds['bl_speed'], wheel_speeds['bl_direction'],
            wheel_speeds['br_speed'], wheel_speeds['br_direction'],
            should_kick
        )

        time.sleep(0.1)  # Pequena pausa para evitar sobrecarga
    
def stop_all_robots(robot_senders):
    for sender in robot_senders.values():
        sender.send_command(0,0,0,0,0,0,0,0,False)