# controller/pid.py (VERSÃO GOAT DEFINITIVA)
import math
import time

class PIDController:
    def __init__(self, kp=1.0, ki=0.0, kd=0.0, output_limits=(None, None)):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.output_limits = output_limits
        self._integral = 0.0
        self._last_error = 0.0
        self._last_time = None

    def reset(self):
        self._integral = 0.0
        self._last_error = 0.0
        self._last_time = None

    def update(self, error, current_time=None):
        if current_time is None:
            current_time = time.time()
        
        dt = 0.0
        if self._last_time is not None:
            dt = current_time - self._last_time

        p = self.kp * error
        self._integral += error * dt
        i = self.ki * self._integral
        d = 0.0
        if dt > 0:
            d = self.kd * (error - self._last_error) / dt

        output = p + i + d

        min_out, max_out = self.output_limits
        if min_out is not None:
            output = max(min_out, output)
        if max_out is not None:
            output = min(max_out, output)

        self._last_error = error
        self._last_time = current_time
        print(f"PID Update -> P: {p:.3f}, I: {i:.3f}, D: {d:.3f}, Output: {output:.3f}")
        return output

# Versão corrigida da função que sempre pega o caminho mais curto
def angle_diff(target, current):
    """ Retorna a menor diferença de ângulo, normalizada entre [-pi, pi]. """
    diff = target - current
    while diff > math.pi:
        diff -= 2 * math.pi
    while diff < -math.pi:
        diff += 2 * math.pi
    return diff

class OmniCalculator:
    def __init__(self, wheel_radius_mm=30, robot_radius_mm=75):
        self.wheel_radius_m = wheel_radius_mm / 1000.0
        self.robot_radius_m = robot_radius_mm / 1000.0
        self.max_motor_pwm = 255
        self.MAX_ANGULAR_VEL_RAD_S = 10.0  

        # Ganhos balanceados para um bom começo
        self.pid_x = PIDController(kp=1.0, ki=0.0, kd=0.5, output_limits=(-0.6, 0.6))
        self.pid_y = PIDController(kp=1.0, ki=0.0, kd=0.5, output_limits=(-0.6, 0.6))
        self.pid_theta = PIDController(kp=5.0, ki=0.0, kd=0.8, output_limits=(-7.0, 7.0))
        
        print(f"OmniCalculator (VERSÃO GOAT FINAL) inicializado.")

    def calculate_wheel_speeds(self, robot_data):
        # 1. CORREÇÃO DA INTEGRAL: Limpa a memória a cada ciclo
        self.pid_x.reset()
        self.pid_y.reset()
        self.pid_theta.reset()

        # Alvos e Posições Atuais
        target_x = robot_data['robot_target_x'] / 1000.0
        target_y = robot_data['robot_target_y'] / 1000.0
        target_theta = robot_data['robot_target_orientation']
        x_m = robot_data['robot_current_x'] / 1000.0
        y_m = robot_data['robot_current_y'] / 1000.0
        theta = robot_data['robot_current_orientation']

        # Cálculo dos Erros
        error_x = target_x - x_m
        error_y = target_y - y_m
        error_theta = angle_diff(target_theta, theta)

        # O Cérebro: Calcula as velocidades GLOBAIS
        vx_global = self.pid_x.update(error_x)
        vy_global = self.pid_y.update(error_y)
        w = self.pid_theta.update(error_theta)
        
        # Transformação para o referencial do robô
        vx_local = math.cos(theta) * vx_global + math.sin(theta) * vy_global
        vy_local = -math.sin(theta) * vx_global + math.cos(theta) * vy_global
        
        r = self.robot_radius_m
        R = self.wheel_radius_m

        # FÓRMULA DE CINEMÁTICA PADRÃO (sem w = -w)
        v_fl = (vx_local - vy_local - r * w) / R
        v_bl = (vx_local + vy_local - r * w) / R
        v_fr = (vx_local + vy_local + r * w) / R
        v_br = (vx_local - vy_local + r * w) / R
        
        speeds = [v_fl, v_bl, v_fr, v_br]
        max_speed = max(abs(s) for s in speeds) if speeds else 0
        if max_speed > self.MAX_ANGULAR_VEL_RAD_S:
            scale = self.MAX_ANGULAR_VEL_RAD_S / max_speed
            v_fl, v_bl, v_fr, v_br = [s * scale for s in speeds]

        def to_pwm(speed):
            return int(min(self.max_motor_pwm, abs(speed / self.MAX_ANGULAR_VEL_RAD_S * self.max_motor_pwm)))

        return {
            'fl_speed': to_pwm(v_fl), 'fl_direction': 0 if v_fl >= 0 else 1,
            'bl_speed': to_pwm(v_bl), 'bl_direction': 0 if v_bl >= 0 else 1,
            'fr_speed': to_pwm(v_fr), 'fr_direction': 0 if v_fr >= 0 else 1,
            'br_speed': to_pwm(v_br), 'br_direction': 0 if v_br >= 0 else 1,
        }