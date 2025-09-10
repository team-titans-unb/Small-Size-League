import math
import config

class OmniCalculator:
    def __init__(self, wheel_radius_mm=None, robot_radius_mm=None):
        """
        Inicializa o OmniCalculator.

        Args:
            wheel_radius_mm (float): Raio da roda omnidirecional em mm.
            robot_radius_mm (float): Distância do centro do robô ao centro da roda em mm.
        """
        self.wheel_radius_m = (wheel_radius_mm if wheel_radius_mm is not None else config.WHEEL_RADIUS_MM) / 1000.0
        self.robot_radius_m = (robot_radius_mm if robot_radius_mm is not None else config.ROBOT_RADIUS_MM) / 1000.0
        self.max_motor_pwm = 255

        # Ângulos das rodas em relação ao eixo X positivo do robô (em radianos)
        self.angle_fl = math.radians(60)
        self.angle_bl = math.radians(45)
        self.angle_fr = math.radians(60)
        self.angle_br = math.radians(45)

        # Calibre este valor! Velocidade angular máxima que um motor pode atingir em rad/s para PWM 255.
        self.MAX_ANGULAR_VEL_RAD_S = 20.0 # Exemplo: 20 rad/s (ajuste)

        print(f"OmniCalculator inicializado. Raio da Roda: {self.wheel_radius_m:.3f}m, Raio do Robô: {self.robot_radius_m:.3f}m")

    def calculate_wheel_speeds(self, vx, vy, w, robot_data):
        """
        Calcula as velocidades PWM e direções para cada roda omnidirecional.

        Args:
            vx (float): Velocidade linear desejada no eixo X do robô (m/s).
            vy (float): Velocidade linear desejada no eixo Y do robô (m/s).
            w (float): Velocidade angular desejada do robô (rad/s).

        Returns:
            dict: Dicionário com velocidades PWM (0-255) e direções (0/1) para cada roda.
        """
        if robot_data is None:
         #Se não houver os dados, retorna velocidade zero
         return {'v_fl': 0.0, 'v_bl': 0.0, 'v_fr': 0.0, 'v_br': 0.0}
        
        Xr = robot_data['robot_current_x']
        Yr = robot_data['robot_current_y']
        ThetaR = robot_data['robot_current_orientation']
        Tx = robot_data['robot_target_x']
        Ty = robot_data['robot_target_y']

        # Velocidade das rodas calculada pela cinemática omnidirecional
        v_fl = ((self.robot_radius_m * w)/self.wheel_radius_m) + (vx * ((-math.sin(ThetaR))/2*self.wheel_radius_m) - (529*math.pi*math.cos(ThetaR))/1919*self.wheel_radius_m) + (vy * ((-529*math.pi*math.sin(ThetaR))/1919*self.wheel_radius_m) + (math.cos(ThetaR))/2*self.wheel_radius_m)
        v_bl = ((self.robot_radius_m * w)/self.wheel_radius_m) + (vx * ((569*math.pi*math.sin(ThetaR))/2528*self.wheel_radius_m) - (569*math.pi*math.cos(ThetaR))/2528*self.wheel_radius_m) + (vy * ((-569*math.pi*math.sin(ThetaR))/2528*self.wheel_radius_m) + (-569*math.pi*math.cos(ThetaR))/2528*self.wheel_radius_m)
        v_fr = ((self.robot_radius_m * w)/self.wheel_radius_m) + (vx * ((569*math.pi*math.sin(ThetaR))/2528*self.wheel_radius_m) + (569*math.pi*math.cos(ThetaR))/2528*self.wheel_radius_m) + (vy * (( 569*math.pi*math.sin(ThetaR))/2528*self.wheel_radius_m) + (-569*math.pi*math.cos(ThetaR))/2528*self.wheel_radius_m)
        v_br = ((self.robot_radius_m * w)/self.wheel_radius_m) + (vx * ((-math.sin(ThetaR))/2*self.wheel_radius_m) + (529*math.pi*math.cos(ThetaR))/1919*self.wheel_radius_m) + (vy * ((529*math.pi*math.sin(ThetaR))/1919*self.wheel_radius_m) + (math.cos(ThetaR))/2*self.wheel_radius_m)

        # Encontrar a velocidade angular máxima entre todas as rodas para normalização
        max_abs_omega = max(abs(v_fl), abs(v_bl), abs(v_fr), abs(v_br))

        # Normaliza as velocidades se alguma exceder a capacidade máxima do motor
        scale_factor = 1.0
        if max_abs_omega > self.MAX_ANGULAR_VEL_RAD_S:
            scale_factor = self.MAX_ANGULAR_VEL_RAD_S / max_abs_omega
            v_fl *= scale_factor
            v_bl *= scale_factor
            v_fr *= scale_factor
            v_br *= scale_factor

        # Converte a velocidade angular (rad/s) para PWM (0-255)
        # Assumindo uma relação linear:
        # (omega_roda / MAX_ANGULAR_VEL_RAD_S) * PWM_MAX
        pwm_fl = int(abs(v_fl / self.MAX_ANGULAR_VEL_RAD_S * self.max_motor_pwm))
        pwm_bl = int(abs(v_bl / self.MAX_ANGULAR_VEL_RAD_S * self.max_motor_pwm))
        pwm_fr = int(abs(v_fr / self.MAX_ANGULAR_VEL_RAD_S * self.max_motor_pwm))
        pwm_br = int(abs(v_br / self.MAX_ANGULAR_VEL_RAD_S * self.max_motor_pwm))

        # Determina a direção (0 ou 1).
        dir_fl = 0 if v_fl >= 0 else 1 
        dir_bl = 0 if v_bl >= 0 else 1
        dir_fr = 0 if v_fr >= 0 else 1
        dir_br = 0 if v_br >= 0 else 1

        # Garante que os valores PWM estão dentro do limite (100,-255)
        pwm_fl = max(200, min(self.max_motor_pwm, pwm_fl))
        pwm_bl = max(200, min(self.max_motor_pwm, pwm_bl))
        pwm_fr = max(200, min(self.max_motor_pwm, pwm_fr))
        pwm_br = max(200, min(self.max_motor_pwm, pwm_br))
        
        return {
            'fl_speed': pwm_fl, 'fl_direction': dir_fl,
            'bl_speed': pwm_bl, 'bl_direction': dir_bl,
            'fr_speed': pwm_fr, 'fr_direction': dir_fr,
            'br_speed': pwm_br, 'br_direction': dir_br,
        }