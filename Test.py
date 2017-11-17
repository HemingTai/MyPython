#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# python导入模块有三种方式：
# 1.直接通过import方式，但是这种方式只是导入了模块，如果要使用模块中的函数或属性等，必须要包含模块名，不能直接使用方法名，如math.sqrt()
# 2.通过 from 模块名 import 函数名 方式，如from collections import Iterable，这种方式可以直接使用函数名而不需要模块名
# 3.内建函数__import__() ,除了前面两种使用import关键字的方法以外，
# 还可以使用内建函数 __import__() 来导入module。两者的区别是，import 后面跟的必须是一个类型(type)，
# 而__import__() 的参数是一个字符串，这个字符串可能来自配置文件，也可能是某个表达式计算结果。
import math
from collections import Iterable
from collections import Iterator
import os, time, random, threading
from functools import reduce
import functools
from PIL import Image
import sys
from types import MethodType
from enum import  Enum, unique
import logging
logging.basicConfig(level=logging.INFO)
import re
from io import StringIO, BytesIO
import pickle
import json
from multiprocessing import Process, Pool, Queue
import subprocess



print('你好，世界')
a = 'ABC'.encode('ascii')
print(a)
b = '中国'.encode('utf-8')
print(b)
print(a.decode('ascii'))
print(b.decode('utf-8'))
print(len('abcde'))
print(len('我爱你中国！'))
print('PI = %.2f' % 3.1415926)
print('Hello,%s, you have $%d.' % ('hem1ng', 100))

S1 = 72
S2 = 85
p = (S2 - S1) / S1 * 100
print('p = %.f %%' % p)
workmate = ['a', 'b', 'c']
print(workmate)
print(len(workmate))
print(workmate[0])
print(workmate[2])
# -1表示直接去数组末尾的数据
print(workmate[-1])

# append是在数组末尾增加，而insert可以插入到指定位置，pop(i)是删除数组指定位置元素,i不赋值则默认删除末尾元素
workmate.append('d')
print(workmate)
workmate.insert(2, 'f')
print(workmate)
workmate.pop()
print(workmate)
workmate.pop(1)
print(workmate)

workmate[1] = 'b'
print(workmate)

L = ['abc', 123, True]
print(L)
M = []
print(len(M))

classmate = ('Alice', 'Bob', 'Catherine')
print(classmate)
print(classmate[1])
print(classmate[-1])
N = (1,)
print(N)

Q = [['Apple', 'Google', 'Microsoft'], ['Java', 'Python', 'Ruby', 'PHP'], ['Adam', 'Bart', 'Lisa']]
print(Q[0][0])
print(Q[1][1])
print(Q[-1][-1])

# elif 是else if 的缩写
age = 18
if age >= 18:
    print('ur age is %d' % age)
    print('adult')
elif age >= 8:
    print('teenager')
else:
    print('baby')

year = '1992'
if int(year) > 2000:
    print('00后')
else:
    print('00前')

weight = 80.5
height = 1.75
p = weight / pow(height, 2)
if p < 18.5:
    print('过轻')
elif p < 25:
    print('正常')
elif p < 28:
    print('过重')
elif p < 32:
    print('肥胖')
else:
    print('严重肥胖')

# 循环语句，依次打印
for item in workmate:
    print(item)

litter = ''
for item in workmate:
    litter += item
print(litter)

# range(X)表示生成一个从0开始，小于X的整数序列，如：range(101)表示从0-100的连续整数序列,list()表示将序列转换成数组
sum1 = 0
x = range(101)
print('x =', x)
y = list(x)
print('y =', y)
# 这里遍历的时候可以是序列即x，也可以是数组即y
for p in y:
    print('p =', p)
    sum1 += p
print('sum =', sum1)

num = 1
sum2 = 0
while num < 100:
    sum2 += num
    if sum2 > 1500:
        break
    num += 2
print(num)
print(sum2)

L = ['Bart', 'Lisa', 'Adam']
for name in L:
    if name == 'Lisa':
        continue
    print('Hello, %s!' % name)

# 如果dict不存在键值，get()则默认返回None，也可以返回指定的值如：no
d = {'Michael': 95, 'Bob': 75, 'Tracy': 85}
print(d['Bob'])
d['Hem1ng'] = 99
print(d)
print(d.get('Tai', 'no'))
d.pop('Tracy')
print(d)

# set也是一个集合，但是set集合不存在相同的元素，也不是一个有序的集合
# add(key)添加元素，remove(key)删除元素
s = {1, 2, 3, 4, 2, 3, 5, 1}
print(s)
s.add(3)
print(s)
s.add(6)
print(s)
s.remove(3)
print(s)

s0 = {2, 3, 7}
print(s & s0)  # 两个集合的交集
print(s | s0)  # 两个集合的并集

a = ['c', 'b', 'd', 'a']
a.sort()
print(a)

# replace()只是拷贝了一份并替换了字符，原始的字符串并没有改变
b = 'aback'
print(b.replace('b', 'f'))
print(b)

c = max(1, 2, 3, 4, 5)
print(c)

n1 = 255
n2 = 1000
print(hex(n1))
print(hex(n2))

d = min
print(d(1, 3, 6))


def my_abs(x):
    if not isinstance(x, (int, float)):
        raise TypeError('bad operand type')
    if x >= 0:
        return x
    else:
        return -x

f = my_abs(4)
print(f)


def quadratic(a, b, c):
    d = pow(b, 2) - 4 * a * c
    if d >= 0:
        m = (-b + math.sqrt(d)) / (2 * a)
        n = (-b - math.sqrt(d)) / (2 * a)
        if n == m:
            return m
        else:
            return m, n
    else:
        return '无解'

print(quadratic(1, -2, 1))
print(quadratic(2, 3, 1))
print(quadratic(1, 3, -4))
print(quadratic(1, 1, 3))

# n=2表示n的默认值为2，调用函数的时候可以给定x参数即可，如power(5)返回的结果就是25
def power(x, n=2):
    s = 1
    if x > 0:
        while n > 0:
            n = n - 1
            s = s * x
        return s

print(power(5, 2))
print(power(5, 3))
print(power(6))

x = 5
if x is 5:
    print('YES')

# *表示可变参数，可以不传参数，传1个参数，传多个参数，或者传入一个tuple
def cal(*nums):
    sums = 0
    for n in  nums:
        sums = sums + pow(n, 2)
    return sums

print(cal())
print(cal(9))
print(cal(1, 2, 3))
print(cal(*[4, 5, 6]))

# **表示关键字参数，该参数会被转换成dict，可以传也可以不传，或者传入一个dict，调用的时候必须传入参数名
def enroll(name, age, **kw):
    print('name: %s, age: %d, other:%s' %(name, age, kw))

enroll('LiuDi', 22)
enroll('hem1ng', 22, city = 'Shanghai', love = 'LD')
enroll('LD', 23, **{'job':'IT'})

# *后面的参数表示命名关键字参数，只接受后面关键字的参数，调用的时候必须传入参数名
def person(name, age, *, father, mather):
    print(name, age, father, mather)

person('david', 22, father='jack', mather='lucy')

def digui(m):
    if m == 1:
        return 1
    return m * digui(m - 1)
print(digui(10))

# 3阶汉诺塔实现从A支架借助B支架移动到C支架上的步骤
def move(n, a, b, c):
    if n == 1:
        print(a, '-->', c)
        return
    move(n-1, a, c, b)
    move(1, a, b, c)
    move(n - 1, b, a, c)

move(3, 'A', 'B', 'C')

# 利用切片获取数组中的元素，names[0:3]表示取数组的前三个元素，不包括下标3对应的元素，
# 如果第一个下标是0还可以省略，直接是names[:3]，names[-3:]表示取数组后三个元素
names = ['A','B', 'C', 'D', 'E']
print(names[0:3])
print(names[-3:])

numbers = list(range(100))
print(numbers[:10])
print(numbers[-10:])
print(numbers[:10:2])
print(numbers[::5])

print((1, 2, 3, 4, 5)[:3])
print('Hem1ngTai'[:2])
print('Hem1ngTai'[::2])

# 遍历字典
d = {'a':1, 'b':2, 'c':3}
for k in d:
    print(k)
for v in d.values():
    print(v)
for k, v in d.items():
    print(k, v)

# enumerate函数可以把一个list变成索引-元素对
for i, v in enumerate([4, 5, 6]):
    print(i, v)

# Iterable表示判断一个对象是否是可迭代对象
print(isinstance('abc', Iterable))
print(isinstance(['a', 'b', 'c'], Iterable))
print(isinstance(123, Iterable))

# 写列表生成式([])时，把要生成的元素x * x放到前面，后面跟for循环，就可以把list创建出来
print([x * x for x in range(1,10)])
# for循环后面还可以加上if判断
print([x * x for x in range(1,10) if x % 2 == 0])
# 生成全排列
print([x + y for x in 'ABCD' for y in 'WXYZ'])
# 生成当前目录下的所有文件和目录名
print([d for d in os.listdir('.')])
# 转换小写
print([s.lower() for s in ['A', 'B', 'C', 'D', 'E', 'F']])

L1 = ['Hello', 'World', 18, 'Apple', None]
print([s.lower() for s in  L1 if isinstance(s, str)])

# 生成器和生成式的区别在于()和[]，生成器保存的是算法
g = (x * x for x in range(1,10))
print(g)
for n in g:
    print(n)

def fib(maxN):
    n, a, b = 0, 0, 1
    while n < maxN:
        # print(b)
        yield b
        a, b = b, a + b
        n = n + 1
g = fib(6)
for n in g:
    print(n)

# 杨辉三角
def triangles(lines):
    a = [1]
    for n in range(lines):
        yield a
        a = [1]+[a[i]+a[i+1] for i in range(n)]+[1]
g = triangles(10)
for n in g:
    print(n)

# 生成器都是Iterator对象，但list、dict、str虽然是Iterable，却不是Iterator。把list、dict、str等Iterable变成Iterator可以使用iter()函数
print(isinstance([1,2,3], Iterator))
print(isinstance(iter([1,2,3]), Iterator))
# 凡是可作用于for循环的对象都是Iterable类型；
# 凡是可作用于next()函数的对象都是Iterator类型，它们表示一个惰性计算的序列；
# 集合数据类型如list、dict、str等是Iterable但不是Iterator，不过可以通过iter()函数获得一个Iterator对象。

def add(x, y, f):
    return f(x) + f(y)
print(add(-3,2,abs))

# map()函数接收两个参数，一个是函数，一个是Iterable，map将传入的函数依次作用到序列的每个元素，并把结果作为新的Iterator返回
def f(x):
    return x * x
r = map(f, [1,2,3,4,5,6,7,8,9])
print(list(r))

s = map(str, [1,2,3,4,5])
print(list(s))

# reduce把一个函数作用在一个序列[x1, x2, x3, ...]上，这个函数必须接收两个参数，reduce把结果继续和序列的下一个元素做累加计算
def add(x, y):
    return x + y
t = reduce(add, [1,2,3,4,5])
print(t)

def meger(x, y):
    return x * 10 + y
u = reduce(meger, [1,2,3,4,5])
print(u)

def normalize(name):
    return name[0].upper() + name[1:].lower()

L2 = ['adam', 'LISA', 'barT']
print(list(map(normalize, L2)))

def prod(L):
    def Cheng(x, y):
        return x * y
    return reduce(Cheng, L)
print('3 * 5 * 7 * 9 =', prod([3,5,7,9]))

def str2float(s):
    def Cheng(x, y):
        return x * 10 + y
    def char2num(s):
        return {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}[s]
    s1, s2 = s.split('.')
    return reduce(Cheng,list(map(int, s1)))+ reduce(Cheng, list(map(int, s2)))/pow(10, len(s2))

print('str2float(\'123.456\') =', str2float('123.456'))

# 和map()类似，filter()也接收一个函数和一个序列。和map()不同的是，filter()把传入的函数依次作用于每个元素，然后根据返回值是True还是False决定保留还是丢弃该元素
def is_odd(n):
    return n % 2 == 0
print(list(filter(is_odd,[1,3,4,5,6,7,8])))

def _odd_iter():
    n = 1
    while True:
        n = n + 2
        yield n
def _not_divisible(n):
    return lambda x:x % n > 0

def prime():
    yield 2
    it = _odd_iter()
    while True:
        n = next(it)
        yield n
        it = filter(_not_divisible(n), it)
for n in prime():
    if n < 10:
        print(n)
    else:
        break

def is_palindrome(n):
    return len(str(n))>1 and n == int(str(n)[::-1])
print(list(filter(is_palindrome,list(range(1,100)))))

# key指定排序的方式
print(sorted([2, 15,-6,8,3]))
print(sorted([2, 15,-6,8,3],key = abs))
print(sorted(['bob', 'about', 'Zoo', 'Credit']))
print(sorted(['bob', 'about', 'Zoo', 'Credit'], key = str.lower))
print(sorted(['bob', 'about', 'Zoo', 'Credit'], key = str.lower, reverse = True))

L = [('Bob', 75), ('Adam', 92), ('Bart', 66), ('Lisa', 88)]
def by_name(x):
    return x[0]
print(sorted(L, key=by_name))
print(sorted(L, key=lambda t:t[0]))

def by_score(x):
    return x[1]
print(sorted(L, key=by_score, reverse=True))
print(sorted(L, key=lambda t:t[1], reverse=True))

def add_sum(L):
    x = 0
    for t in L:
        x = x + t
    return x

def lazy_sum(*L):
    def add_sum():
        x = 0
        for t in L:
            x = x + t
        return x
    return add_sum
f = lazy_sum(1,2,3,4,5)
print(f)
print(f())

# 返回函数不要引用任何循环变量，或者后续会发生变化的变量。
# 关键字lambda表示匿名函数，冒号前面的x表示函数参数。匿名函数有个限制，就是只能有一个表达式，不用写return，返回值就是该表达式的结果。
print(list(map(lambda x:x * x, [1,2,3])))

# 函数对象有一个__name__属性，可以拿到函数的名字
print(f.__name__)

# 装饰器
def log(func):
    def wrapper(*args, **keywords):
        print('call %s' % func.__name__)
        return func(*args, **keywords)
    return wrapper

@log
def now():
    print('2017-11-03')

now()

def newlog(func):
    @functools.wraps(func)
    def wrapper(*args, **keywords):
        print('begin call')
        f = func(*args, **keywords)
        print('end call')
        return f
    return wrapper()

@newlog
def f():
    print('call f')

def nnlog(*text):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **keywords):
            print('%s %s:' %(text, func.__name__))
            return func(*args, **keywords)
        return wrapper
    return decorator

@nnlog()
def f():
    print('aaa')

f()

@nnlog('execute')
def f():
    print('bbb')

f()

# 偏函数：把字符串转换成数字，默认按照十进制转换,base参数指定为某进制转换
print(int('1234'))
print(int('456', base=8))

# 假设要转换二进制字符串，functools.partial的作用就是把一个函数的某些参数给固定住（也就是设置默认值），
# 返回一个新的函数，调用这个新函数会更简单。
int2 = functools.partial(int, base = 2)
print(int2('1011'))

# 类似_xxx和__xxx这样的函数或变量就是非公开的（private），不应该被直接引用，比如_abc，__abc等
def _private_1(name):
    print('Hello,',name)

def _private_2(name):
    print('Hi,',name)

def greeting(name):
    if len(name) > 2:
        return _private_1(name)
    else:
        return _private_2(name)

greeting('LiuDi')
greeting('HT')

im = Image.open('/Users/luo/Downloads/切片补充/icon_xs_rmb@2x.png')
print(im.format, im.size, im.mode)
im.thumbnail((20,20))
im.save('thumbnail.png', 'PNG')

print(sys.path)
sys.path.append('/Users/luo/Desktop')
print(sys.path)

# 定义一个类，继承自object类，拥有name和gender两个属性以及一个描述方法
# 在Python中，变量名类似__xxx__的，也就是以双下划线开头，并且以双下划线结尾的，是特殊变量，特殊变量是可以直接访问的，不是private变量
class Person(object):
    def __init__(self, name, gender):
        self.__name = name
        self.__gender = gender

    def get_name(self):
        return self.__name
    def set_name(self, name):
        self.__name = name

    def get_gender(self):
        return self.__gender
    def set_gender(self, gender):
        self.__gender = gender

    def description(self):
        print('My name is %s,i am a %s' %(self.__name, self.__gender))

p1 = Person('Hem1ng', 'boy')
p2 = Person('Rebeica', 'girl')
p1.description()
p2.description()
p1.get_name()
p2.set_name('LD')
p1.set_gender('girl')
p2.get_gender()
p1.description()
p2.description()

# 能用type()判断的基本类型也可以用isinstance()判断，对于class的继承关系来说，使用type()就很不方便。
# 我们要判断class的类型，可以使用isinstance()函数
print(type(p1))
# 如果要获得一个对象的所有属性和方法，可以使用dir()函数，它返回一个包含字符串的list
print(dir(p1))

if hasattr(p1, '__name'):
    print('YES')
else:
    print('NO')

setattr(p1, 'age', 18)
if hasattr(p1, 'age'):
    print(getattr(p1,'age'))
print(getattr(p1,'Z', '404 not found'))

class Student():
    pass

s = Student()
s.age = 18
print(s.age)

def set_name(self, name):
    self.name = name

s.set_name = MethodType(set_name, s)
s.set_name('Hem1ng')
print(s.name)

def set_score(self, score):
    self.score = score

Student.set_score = set_score
s.set_score(98)
print(s.score)

# 为了达到限制的目的，Python允许在定义class的时候，定义一个特殊的__slots__变量，
# 来限制该class实例能添加的属性,用tuple定义允许绑定的属性名称
# 使用__slots__要注意，__slots__定义的属性仅对当前类实例起作用，对继承的子类是不起作用的,
# 除非在子类中也定义__slots__，这样，子类实例允许定义的属性就是自身的__slots__加上父类的__slots__
class SHStudent():
    # __slots__ = ('name', 'age')

    # @property装饰器就是负责把一个方法变成属性调用
    @property
    def gender(self):
        return self._gender
    @gender.setter
    def gender(self, value):
        self._gender = value

    # 只定义getter方法，不定义setter方法就是一个只读属性
    @property
    def city(self):
        self._city = 'sh'
        return self._city

shs = SHStudent()
shs.name = 'LD'
shs.age = 25

shs.gender = 'male'
print(shs.gender)
print(shs.city)

class Screen(object):

    @property
    def width(self):
        return self._width
    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        return self._height
    @height.setter
    def height(self, value):
        self._height = value

    @property
    def resolution(self):
        self._resolution = self._height * self._width
        return self._resolution

sc = Screen()
sc.height = 768
sc.width = 1024
print('Area is',sc.resolution)
assert sc.resolution == 786432, '1024 * 768 = %d ?' % s.resolution

class RunnableMixIn(object):
    def run(self):
        print('Running...')

class FlyableMixIn(object):
    def fly(self):
        print('Flying...')

class CarnivorousMixIn(object):
    def desc(self):
        print('I\'m Carnivorous')

class HerbivoresMixIn(object):
    def desc(self):
        print('I\'m Herbivores')

class Animal(object):
    pass

class Mammal(Animal):
    pass

class Bird(Animal):
    pass

# 通过多重继承，一个子类就可以同时获得多个父类的所有功能。
class Dog(Mammal, RunnableMixIn, CarnivorousMixIn):
    pass

class Bat(Mammal):
    pass

# MixIn的目的就是给一个类增加多个功能，这样，在设计类的时候，我们优先考虑通过多重继承来组合多个MixIn的功能，而不是设计多层次的复杂的继承关系。
class Parrot(Bird, FlyableMixIn, HerbivoresMixIn):
    pass

class Ostrich(Bird):
    pass

d = Dog()
d.run()
d.desc()

p = Parrot()
p.fly()
p.desc()

class CNPerson(object):
    def __init__(self,name):
        self.name = name

    def __str__(self):
        return 'Person name is %s' % self.name
    __repr__ = __str__

cnp = CNPerson('hem1ng')
print(cnp)

# 如果一个类想被用于for ... in循环，类似list或tuple那样，就必须实现一个__iter__()方法，该方法返回一个迭代对象，
# 然后，Python的for循环就会不断调用该迭代对象的__next__()方法拿到循环的下一个值，直到遇到StopIteration错误时退出循环
class Myfib(object):
    def __init__(self):
        self.a, self.b = 0, 1

    def __iter__(self):
        return self

    def __next__(self):
        self.a, self.b = self.b, self.a + self.b
        if self.a > 100:
            raise StopIteration
        return self.a

f = Myfib()
for n in f:
    print(n)

class Fib(object):
    # 像list那样按照下标取出元素，需要实现__getitem__()方法
    def __getitem__(self, n):
        a, b = 1, 1
        for x in range(n):
            a, b = b, a + b
        return a

f = Fib()
print(f[1])
print(f[3])

class NewFib(object):

    def __getitem__(self, n):
        if isinstance(n, int):
            a, b = 1, 1
            for x in range(n):
                a, b = b, a + b
            return a

        if isinstance(n, slice):
            start = n.start
            stop = n.stop
            if start is None:
                start = 0
            a, b = 1, 1
            L = []
            for x in range(stop):
                if x >= start:
                    L.append(a)
                a, b = b, a + b
            return L

f = NewFib()
print(f[:5])

class Company(object):

    def __init__(self, name):
        self.name = name

    def __getattr__(self, item):
        if item == 'score':
            return 99
        elif item == 'age':
            return lambda: 25

c = Company('Vcredit')
print(c.name)
print(c.score)
print(c.age())

class Chain(object):

    def __init__(self, path = ''):
        self._path = path

    def __getattr__(self, path):
        return Chain('%s/%s' % (self._path, path))

    def user(self, name):
        return Chain('/user/%s' % name)

    def __str__(self):
        return self._path

    __repr = __str__

print(Chain().status.find.list)
print(Chain().user('Heming').repo)

class People(object):

    def __init__(self, name):
        self._name = name

    def __call__(self):
        print('My name is',self._name)

p = People('Tai')
p()

# callable(o)判断一个对象是否能被调用
print(callable(p))

# 枚举 value属性是自动赋给成员的int常量，默认从1开始计数
Month = Enum('Month', ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))
for name, member in Month.__members__.items():
    print(name, '=>', member, ',', member.value)

# @unique 装饰器可以帮助我们检查保证没有重复值。
@unique
class Weekday(Enum):
    Sun = 0
    Mon = 1
    Tue = 2
    Wed = 3
    Thu = 4
    Fri = 5
    Sat = 6

# 访问枚举值的方式：既可以用成员名称引用枚举常量，又可以直接根据value的值获得枚举常量。
print(Weekday.Mon)
print(Weekday['Thu'])
print(Weekday.Tue.value)
print(Weekday(3))

for name, member in Weekday.__members__.items():
    print(name, '=>', member, member.value)

# 要创建一个class对象，type()函数依次传入3个参数：
# class的名称；
# 继承的父类集合，注意Python支持多重继承，如果只有一个父类，别忘了tuple的单元素写法；
# class的方法名称与函数绑定，这里我们把函数fn绑定到方法名hello上
def fn(self, name='world'):
    print('hello %s' % name)

Hello = type('Hello', (object,), dict(hello=fn))
h = Hello()
h.hello()
print(type(Hello))
print(type(h))

class ListMetaClass(type):
    def __new__(cls, name, bases, attrs):
        attrs['add'] = lambda self, value: self.append(value)
        return type.__new__(cls, name, bases, attrs)
class MyList(list, metaclass=ListMetaClass):
    pass
ml = MyList()
ml.add(1)
print(ml)

class Field(object):
    def __init__(self, name, column_type):
        self.name = name
        self.column_type = column_type

    def __str__(self):
        return '<%s:%s>' % (self.__class__.__name__, self.name)

class StringField(Field):
    def __init__(self, name):
        super(StringField, self).__init__(name, 'varchar(100)')

class IntegerField(Field):
    def __init__(self, name):
        super(IntegerField, self).__init__(name, 'bigint')

class ModelMetaClass(type):

    def __new__(cls, name, bases, attrs):
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)
        print('Found model %s' % name)
        mappings = dict()
        for k, v in attrs.items():
            if isinstance(v, Field):
                print('Found mapping %s ==> %s' %(k, v))
                mappings[k] = v
        for k in mappings.keys():
            attrs.pop(k)
        attrs['__mappings__'] = mappings
        attrs['__table__'] = name
        return type.__new__(cls, name, bases, attrs)

class Model(dict, metaclass=ModelMetaClass):
    def __init__(self, **kw):
        super(Model, self).__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

    def save(self):
        fields = []
        params = []
        args =[]
        for k, v in self.__mappings__.items():
            fields.append(v.name)
            params.append('?')
            args.append(getattr(self, k, None))
        sql = 'insert into %s (%s) values (%s)' % (self.__table__, ','.join(fields), ','.join(params))
        print('SQL: %s' % sql)
        print('ARGS: %s' % str(args))

class User(Model):
    id = IntegerField('id')
    name = StringField('username')
    email = StringField('email')
    password = StringField('password')

u = User(id=12345, name='Michael', email='test@orm.org', password='my-pwd')
u.save()

# try except(可以有多个except语句) finally(可以没有finally语句)捕获异常,
# 可以在except语句块后面加一个else，当没有错误发生时，会自动执行else语句
# Python的错误其实也是class，所有的错误类型都继承自BaseException，所以在使用except时需要注意的是，
# 它不但捕获该类型的错误，还把其子类也“一网打尽”。比如：
# try:
#     foo()
# except ValueError as e:
#     print('ValueError')
# except UnicodeError as e:
#     print('UnicodeError')
# 第二个except永远也捕获不到UnicodeError，因为UnicodeError是ValueError的子类，如果有，也被第一个except给捕获了。
try:
    print('try...')
    r = 10 / int('a')
    print('result =',r)
except ValueError as  e:
    print('except:',e)
except ZeroDivisionError as  e:
    print('except:',e)
else:
    print('no error')
finally:
    print('finally')
print('END')

# 使用try...except捕获错误还有一个巨大的好处，就是可以跨越多层调用，
# 比如函数main()调用foo()，foo()调用bar()，结果bar()出错了，这时，只要main()捕获到了，就可以处理

def foo(s):
    return 10 / int(s)

def bar(s):
    return foo(s) * 2

def main():
    try:
        bar('0')
    except Exception as e:
        # print('except:', e)
        logging.exception(e)
    finally:
        print('finally')
# main()
print('end')

class FooError(ValueError):
    pass

def foo(s):
    n = int(s)
    if n == 0:
        raise FooError('invalid value: %s' % s)
    return 10 / n

def bar():
    try:
        foo('0')
    except ValueError as e:
        print('ValueError')
        # raise语句如果不带参数，就会把当前错误原样抛出
        raise

# foo('0')
# bar()

def foo1(s):
    n = int(s)
    assert n != 0, 'n is zero!'
    return 10 / n

def main1():
    foo1('1')
# main1()

s = '0'
n = int(s)
logging.info('n = %d' % n)
# print(10 / n)

m = re.search('(?<=abc)def','abcdef')
print(m.group(0))

# 读文件调用open()函数，传入参数：文件路径，读写方式(r,rb,w,wb),rb,wb表示读或写二进制文件
# 由于文件读写时都有可能产生IOError，一旦出错，后面的f.close()就不会调用。
# 所以，为了保证无论是否出错都能正确地关闭文件，我们可以使用try ... finally来实现
try:
    f = open('/Users/luo/Desktop/cal.py','r')
    print(f.read())
except IOError as e:
    print(e)
finally:
    if f:
        f.close()

# Python引入了with语句来自动帮我们调用close()方法
# 调用read()会一次性读取文件的全部内容，如果文件有10G，内存就爆了，
# 所以，要保险起见，可以反复调用read(size)方法，每次最多读取size个字节的内容。
# 另外，调用readline()可以每次读取一行内容，调用readlines()一次读取所有内容并按行返回list。因此，要根据需要决定怎么调用。
with open('/Users/luo/Desktop/cal.py','r') as f:
    f.read()

# for line in f.readlines():
#     print(line.strip())

e = open('/Users/luo/Desktop/PythonRepo/thumbnail.png','rb')
print(e.read())

# 要读取非UTF-8编码的文本文件，需要给open()函数传入encoding参数
f = open('/Users/luo/Desktop/test.py', 'w')
f.write('hello,world')
f.close()

with open('/Users/luo/Desktop/test.py', 'w') as f:
    f.write('hahahahahhha')

f = StringIO()
f.write('hello')
f.write(',')
f.write('world!')
# getvalue()方法用于获得写入后的str
print(f.getvalue())

f = StringIO('Hello\nHem1ng')
for n in f.readlines():
    print(n.strip())

f = BytesIO()
f.write('中文'.encode('utf-8'))
print(f.getvalue())

e = BytesIO(b'\xe4\xb8\xad\xe6\x96\x87')
print(e.read())

# pickle.dumps()方法把任意对象序列化成一个bytes，然后，就可以把这个bytes写入文件。
# 或者用另一个方法pickle.dump()直接把对象序列化后写入一个file-like Object
d = dict(name = 'bob', age = 25, score = 90)
c = pickle.dumps(d)
print(c)
f = open('dump.txt','wb')
pickle.dump(d, f)
f.close()

# 当我们要把对象从磁盘读到内存时，可以先把内容读到一个bytes，然后用pickle.loads()方法反序列化出对象，
# 也可以直接用pickle.load()方法从一个file-like Object中直接反序列化出对象
f = open('dump.txt', 'rb')
b = pickle.load(f)
f.close()
print(b)

# dumps()方法返回一个str，内容就是标准的JSON
print(json.dumps(d))

# 用loads()或者对应的load()方法，从file-like Object中读取字符串并反序列化：
j = '{"name": "bob", "age": 25, "score": 90}'
g = json.loads(j)
print(g)

class Student(object):
    def __init__(self, name, age, score):
        self.name = name
        self.age = age
        self.score = score

def student2dict(std):
    return {
        'name' : std.name,
        'age' : std.age,
        'score' : std.score
    }

def dict2student(d):
    return Student(d['name'],d['age'],d['score'])


# 可选参数default就是把任意一个对象变成一个可序列为JSON的对象，我们只需要为Student专门写一个转换函数，再把函数传进去即可
s = Student('heming',25,88)
print(json.dumps(s, default=student2dict))
print(json.dumps(s,default=lambda obj:obj.__dict__))

# 如果我们要把JSON反序列化为一个Student对象实例，loads()方法首先转换出一个dict对象，然后，我们传入的object_hook函数负责把dict转换为Student实例
j_str = '{"name": "bob", "age": 25, "score": 90}'
s = json.loads(j_str,object_hook=dict2student)
print(s)

# print('Process (%s) start...' % os.getpid())
# pid = os.fork()
# if pid == 0:
#     print('I am child process (%s) and my parent is (%s)' % (os.getpid(), os.getppid()))
# else:
#     print('I (%s) just creted a child process (%s)' % (os.getpid(), pid))

def run_proc(name):
    print('Run child process %s (%s)...' % (name, os.getpid()))
if __name__ == '__main__':
    print('Parent process %s.' % os.getpid())
    # 创建子进程时，只需要传入一个执行函数和函数的参数，创建一个Process实例，用start()方法启动，这样创建进程比fork()还要简单。
    # join()方法可以等待子进程结束后再继续往下运行，通常用于进程间的同步。
    p = Process(target=run_proc, args=('test',))
    print('Child process will start')
    p.start()
    p.join()
    print('Child process end')

def long_time_task(name):
    print('Run task %s (%s)...' % (name, os.getpid()))
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print('Task %s runs %0.2f seconds.' % (name, (end-start)))

# 对Pool对象调用join()方法会等待所有子进程执行完毕，调用join()之前必须先调用close()，调用close()之后就不能继续添加新的Process了
if __name__ == '__main__':
    print('Parent process %s.' % os.getpid())
    p = Pool(4)
    # 由于Pool的默认大小是CPU的核数，如果你不幸拥有8核CPU，你要提交至少9个子进程才能看到上面的等待效果
    for i in range(5):
        p.apply_async(long_time_task, args=(i,))
    print('Waiting for all subprocess done...')
    p.close()
    p.join()
    print('All subprocess done.')

print('$ nslookup www.python.org')
r = subprocess.call(['nslookup', 'www.python.org'])
print('Exit code:' ,r)

print('$ nslookup')
p = subprocess.Popen(['nslookup'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, err = p.communicate(b'set q=mx\npython.org\nexit\n')
print(output.decode('utf-8'))
print('Exit code:', p.returncode)

# 写数据进程
def write(q):
    print('Process to write: %s' % os.getpid())
    for value in ['A','B','C']:
        print('Put %s to queue...' % value)
        q.put(value)
        time.sleep(random.random())

# 读数据进程
def read(q):
    print('Process to read: %s' % os.getpid())
    while True:
        value = q.get(True)
        print('Get %s from queue,' % value)

if __name__ == '__main__':
    # 父进程创建Queue，并传给各个子进程
    q = Queue()
    pw = Process(target=write, args=(q,))
    pr = Process(target=read, args=(q,))
    # 启动子进程pw，写入
    pw.start()
    # 启动子进程pr，读取
    pr.start()
    # 等待pw结束
    pw.join()
    # pr进程里是死循环，无法等待其结束，只能强行终止
    pr.terminate()

def loop():
    print('thread %s is running' % threading.current_thread().name)
    n = 0
    while n < 5:
        n = n + 1
        print('thread %s >>> %s' % (threading.current_thread().name, n))
        time.sleep(1)
    print('thread %s ended.' % threading.current_thread().name)

print('thread %s is running' % threading.current_thread().name)
t = threading.Thread(target=loop, name='LoopThread')
t.start()
t.join()
print('thread %s ended' % threading.current_thread().name)

# 当多个线程同时执行lock.acquire()时，只有一个线程能成功地获取锁，然后继续执行代码，其他线程就继续等待直到获得锁为止
balance = 0
lock = threading.Lock()
def change_it(n):
    global balance
    balance = balance + n
    balance = balance - n
def run_thread(n):
    for i in range(10):
        # 先获取锁
        lock.acquire()
        try:
            change_it(n)
        finally:
            lock.release()

t1 = threading.Thread(target=run_thread, args=(5,))
t2 = threading.Thread(target=run_thread, args=(8,))
t1.start()
t2.start()
t1.join()
t2.join()
print(balance)

# 创建全局ThreadLocal对象
# 一个ThreadLocal变量虽然是全局变量，但每个线程都只能读写自己线程的独立副本，互不干扰。ThreadLocal解决了参数在一个线程中各个函数之间互相传递的问题。
local_name = threading.local()
def process_name():
    std = local_name.name
    print('Hello, %s (in %s)' % (std, threading.current_thread().name))

def process_thread(name):
    local_name.name = name
    process_name()

t1 = threading.Thread(target=process_thread, args=('Alice',), name='Thread-A')
t2 = threading.Thread(target=process_thread, args=('Bob',), name='Thread-B')
t1.start()
t2.start()
t1.join()
t2.join()
print('ended')

# r表示字符串不转义
print(re.match(r'^\d{3}\-\d{3,8}$','010-12345'))
print(re.match(r'^\d{3}\-\d{3,8}$','010 12345'))

# ^py$是只能匹配'py'
text = input('please input text here:')
if re.match(r'^py$',text):
    print('match')
else:
    print('not match')

print('a b   c'.split(' '))
print(re.split(r'\s+','a b   c'))
print(re.split(r'[\s\,]+','a,b,   c,d'))

# 用()表示的就是要提取的分组（Group）
# 如果正则表达式中定义了组，就可以在Match对象上用group()方法提取出子串来。
# 注意到group(0)永远是原始字符串，group(1)、group(2)……表示第1、2、……个子串。
m = re.match(r'(\d{3})-(\d{3,8})$','010-12345678')
print(m)
print(m.group(0))
print(m.group(1))
print(m.group(2))

t = '19:20:30'
m = re.match(r'^([0-1][0-9]|2[0-3])\:([0-5][0-9])\:([0-5][0-9])$',t)
print(m)
print(m.groups())

# 正则匹配默认是贪婪匹配，也就是匹配尽可能多的字符
# 由于\d+采用贪婪匹配，直接把后面的0全部匹配了，结果0*只能匹配空字符串了。
# 必须让\d+采用非贪婪匹配（也就是尽可能少匹配），才能把后面的0匹配出来，加个?就可以让\d+采用非贪婪匹配
print(re.match(r'(\d+)(0*)$','1023000').groups())
print(re.match(r'(\d+?)(0*)$','1023000').groups())
print(re.match(r'(\d+?)(0*)$','123000').groups())
print(re.match(r'(\d+?)(0*)$','10023000').groups())
# 预编译
re_tel = re.compile(r'^(\d{3})-(\d{3,8})$')
print(re_tel.match('021-51203345').groups())

re_mail = re.compile(r'^([0-9a-zA-Z\.\_]+)@([0-9a-zA-Z]+)\.(\w{3})$')
print(re_mail.match('someone@gmail.com'))
print(re_mail.match('bill.gates@microsoft.com'))

re_name_mail = re.compile(r'^\<([\w\s]+)\>\s+([a-zA-Z._]+)@(\W+)\.(\w{3})$')
print(re_name_mail.match('<Tom paris> tom@voyager.com'))





