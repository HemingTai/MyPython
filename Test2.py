import base64
import hashlib
import itertools
import re
import struct
from collections import namedtuple, deque, defaultdict, OrderedDict, Counter
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from xml.parsers.expat import ParserCreate
from html.parser import HTMLParser
from html.entities import name2codepoint

# datetime.now()返回当前日期和时间，其类型是datetime
now = datetime.now()
print(now)
print(type(now))
# 要指定某个日期和时间，我们直接用参数构造一个datetime
dt = datetime(2017,11,14,14,23,55)
print(dt)
# 把一个datetime类型转换为timestamp只需要简单调用timestamp()方法,注意Python的timestamp是一个浮点数,如果有小数位，小数位表示毫秒数
print(dt.timestamp())
# 要把timestamp转换为datetime，使用datetime提供的fromtimestamp()方法
t = 1510640000.0
print(datetime.fromtimestamp(t))
# 注意到timestamp是一个浮点数，它没有时区的概念，而datetime是有时区的。上述转换是在timestamp和本地时间做转换。本地时间是指当前操作系统设定的时区
# timestamp也可以直接被转换到UTC标准时区的时间(格林威治标准时间)
print(datetime.utcfromtimestamp(t))
# 字符串'%Y-%m-%d %H:%M:%S'规定了日期和时间部分的格式
print(datetime.strptime('2017-11-14 14:37:40', '%Y-%m-%d %H:%M:%S'))
print(datetime.strptime('2017/11/14 14/30/40','%Y/%m/%d %H/%M/%S'))
# 如果已经有了datetime对象，要把它格式化为字符串显示给用户，就需要转换为str，转换方法是通过strftime()实现的，同样需要一个日期和时间的格式化字符串
print(now.strftime('%Y %b %d %a %H:%M:%S'))
# 对日期和时间进行加减实际上就是把datetime往后或往前计算，得到新的datetime。加减可以直接用+和-运算符，不过需要导入timedelta这个类
print(now+timedelta(hours=10))
print(now+timedelta(days=1))
print(now+timedelta(days=1,hours=4))
# 一个datetime类型有一个时区属性tzinfo，但是默认为None，所以无法区分这个datetime到底是哪个时区，除非强行给datetime设置一个时区
tz_utc_8 = timezone(timedelta(hours=8))
nnow = datetime.now()
print(nnow)
print(nnow.replace(tzinfo=tz_utc_8))
# 通过utcnow()拿到当前的UTC时间
utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
print(utc_dt)
bj_dt = utc_dt.astimezone(timezone(timedelta(hours=8)))
print(bj_dt)

def to_timestamp(dt_str, tz_str):
    re_timezone = re.compile(r'^UTC([+-])0?(\d{1,2}):[0-5][0-9]$')
    if re_timezone.match(tz_str):
        s = re_timezone.match(tz_str).group(1)
        t = re_timezone.match(tz_str).group(2)
        print('t=',t)
        ot = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
        if s == '+':
            nt = ot.astimezone(timezone(timedelta(hours=int(t))))
        else:
            nt = ot.astimezone(timezone(timedelta(hours=-int(t))))
        print('nt=',nt)
        return nt.timestamp()

pt1 = to_timestamp('2015-6-1 08:10:30', 'UTC+7:00')
print('pt1=',pt1)
pt2 = to_timestamp('2015-5-31 16:10:30', 'UTC-09:00')
print('pt2=',pt2)

# namedtuple是一个函数，它用来创建一个自定义的tuple对象，并且规定了tuple元素的个数，并可以用属性而不是索引来引用tuple的某个元素
Point = namedtuple('Point', ['x', 'y'])
p = Point(1,2)
print(p)
print(p.x)
print(p.y)

# deque是为了高效实现插入和删除操作的双向列表，适合用于队列和栈
# deque除了实现list的append()和pop()外，还支持appendleft()和popleft()，这样就可以非常高效地往头部添加或删除元素
q = deque(['a','b','c'])
q.append('x')
q.appendleft('y')
print(q)
q.pop()
print(q)
q.popleft()
print(q)

# 使用dict时，如果引用的Key不存在，就会抛出KeyError。如果希望key不存在时，返回一个默认值，就可以用defaultdict
dd = defaultdict(lambda :'N/A')
dd['key'] = 'abc'
print(dd['key'])
print(dd['key1'])# key1不存在，返回默认值
# 使用dict时，Key是无序的。在对dict做迭代时，我们无法确定Key的顺序。如果要保持Key的顺序，可以用OrderedDict
d = dict([('a',1),('b',2),('c',3),('d',4)])
print(d)
# 注意，OrderedDict的Key会按照插入的顺序排列，不是Key本身排序
od = OrderedDict([('a',1), ('b',2),('c',3),('d',4)])
print(od)
print(od.keys())

# OrderedDict可以实现一个FIFO（先进先出）的dict，当容量超出限制时，先删除最早添加的Key
class LastUpdatedOrderDict(OrderedDict):
    def __init__(self, capacity):
        super(LastUpdatedOrderDict, self).__init__()
        self._capacity = capacity

    def __setitem__(self, key, value):
        containsKey = 1 if key in self else 0
        if len(self)- containsKey >= self._capacity:
            last = self.popitem(last=False)
            print('remove:', last)
        if containsKey:
            del self[key]
            print('set:',(key, value))
        else:
            print('add:',(key, value))
        OrderedDict.__setitem__(self,key,value)

luod = LastUpdatedOrderDict(3)
luod['a'] = 1
luod['b'] = 2
luod['c'] = 3
print(luod)
luod['d'] = 4
print(luod)

# Counter是一个简单的计数器，例如，统计字符出现的个数
c = Counter()
for ch in 'programming':
    c[ch] = c[ch] + 1
print(c)

# base64编码
print(base64.b64encode(b'binary\x00string'))
print(base64.b64decode(b'YmluYXJ5AHN0cmluZw=='))
# 由于标准的Base64编码后可能出现字符+和/，在URL中就不能直接作为参数，所以又有一种"url safe"的base64编码，其实就是把字符+和/分别变成-和_
print(base64.b64encode(b'i\xb7\x1d\xfb\xef\xff'))
print(base64.urlsafe_b64encode(b'i\xb7\x1d\xfb\xef\xff'))
print(base64.urlsafe_b64decode('abcd--__'))

# 如果要编码的二进制数据不是3的倍数，最后会剩下1个或2个字节，Base64用\x00字节在末尾补足后，
# 再在编码的末尾加上1个或2个=号，表示补了多少字节，解码的时候，会自动去掉
def safe_base64_decode(s):
    if isinstance(s,bytes):
        s = str(s, encoding='utf-8')
    yu = len(s) % 4
    return base64.b64decode(s+'='*yu)
print(safe_base64_decode('YWJjZA'))

# struct的pack函数把任意数据类型变成bytes，pack的第一个参数是处理指令，'>I'的意思是：
# >表示字节顺序是big-endian，也就是网络序，I表示4字节无符号整数。
# 后面的参数个数要和处理指令一致
print(struct.pack('>I', 10240099))
# unpack把bytes变成相应的数据类型
# 根据>IH的说明，后面的bytes依次变为I：4字节无符号整数和H：2字节无符号整数
print(struct.unpack('>IH',b'\xf0\xf0\xf0\xf0\x80\x80'))

s = b'\x42\x4d\x38\x8c\x0a\x00\x00\x00\x00\x00\x36\x00\x00\x00\x28\x00\x00\x00\x80\x02\x00\x00\x68\x01\x00\x00\x01\x00\x18\x00'
struct.unpack('<ccIIIIIIHH',s)

def checkFileIsBMP(path):
    with open(path,'rb') as f:
        bs = f.read(30)
        result = struct.unpack('<ccIIIIIIHH',bs)
        if result[1] == b'M' or result[1] == b'A':
            print('此文件是位图')
            print('size:%s colors:%s' % (result[2],result[-1]))
        else:
            print('此文件不是位图')

# 计算出一个字符串的MD5值，MD5的结果是固定的128 bit字节，通常用一个32位的16进制字符串表示
md5 = hashlib.md5()
md5.update('how to use md5 in python hashlib?'.encode('utf-8'))
print(md5.hexdigest())
md5.update('how to use md4 in python hashlib?'.encode('utf-8'))
print(md5.hexdigest())
# 计算出一个字符串的SHA1值，SHA1的结果是160 bit字节，通常用一个40位的16进制字符串表示
sha1 = hashlib.sha1()
sha1.update('how to use sha1 in python hashlib?'.encode('utf-8'))
print(sha1.hexdigest())
sha1.update('how to use sha2 in python hashlib?'.encode('utf-8'))
print(sha1.hexdigest())

db = {
    'michael': 'e10adc3949ba59abbe56e057f20f883e',
    'bob': '878ef96e86145580c38c87f0410ad153',
    'alice': '99b1c2188db85afee403b1536010c2c9'
}
def string2md5(str):
    md5 = hashlib.md5()
    md5.update(str.encode('utf-8'))
    return md5.hexdigest()
def login(userName, password):
    for name in db.keys():
        if userName == name:
            if string2md5(password) == db[name]:
                print('login success!')
            else:
                print('wrong password!')
            break

login('alice','alice2008')
newdb = {}
# 由于常用口令的MD5值很容易被计算出来，所以，要确保存储的用户口令不是那些已经被计算出来的常用口令的MD5，这一方法通过对原始口令加一个复杂字符串来实现，俗称“加盐”
def register(userName, password):
    newdb[userName] = string2md5(password+userName+'badboy')
register('alice','alice2008')
def newLogin(userName, password):
    for name in newdb.keys():
        if userName == name:
            if string2md5(password+userName+'badboy') == newdb[name]:
                print('login success!')
            else:
                print('wrong password!')
            break
newLogin('alice','alice2008')

# itertools模块提供的全部是处理迭代功能的函数，它们的返回值不是list，而是Iterator，只有用for循环迭代的时候才真正计算
# count()会创建一个无限的迭代器，所以以下代码会打印出自然数序列，根本停不下来
# 无限序列虽然可以无限迭代下去，但是通常我们会通过takewhile()等函数根据条件判断来截取出一个有限的序列
natuals = itertools.count(1)
# for n in natuals:
#     print(n)
nas = itertools.takewhile(lambda x: x <= 10, natuals)
print(list(nas))
# cycle()会把传入的一个序列无限重复下去
# cs = itertools.cycle('ABCD')
# for c in cs:
#     print(c)
# repeat()负责把一个元素无限重复下去，不过如果提供第二个参数就可以限定重复次数
ns = itertools.repeat('A',3)
for n in ns:
    print(n)
# chain()可以把一组迭代对象串联起来，形成一个更大的迭代器
for c in itertools.chain('ABCD', 'XYZ'):
    print(c)
# groupby()把迭代器中相邻的重复元素挑出来放在一起
for key, group in itertools.groupby('AAAAAVVVVFFFDDDSSSS'):
    print(key, list(group))
# 实际上挑选规则是通过函数完成的，只要作用于函数的两个元素返回的值相等，这两个元素就被认为是在一组的，而函数返回值作为组的key。如果我们要忽略大小写分组，就可以让元素'A'和'a'都返回相同的key
for key, group in itertools.groupby('AAAaaaVVVVvFFffFDdDDSssSSS', lambda c: c.upper()):
    print(key, list(group))
# 任何对象，只要正确实现了上下文管理，就可以用于with语句。实现上下文管理是通过__enter__和__exit__这两个方法实现的
class Query(object):
    def __init__(self, name):
        self.name = name
    def __enter__(self):
        print('begin')
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print('Error')
        else:
            print('End')
    def query(self):
        print('Query info about %s ...' % self.name)

with Query('Bob') as q:
    q.query()

class NewQuery(object):
    def __init__(self, name):
        self.name = name
    def newQuery(self):
        print('Query info about %s ...' % self.name)

# @contextmanager这个decorator接受一个generator，用yield语句把with ... as var把变量输出出去，然后，with语句就可以正常地工作了
@contextmanager
def create_query(name):
    print('begin')
    q = NewQuery(name)
    yield q
    print('End')
with create_query('Alice') as nq:
    nq.newQuery()

@contextmanager
def tag(name):
    print('<%s>' % name)
    yield
    print('</%s>' % name)
# 代码的执行顺序是：
# with语句首先执行yield之前的语句，因此打印出<h1>；
# yield调用会执行with语句内部的所有语句，因此打印出hello和world；
# 最后执行yield之后的语句，打印出</h1>。
with tag('h1'):
    print('hello')
    print('heming')
# 如果一个对象没有实现上下文，我们就不能把它用于with语句。这个时候，可以用closing()来把该对象变为上下文对象
# with closing(urlopen('http://www.python.org')) as page:
#     for line in page:
#         print(line)
# closing也是一个经过@contextmanager装饰的generator
@contextmanager
def closing(thing):
    try:
        yield thing
    finally:
        thing.close()

class DefaultSaxHandler(object):
    def start_element(self, name, attrs):
        print('sax:start_element: %s, attrs: %s' % (name, attrs))

    def end_element(self, name):
        print('sax:end_element: %s' % name)

    def char_data(self, text):
        print('sax:char_element: %s' % text)

xml = r'''<?xml version="1.0"?>
<ol>
    <li><a href="/python">Python</a></li>
    <li><a href="/ruby">Ruby</a></li>
</ol>
'''
# 需要注意的是读取一大段字符串时，CharacterDataHandler可能被多次调用，所以需要自己保存起来，在EndElementHandler里面再合并
handler = DefaultSaxHandler()
parser = ParserCreate()
parser.StartElementHandler = handler.start_element
parser.EndElementHandler = handler.end_element
parser.CharacterDataHandler = handler.char_data
parser.Parse(xml)

weatherXML = r'''<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<rss version="2.0" xmlns:yweather="http://xml.weather.yahoo.com/ns/rss/1.0" xmlns:geo="http://www.w3.org/2003/01/geo/wgs84_pos#">
    <channel>
        <title>Yahoo! Weather - Beijing, CN</title>
        <lastBuildDate>Wed, 27 May 2015 11:00 am CST</lastBuildDate>
        <yweather:location city="Beijing" region="" country="China"/>
        <yweather:units temperature="C" distance="km" pressure="mb" speed="km/h"/>
        <yweather:wind chill="28" direction="180" speed="14.48" />
        <yweather:atmosphere humidity="53" visibility="2.61" pressure="1006.1" rising="0" />
        <yweather:astronomy sunrise="4:51 am" sunset="7:32 pm"/>
        <item>
            <geo:lat>39.91</geo:lat>
            <geo:long>116.39</geo:long>
            <pubDate>Wed, 27 May 2015 11:00 am CST</pubDate>
            <yweather:condition text="Haze" code="21" temp="28" date="Wed, 27 May 2015 11:00 am CST" />
            <yweather:forecast day="Wed" date="27 May 2015" low="20" high="33" text="Partly Cloudy" code="30" />
            <yweather:forecast day="Thu" date="28 May 2015" low="21" high="34" text="Sunny" code="32" />
            <yweather:forecast day="Fri" date="29 May 2015" low="18" high="25" text="AM Showers" code="39" />
            <yweather:forecast day="Sat" date="30 May 2015" low="18" high="32" text="Sunny" code="32" />
            <yweather:forecast day="Sun" date="31 May 2015" low="20" high="37" text="Sunny" code="32" />
        </item>
    </channel>
</rss>'''
class WeatherSaxHandler(object):
    def start_element(self, name, attrs):
        if name == 'yweather:location' or name == 'pubDate' or name == 'yweather:condition' or name == 'yweather:forecast':
            print('sax:start_element: %s, attrs: %s' % (name, attrs))

def parseWeather(xml):
    handler = WeatherSaxHandler()
    parser = ParserCreate()
    parser.StartElementHandler = handler.start_element
    parser.Parse(xml)

parseWeather(weatherXML)

# feed()方法可以多次调用，也就是不一定一次把整个HTML字符串都塞进去，可以一部分一部分塞进去。
# 特殊字符有两种，一种是英文表示的&nbsp;，一种是数字表示的&#1234;，这两种字符都可以通过Parser解析出来。
class MyHTMLParser(HTMLParser):

    def handler_starttag(self, tag, attrs):
        print('<%s>' % tag)
        print('%s' % attrs)

    def handle_endtag(self, tag):
        print('</%s>' % tag)

    def handle_startendtag(self, tag, attrs):
        print('<%s/>' % tag)
        print('%s' % attrs)

    def handle_data(self, data):
        print(data)

    def handle_comment(self, data):
        print('<!--', data, '-->')

    def handle_entityref(self, name):
        print('&%s;' % name)

    def handle_charref(self, name):
        print('&#%s;' % name)

htmlParser = MyHTMLParser()
htmlParser.feed('''<html>
<head></head>
<body>
<!-- test html parser -->
    <p>Some <a href=\"#\">html</a> HTML&nbsp;tutorial...<br>END</p>
</body></html>''')












