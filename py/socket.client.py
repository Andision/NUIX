import socket
# 1创建接字
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 2创建广播权,默认不允许发送广播
# udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)
udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# 3绑定端口
udp_socket.bind(("0.0.0.0", 7002))
# 4发送广播
# content = struct.pack("3l?5l", 0xF2, 0x01, 0x09, True, 0x00, 0x00, 0x00, 0x00, 0x16)
content = b'NUIX connect request'
# python3发送bytes，str.encode()可转成bytes
udp_socket.sendto(content, ("192.168.10.255", 60000))
# print(struct.unpack("3l?5l", content))
