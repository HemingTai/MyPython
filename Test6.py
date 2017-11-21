# <-----------网络编程---------->!
# -*- coding: utf-8 -*-

import socket, threading, time

# 创建Socket时，AF_INET指定使用IPv4协议，如果要用更先进的IPv6，就指定为AF_INET6。SOCK_STREAM指定使用面向流的TCP协议，
# 这样，一个Socket对象就创建成功，但是还没有建立连接
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 客户端要主动发起TCP连接，必须知道服务器的IP地址和端口号。新浪网站的IP地址可以用域名www.sina.com.cn自动转换到IP地址，但是怎么知道新浪服务器的端口号呢？
# 答案是作为服务器，提供什么样的服务，端口号就必须固定下来。由于我们想要访问网页，因此新浪提供网页服务的服务器必须把端口号固定在80端口，
# 因为80端口是Web服务的标准端口。其他服务都有对应的标准端口号，例如SMTP服务是25端口，FTP服务是21端口，等等。
# 端口号小于1024的是Internet标准服务的端口，端口号大于1024的，可以任意使用
# 注意参数是一个tuple，包含地址和端口号。
s.connect(('www.sina.com.cn', 80))
# 建立TCP连接后，我们就可以向新浪服务器发送请求，要求返回首页的内容
s.send(b'GET / HTTP/1.1\r\nHost: www.sina.com.cn\r\nConnection: close\r\n\r\n')
# 接收数据,调用recv(max)方法，一次最多接收指定的字节数，因此，在一个while循环中反复接收，直到recv()返回空数据，表示接收完毕，退出循环。
buffer = []
while True:
    d = s.recv(1024)
    if d:
        buffer.append(d)
    else:
        break
data = b''.join(buffer)
# 当我们接收完数据后，调用close()方法关闭Socket，这样，一次完整的网络通信就结束了
s.close()
# 接收到的数据包括HTTP头和网页本身，我们只需要把HTTP头和网页分离一下，把HTTP头打印出来，网页内容保存到文件
header, html = data.split(b'\r\n\r\n', 1)
print(header.decode('utf-8'))
with open('sina.html', 'wb') as f:
    f.write(html)




