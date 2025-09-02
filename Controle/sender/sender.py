from abc import ABC, abstractmethod
import socket

class Sender(ABC):
    @abstractmethod
    def send_command(sekf, *args, **kwargs):
        pass

    