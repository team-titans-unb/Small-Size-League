import math

class Strategy:
    def __init__(self):
        print("Estrategia inicializada: Selecionando alvo (bola) para o robo.")
        self.KICK_DISTANCE_THRESHOLD = 0.15

    def decide_action(self, robot_state_for_strategy, robot_id):
        robot_current_x = robot_state_for_strategy.get('robot_current_x')
        robot_current_y = robot_state_for_strategy.get('robot_current_y')
        robot_current_orientation = robot_state_for_strategy.get('robot_current_orientation')
        ball_pos = robot_state_for_strategy.get('ball_pos')

        robot_target_x = None
        robot_target_y = None
        robot_target_orientation = None
        kick_command = False

        if robot_current_x is None or robot_target_x is None and ball_pos is None:
            return None

        if ball_pos:
            robot_target_x = ball_pos['x']
            robot_target_y = ball_pos['y']
        else:
            robot_target_x = 0.0
            robot_target_y = 0.0
            robot_target_orientation = 0.0
            kick_command = False


        return {
            'robot_current_x': robot_current_x,
            'robot_current_y': robot_current_y,
            'robot_current_orientation': robot_current_orientation,
            'robot_target_x': robot_target_x,
            'robot_target_y': robot_target_y,
            'robot_target_orientation': robot_target_orientation,
            'kick_command': kick_command
        }