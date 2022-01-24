from pathlib import Path

from utils import send, receive

import socket
import hashlib

def handle_list(user: str) -> str:
    path = Path('./server/' + user)

    if len(list(path.iterdir())):
        ret = '\n\t-'.join(i.name for i in path.iterdir())
    else:
        ret = 'The directory is empty.'

    return ret

def handle_upload(file: Path, sockfd: socket.socket, chunk_size=512) -> None:
    print(file)
    send(sockfd, file.name)
    checksum = hashlib.sha256()

    with open(file, mode='rb') as fd:
        while True:
            data = fd.read(chunk_size)
            
            if not data:
                print('File sent')
                break
            checksum.update(data)
            sockfd.send(data)

        confirm = sockfd.recv(2)
        digest = checksum.hexdigest()
        print(digest)

        if confirm == b'OK':
            sockfd.send(digest.encode())

def handle_download(user:str, sockfd: socket.socket, chunk_size=512) -> str:
    filename = receive(sockfd)
    checksum = hashlib.sha256()

    with open(f'./server/{user}/{filename}', mode='wb') as fd:
        print('Downloading file:', filename)

        while True:
            recv = sockfd.recv(chunk_size)

            fd.write(recv)
            checksum.update(recv)

            if len(recv) < chunk_size:
                print('File downloaded')
                break
            
            print(recv)
        
        sockfd.send(b'OK')
        remote_checksum = sockfd.recv(1024).decode()
        hexdigest = checksum.hexdigest()
        print(hexdigest)

        ret = 'File received successfully'

        if remote_checksum != hexdigest:
            ret = 'File corrupted. Different SHA256 checksum\n'
            ret += '\t Client SHA256: ' + remote_checksum + '\n' 
            ret += '\t Server SHA256: ' + hexdigest + '\n'

        return ret

HANDLERS = {
    'list': handle_list,
    'upload': handle_upload,
    'download': handle_download
}
