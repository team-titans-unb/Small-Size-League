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
        self.MAX_ANGULAR_VEL_RAD_S = 10 # Exemplo: 20 rad/s (ajuste)

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
        ###print (f"Velocidade x{vx}, Velo Y: {vy} Velo Anglular{w}")
        if robot_data is None:
         #Se não houver os dados, retorna velocidade zero
         return {'v_fl': 0.0, 'v_bl': 0.0, 'v_fr': 0.0, 'v_br': 0.0}
        
        print(f"Vel Vx: {vx}")
        print(f"Vel Vy{vy}")
        print(f"W :{w}")
        
        Xr = robot_data['robot_current_x']
        Yr = robot_data['robot_current_y']
        ThetaR = robot_data['robot_current_orientation']
        Tx = robot_data['robot_target_x']
        Ty = robot_data['robot_target_y']

        # Velocidade das rodas calculada pela cinemática omnidirecional

        r = self.robot_radius_m      # Raio do robô
        R = self.wheel_radius_m      # Raio da roda

        sin_theta = math.sin(ThetaR)
        cos_theta = math.cos(ThetaR)

        term_w = (r * w) / R  # Componente rotacional (giro do robô)

        # -------------------------------
        # FL (Front Left)
        # -------------------------------
        term_vx_fl = vx * ((-sin_theta) / (2 * R)) - (529 * math.pi * cos_theta) / (1919 * R)
        term_vy_fl = vy * ((-529 * math.pi * sin_theta) / (1919 * R)) + (cos_theta / (2 * R))
        v_fl = term_w + term_vx_fl + term_vy_fl

        # -------------------------------
        # BL (Back Left)
        # -------------------------------
        term_vx_bl = vx * ((569 * math.pi * sin_theta) / (2528 * R)) - (569 * math.pi * cos_theta) / (2528 * R)
        term_vy_bl = vy * ((-569 * math.pi * sin_theta) / (2528 * R)) + (-569 * math.pi * cos_theta) / (2528 * R)
        v_bl = term_w + term_vx_bl + term_vy_bl

        # -------------------------------
        # FR (Front Right)
        # -------------------------------
        term_vx_fr = vx * ((569 * math.pi * sin_theta) / (2528 * R)) + (569 * math.pi * cos_theta) / (2528 * R)
        term_vy_fr = vy * (( 569 * math.pi * sin_theta) / (2528 * R)) + (-569 * math.pi * cos_theta) / (2528 * R)
        v_fr = term_w + term_vx_fr + term_vy_fr

        # -------------------------------
        # BR (Back Right)
        # -------------------------------
        term_vx_br = vx * ((-sin_theta) / (2 * R)) + (529 * math.pi * cos_theta) / (1919 * R)
        term_vy_br = vy * ((529 * math.pi * sin_theta) / (1919 * R)) + (cos_theta / (2 * R))
        v_br = term_w + term_vx_br + term_vy_br
        

        # ----------- Impressão formatada -----------

        def print_wheel_velocity(wheel, t_w, t_vx, t_vy, v):
            print(f"\nRoda: {wheel}")
            print(f"{'Termo (w)':<15}: {t_w: .6f}")
            print(f"{'Termo (vx)':<15}: {t_vx: .6f}")
            print(f"{'Termo (vy)':<15}: {t_vy: .6f}")
            print(f"{'Resultado':<15}: {v: .6f}")

        #print("== Velocidades das Rodas (Detalhadas) ==")
#
        #print_wheel_velocity("FL", term_w, term_vx_fl, term_vy_fl, v_fl)
        #print_wheel_velocity("BL", term_w, term_vx_bl, term_vy_bl, v_bl)
        #print_wheel_velocity("FR", term_w, term_vx_fr, term_vy_fr, v_fr)
        #print_wheel_velocity("BR", term_w, term_vx_br, term_vy_br, v_br)
        #print("Wheel Velocities:")
        #print(f"{'Wheel':<10} {'Velocity':<20}")
        #print("-" * 30)
        #print(f"{'FL':<10} {v_fl:<20.6f}")
        #print(f"{'BL':<10} {v_bl:<20.6f}")
        #print(f"{'FR':<10} {v_fr:<20.6f}")
        #print(f"{'BR':<10} {v_br:<20.6f}")

        # Encontrar a velocidade angular máxima entre todas as rodas para normalização
        max_abs_omega = max(abs(v_fl), abs(v_bl), abs(v_fr), abs(v_br))

        # Normaliza as velocidades sprint(f"{vx}")e alguma exceder a capacidade máxima do motor
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
        pwm_fl = min(self.max_motor_pwm, pwm_fl)
        pwm_bl = min(self.max_motor_pwm, pwm_bl)
        pwm_fr = min(self.max_motor_pwm, pwm_fr)
        pwm_br = min(self.max_motor_pwm, pwm_br)
        output = {
        'fl_speed': pwm_fl, 'fl_direction': dir_fl,
        'bl_speed': pwm_bl, 'bl_direction': dir_bl,
        'fr_speed': pwm_fr, 'fr_direction': dir_fr,
        'br_speed': pwm_br, 'br_direction': dir_br,
        }      

        print("Output:")
        print(f"{'Wheel':<10} {'Speed':<10} {'Direction':<10}")
        print("-" * 30)
        print(f"{'FL':<10} {output['fl_speed']:<10} {output['fl_direction']:<10}")
        print(f"{'BL':<10} {output['bl_speed']:<10} {output['bl_direction']:<10}")
        print(f"{'FR':<10} {output['fr_speed']:<10} {output['fr_direction']:<10}")
        print(f"{'BR':<10} {output['br_speed']:<10} {output['br_direction']:<10}")
        print(output)  # <-- Aqui ele mostra as variáveis com os valores atuais
        
        return {
            'fl_speed': pwm_fl, 'fl_direction': dir_fl,
            'bl_speed': pwm_bl, 'bl_direction': dir_bl,
            'fr_speed': pwm_fr, 'fr_direction': dir_fr,
            'br_speed': pwm_br, 'br_direction': dir_br,
        }