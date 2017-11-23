# HTTP协议是一种文本协议，所以，它的格式也非常简单。HTTP GET请求的格式：
#
# GET /path HTTP/1.1
# Header1: Value1
# Header2: Value2
# Header3: Value3
# 每个Header一行一个，换行符是\r\n。
#
# HTTP POST请求的格式：
#
# POST /path HTTP/1.1
# Header1: Value1
# Header2: Value2
# Header3: Value3
#
# body data goes here...
# 当遇到连续两个\r\n时，Header部分结束，后面的数据全部是Body。

# HTTP响应的格式：
#
# 200 OK
# Header1: Value1
# Header2: Value2
# Header3: Value3
#
# body data goes here...
# HTTP响应如果包含body，也是通过\r\n\r\n来分隔的。
# 请再次注意，Body的数据类型由Content-Type头来确定，如果是网页，Body就是文本，如果是图片，Body就是图片的二进制数据。
# 当存在Content-Encoding时，Body数据是被压缩的，最常见的压缩方式是gzip，
# 所以，看到Content-Encoding: gzip时，需要将Body数据先解压缩，才能得到真正的数据。压缩的目的在于减少Body的大小，加快网络传输。


# application()函数就是符合WSGI标准的一个HTTP处理函数，它接收两个参数：
# environ：一个包含所有HTTP请求信息的dict对象；
# start_response：一个发送HTTP响应的函数。
def application(enviroment, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    body = '<h1>Hello, %s!</h1>' % (enviroment['PATH_INFO'][1:] or 'web')
    return [body.encode('utf-8')]
# 在application()函数中，调用：start_response()就发送了HTTP响应的Header
# 注意Header只能发送一次，也就是只能调用一次start_response()函数。
# start_response()函数接收两个参数，一个是HTTP响应码，一个是一组list表示的HTTP Header，
# 每个Header用一个包含两个str的tuple表示