import socket

from utils import receive, send

from handlers import HANDLERS, handle_download

from pathlib import Path

SERVER_PATH = Path('./server')

if __name__ == '__main__':

    if not SERVER_PATH.exists():
        SERVER_PATH.mkdir()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sockfd:
        sockfd.setsockopt(socket.SOL_SOCKET , socket.SO_REUSEADDR, 1)
        sockfd.bind(('localhost', 10900))

        sockfd.listen()

        while True:
            conn, addr = sockfd.accept()
            user = receive(conn)
            user_path = SERVER_PATH.joinpath(user)

            if not user_path.exists():
                print('First login of the user! Creating a directory for him/her.')
                user_path.mkdir()

            print('Connection accepted for user', user)
            print(*addr)

            while True:
                try:
                    msg = receive(conn)
                    print('Received:', msg)

                    cmd_func = HANDLERS.get(msg)

                    resp = 'OK'
                    if msg == 'list':
                        resp = cmd_func(user)
                    elif msg == 'upload':
                        resp = handle_download(user, conn)
                    elif msg == 'download':
                        pass

                    send(conn, resp)
                except EOFError:
                    addr, port = conn.getpeername()
                    print(f'Client {addr}:{port} disconnected')
                    break