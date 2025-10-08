import math
class Strategy:
    def __init__(self):
        print("Estrategia inicializada: Selecionando alvo (bola) para o robo.")
        self.KICK_DISTANCE_THRESHOLD = 150 # mm

    def decide_action(self, robot_state_for_strategy, robot_id):
        robot_current_x = robot_state_for_strategy.get('robot_current_x')
        robot_current_y = robot_state_for_strategy.get('robot_current_y')
        robot_current_orientation = robot_state_for_strategy.get('robot_current_orientation')
        ball_pos = robot_state_for_strategy.get('ball_pos')

        kick_command = False

        if robot_current_x is None or ball_pos is None:
            print ("Robot position or ball position is None, cannot follow the ball.")
            return None

        # >>>>> CORREÇÃO FINAL <<<<<
        # Remova o sinal de menos. A fiação e a cinemática já estão corretas.
        angle_to_ball = math.atan2(
            (ball_pos['y'] - robot_current_y), # SEM o sinal de menos
            (ball_pos['x'] - robot_current_x)
        )
        robot_target_orientation = angle_to_ball
        # >>>>> FIM DA CORREÇÃO <<<<<

        robot_target_x = ball_pos['x']
        robot_target_y = ball_pos['y']
        
        distance_to_ball = ((robot_current_x - ball_pos['x']) ** 2 + (robot_current_y - ball_pos['y']) ** 2) ** 0.5
        if distance_to_ball < self.KICK_DISTANCE_THRESHOLD:
            kick_command = True
            print (f"Robot {robot_id} is close to the ball (distance: {distance_to_ball:.2f}). Preparing to kick.")
        else:
            print (f"Robot {robot_id} is far from the ball (distance: {distance_to_ball:.2f}). Moving towards the ball.")

        return {
            'robot_current_x': robot_current_x,
            'robot_current_y': robot_current_y,
            'robot_current_orientation': robot_current_orientation,
            'robot_target_x': robot_target_x,
            'robot_target_y': robot_target_y,
            'robot_target_orientation': robot_target_orientation,
            'kick_command': kick_command
        }
        