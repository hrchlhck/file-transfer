import pickle
import socket

__all__ = [
    'send', 'receive'
]

def send(sockfd: socket.socket, data: object) -> None:
    obj = pickle.dumps(data)
    sockfd.send(obj)

def receive(sockfd: socket.socket, buffer_size=1024) -> object:
    return pickle.loads(sockfd.recv(buffer_size))