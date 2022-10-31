import socket
import time

PORT = 60000
sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sk.settimeout(200000)
sk.bind(('0.0.0.0', PORT))
while True:
    msg, addr = sk.recvfrom(1024)
    print(time.strftime("%H:%M:%S"))
    print(f'from {addr[0]}:{addr[1]}, msg: {msg}')
    if msg == b'NUIX connect request':
        print('print')
        sk.sendto('NUIX connect received'.encode('utf-8'), addr)