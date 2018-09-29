
# ------------------------ 协程 -----------------------

def consumer():
    r = ''
    while True:
        print('xxxxxxxxxxx')
        n = yield r
        print('yyyyyyyyyyy')
        print('nnnnnnnnnnn:'+ str(n))
        if not n:
            print('zzzzzzzzzzz')
            return
        print('[Consumer] Consumeing %s...' % n)
        r = '200 OK'
        print('eeeeeeeeeeee')

def produce(c):
    print('aaaaaaaaaaa')
    c.send(None)
    print('bbbbbbbbbbb')
    n = 0
    while n < 5:
        n = n + 1
        print('[Producer] Producing %s' % n)
        print('ccccccccccc')
        r = c.send(n)
        print('ddddddddddd')
        print('[Producer] Consumer return: %s' % r)
    c.close()

c = consumer()
produce(c)

# ------------------------ asyncio ----------------------------

import  asyncio

# @asyncio.coroutine把一个generator标记为coroutine类型，然后，我们就把这个coroutine扔到EventLoop中执行
# @asyncio.coroutine
# def hello():
#     print('Hello world')
#     r = yield from asyncio.sleep(1)
#     print('Hello, again')

# hello()会首先打印出Hello world!，然后，yield from语法可以让我们方便地调用另一个generator。
# 由于asyncio.sleep()也是一个coroutine，所以线程不会等待asyncio.sleep()，而是直接中断并执行下一个消息循环。
# 当asyncio.sleep()返回时，线程就可以从yield from拿到返回值（此处是None），然后接着执行下一行语句。
# 把asyncio.sleep(1)看成是一个耗时1秒的IO操作，在此期间，主线程并未等待，而是去执行EventLoop中其他可以执行的coroutine了，因此可以实现并发执行
# loop = asyncio.get_event_loop()
# loop.run_until_complete(hello())
# loop.close()

@asyncio.coroutine
def wget(host):
    print('wget %s...' % host)
    connect = asyncio.open_connection(host, 80)
    reader, writer = yield from connect
    header = 'GET / HTTP/1.0\r\nHost: %s\r\n\r\n' % host
    writer.write(header.encode('utf-8'))
    yield from writer.drain()
    while True:
        line = yield from reader.readline()
        if line == b'\r\n':
            break
        print('%s header > %s' % (host, line.decode('utf-8').rstrip()))
    writer.close()
# 异步操作需要在coroutine中通过yield from完成；多个coroutine可以封装成一组Task然后并发执行
loop1 = asyncio.get_event_loop()
tasks = [wget(host) for host in ['www.sina.com.cn', 'www.sohu.com', 'www.163.com']]
loop1.run_until_complete(asyncio.wait(tasks))
loop1.close()

# async和await是针对coroutine的新语法，要使用新的语法，只需要做两步简单的替换：
# 把@asyncio.coroutine替换为async；
# 把yield from替换为await
async def hello():
    print('Hello world')
    r = await asyncio.sleep(1)
    print('Hello, again')

# loop = asyncio.get_event_loop()
# loop.run_until_complete(hello())
# loop.close()











