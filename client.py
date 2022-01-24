import socket

from pathlib import Path

from utils import receive, send

from handlers import HANDLERS

CLIENT_PATH = Path('./client')

if __name__ == '__main__':
    if not CLIENT_PATH.exists():
        CLIENT_PATH.mkdir()
        
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sockfd:
        user = input('Username: ')
        sockfd.connect(('localhost', 10900))
        send(sockfd, user)

        while True:
            msg = input('>>> ')

            if msg == 'upload':
                file_exists = False
                while not file_exists:
                    file = CLIENT_PATH / Path(input('Relative file path: '))

                    if not file.exists():
                        print(f'File \'{str(file)}\' does not exist.')
                    else:
                        break
                send(sockfd, msg)
                HANDLERS[msg](file, sockfd)
            else:
                send(sockfd, msg)

            response = receive(sockfd)
            print('Response:', response)
