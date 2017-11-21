import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
for data in [b'heming', b'badboy', b'david']:
    s.sendto(data, ('127.0.0.1', 9999))
    # 从服务器接收数据仍然调用recv()方法
    print(s.recv(1024).decode('utf-8'))
s.close()
