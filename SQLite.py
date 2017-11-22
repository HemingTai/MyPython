import sqlite3, os
import mysql.connector

from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base


# 连接到SQLite数据库，数据库文件是test.db，如果文件不存在，会自动在当前目录创建
# conn = sqlite3.connect('test.db')
# 创建一个Cursor
# cursor = conn.cursor()
# 执行一条SQL语句，创建user表
# cursor.execute('create table user (id varchar(20) primary key, name varchar(20))')
# 继续执行一条SQL语句，插入一条记录
# cursor.execute('insert into user (id, name) values (\'1\',\'heming\')')
# 通过rowcount获得插入的行数
# print(cursor.rowcount)
# 查询记录
# 使用Python的DB-API时，只要搞清楚Connection和Cursor对象，打开后一定记得关闭，就可以放心地使用。
# 使用Cursor对象执行insert，update，delete语句时，执行结果由rowcount返回影响的行数，就可以拿到执行结果。
# 使用Cursor对象执行select语句时，通过featchall()可以拿到结果集。结果集是一个list，每个元素都是一个tuple，对应一行记录。
# 如果SQL语句带有参数，那么需要把参数按照位置传递给execute()方法，有几个?占位符就必须对应几个参数
# cursor.execute('SELECT * FROM user WHERE id=?',('1',))
# values = cursor.fetchall()
# print(values)
# 关闭Cursor
# cursor.close()
# 提交事务
# conn.commit()
# 关闭Connection
# conn.close()

# db_file = os.path.join(os.path.dirname(__file__), 'test.db')
# if os.path.isfile(db_file):
#     os.remove(db_file)
#
# con = sqlite3.connect(db_file)
# cur = con.cursor()
# cur.execute('create table user (id varchar(20) primary key, name varchar(20), score int)')
# cur.execute('insert into user values (\'A-001\', \'Adam\', 95)')
# cur.execute('insert into user values (\'A-002\', \'Bart\', 62)')
# cur.execute('insert into user values (\'A-003\', \'Lisa\', 78)')
# cur.close()
# con.commit()
# con.close()
#
# def get_score_in(low, high):
#     con = sqlite3.connect('test.db')
#     cur = con.cursor()
#     cur.execute('select name from user where score BETWEEN ? AND ? ORDER BY score ASC ', (low, high))
#     values = cur.fetchall()
#     result = list(map(lambda x:x[0], values))
#     print(result)
#     cur.close()
#     con.commit()
#     con.close()
#
# get_score_in(60,100)


# conn = mysql.connector.connect(user='root',password='99112911',database='Test')
# cur = conn.cursor()
# cur.execute('create table user (id varchar(20) primary key, name varchar(20))')
# 执行INSERT等操作后要调用commit()提交事务；
# MySQL的SQL占位符是%s
# cur.execute('insert into user (id, name) values (%s, %s)', ['1', 'Michael'])
# print(cur.rowcount)
# conn.commit()
# cur.execute('select * from user where id = %s',('1',))
# value = cur.fetchall()
# print(value)
# cur.close()
# conn.close()

# 创建对象基类
Base = declarative_base()

class User(Base):
    # 表的名字
    __tablename__ = 'user'
    # 表结构
    id = Column(String(20), primary_key=True)
    name = Column(String(20))
    # 一对多
    # 由于关系数据库的多个表还可以用外键实现一对多、多对多等关联，相应地，ORM框架也可以提供两个对象之间的一对多、多对多等功能。
    # 例如，如果一个User拥有多个Book，就可以定义一对多关系如下
    books = relationship('Book')

class Book(Base):
    __tableName__ = 'book'

    id = Column(String(20), primary_key=True)
    name = Column(String(20))
    # “多”的一方的book表是通过外键关联到user表的:
    user_id = Column(String(20),ForeignKey=('User.id'))

# 初始化数据连接
# create_engine()用来初始化数据库连接。SQLAlchemy用一个字符串表示连接信息：'数据库类型+数据库驱动名称://用户名:口令@机器地址:端口号/数据库名'
# 你只需要根据需要替换掉用户名、口令等信息即可
engine = create_engine('mysql+mysqlconnector://root:99112911@localhost:3306/Test')
# 创建DBSession
DBSession = sessionmaker(bind=engine)
# 创建session对象
session = DBSession()
new_user = User(id='2', name='hem1ng')
session.add(new_user)
# 提交即保存到数据库
session.commit()
# 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行
user = session.query(User).filter(User.id=='2').one()
print(type(user))
print(user.name)
session.close()
# 可见，关键是获取session，然后把对象添加到session，最后提交并关闭。DBSession对象可视为当前数据库连接
