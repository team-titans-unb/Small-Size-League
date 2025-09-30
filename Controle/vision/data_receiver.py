from vision.protobuf_messages import wrapper_pb2 as wr

class VisionDataReceiver:
    def __init__(self, vision_client):
        self.sock = vision_client.get_socket()
        if not self.sock:
            raise ValueError("VisionClient não está conectado. Chame client.connect() primeiro.")
        
        self.last_detection_data = None
        self.last_geometry_data = None

    def receive_data(self):
        data = None
        while True:
            try:
                data, _ = self.sock.recvfrom(2048)
                break
            except Exception as e:
                print(f"Erro ao receber dados: {e}")
            if data is not None:
                break

        if data is not None:
            try:
                frame = wr.SSL_WrapperPacket().FromString(data)

                if frame.detection:
                    detection = frame.detection
                    self.last_detection_data = self._parse_detection_frame(detection)

                if frame.geometry:
                    geometry = frame.geometry
                    self.last_geometry_data = self._parse_geometry_data(geometry)
                
                return {
                    'detection': self.last_detection_data,
                    'geometry': self.last_geometry_data,
                }

            except Exception as e:
                print(f"Erro ao processar dados recebidos: {e}")
        
        return None

    def _parse_detection_frame(self, detection_frame):
        parsed_data = {
            'camera_id': detection_frame.camera_id,
            'frame_number': detection_frame.frame_number,
            't_capture': detection_frame.t_capture,
            't_sent': detection_frame.t_sent,
            'balls': [],
            'robots': {
                'blue': [],
                'yellow': []
            }
        }

        for ball in detection_frame.balls:
            parsed_data['balls'].append({
                'confidence': ball.confidence,
                'area': ball.area,
                'x': ball.x,
                'y': ball.y,
                'z': ball.z,
                'pixel_x': ball.pixel_x,
                'pixel_y': ball.pixel_y
            })

        for robot in detection_frame.robots_blue:
            parsed_data['robots']['blue'].append({
                'robot_id': robot.robot_id,
                'confidence': robot.confidence,
                'x': robot.x,
                'y': robot.y,
                'orientation': robot.orientation,
                'pixel_x': robot.pixel_x,
                'pixel_y': robot.pixel_y,
                'height': robot.height
            })
        
        for robot in detection_frame.robots_yellow:
            parsed_data['robots']['yellow'].append({
                'robot_id': robot.robot_id,
                'confidence': robot.confidence,
                'x': robot.x,
                'y': robot.y,
                'orientation': robot.orientation,
                'pixel_x': robot.pixel_x,
                'pixel_y': robot.pixel_y,
                'height': robot.height
            })
        
        return parsed_data

    def _parse_geometry_data(self, geometry_data):
        parsed_data = {
            'field_length': geometry_data.field.field_length,
            'field_width': geometry_data.field.field_width,
        }
        return parsed_data

    def get_last_detection(self):
        return self.last_detection_data
    
    def get_last_geometry(self):
        return self.last_geometry_data

if __name__ == '__main__':
    from client import VisionClient
    import socket
    VISION_IP = '224.5.23.2'
    VISION_PORT = 10006

    client = VisionClient(VISION_IP, VISION_PORT)
    if client.connect():
        print("Cliente de visão configurado. Tente enviar dados para ele.")
        data_receiver = VisionDataReceiver(client)
        try:
            while True:
                vision_info = data_receiver.receive_data()
                detection = vision_info['detection']
                balls = detection['balls']
                if balls:
                    print(f"Dados recebidos: {balls}")
                else:
                    print("Nenhum dado recebido.")
        except KeyboardInterrupt:
            print("Interrompido pelo usuário.")
        finally:
            client.disconnect()