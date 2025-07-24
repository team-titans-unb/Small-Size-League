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
        self.angle_fl = math.radians(135)
        self.angle_bl = math.radians(225)
        self.angle_fr = math.radians(45)
        self.angle_br = math.radians(315)

        # Calibre este valor! Velocidade angular máxima que um motor pode atingir em rad/s para PWM 255.
        self.MAX_ANGULAR_VEL_RAD_S = 20.0 # Exemplo: 20 rad/s (ajuste)

        print(f"OmniCalculator inicializado. Raio da Roda: {self.wheel_radius_m:.3f}m, Raio do Robô: {self.robot_radius_m:.3f}m")

    def calculate_wheel_speeds(self, vx, vy, w):
        """
        Calcula as velocidades PWM e direções para cada roda omnidirecional.

        Args:
            vx (float): Velocidade linear desejada no eixo X do robô (m/s).
            vy (float): Velocidade linear desejada no eixo Y do robô (m/s).
            w (float): Velocidade angular desejada do robô (rad/s).

        Returns:
            dict: Dicionário com velocidades PWM (0-255) e direções (0/1) para cada roda.
        """
        # O modelo mais comum de cinemática inversa para rodas mecanum/omni é:
        # V_roda_i = vx * cos(alpha_i) + vy * sin(alpha_i) + L * w

        # Velocidade tangencial de cada roda (m/s)
        v_fl = (vx * math.cos(self.angle_fl) + vy * math.sin(self.angle_fl) + self.robot_radius_m * w)
        v_bl = (vx * math.cos(self.angle_bl) + vy * math.sin(self.angle_bl) + self.robot_radius_m * w)
        v_fr = (vx * math.cos(self.angle_fr) + vy * math.sin(self.angle_fr) + self.robot_radius_m * w)
        v_br = (vx * math.cos(self.angle_br) + vy * math.sin(self.angle_br) + self.robot_radius_m * w)

        # Converte velocidade tangencial (m/s) para velocidade angular da roda (rad/s)
        omega_fl = v_fl / self.wheel_radius_m
        omega_bl = v_bl / self.wheel_radius_m
        omega_fr = v_fr / self.wheel_radius_m
        omega_br = v_br / self.wheel_radius_m

        # Encontrar a velocidade angular máxima entre todas as rodas para normalização
        max_abs_omega = max(abs(omega_fl), abs(omega_bl), abs(omega_fr), abs(omega_br))

        # Normaliza as velocidades se alguma exceder a capacidade máxima do motor
        scale_factor = 1.0
        if max_abs_omega > self.MAX_ANGULAR_VEL_RAD_S:
            scale_factor = self.MAX_ANGULAR_VEL_RAD_S / max_abs_omega
            omega_fl *= scale_factor
            omega_bl *= scale_factor
            omega_fr *= scale_factor
            omega_br *= scale_factor

        # Converte a velocidade angular (rad/s) para PWM (0-255)
        # Assumindo uma relação linear:
        # (omega_roda / MAX_ANGULAR_VEL_RAD_S) * PWM_MAX
        pwm_fl = int(abs(omega_fl / self.MAX_ANGULAR_VEL_RAD_S * self.max_motor_pwm))
        pwm_bl = int(abs(omega_bl / self.MAX_ANGULAR_VEL_RAD_S * self.max_motor_pwm))
        pwm_fr = int(abs(omega_fr / self.MAX_ANGULAR_VEL_RAD_S * self.max_motor_pwm))
        pwm_br = int(abs(omega_br / self.MAX_ANGULAR_VEL_RAD_S * self.max_motor_pwm))

        # Determina a direção (0 ou 1).
        dir_fl = 0 if omega_fl >= 0 else 1 
        dir_bl = 0 if omega_bl >= 0 else 1
        dir_fr = 0 if omega_fr >= 0 else 1
        dir_br = 0 if omega_br >= 0 else 1

        # Garante que os valores PWM estão dentro do limite (0-255)
        pwm_fl = max(0, min(self.max_motor_pwm, pwm_fl))
        pwm_bl = max(0, min(self.max_motor_pwm, pwm_bl))
        pwm_fr = max(0, min(self.max_motor_pwm, pwm_fr))
        pwm_br = max(0, min(self.max_motor_pwm, pwm_br))
        
        return {
            'fl_speed': pwm_fl, 'fl_direction': dir_fl,
            'bl_speed': pwm_bl, 'bl_direction': dir_bl,
            'fr_speed': pwm_fr, 'fr_direction': dir_fr,
            'br_speed': pwm_br, 'br_direction': dir_br,
        }