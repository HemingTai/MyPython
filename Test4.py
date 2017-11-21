import chardet, psutil

# 当我们拿到一个bytes时，就可以对其检测编码
# 检测出的编码是ascii，注意到还有个confidence字段，表示检测的概率是1.0（即100%）
print(chardet.detect(b'hello,world'))
# 检测的编码是GB2312，注意到GBK是GB2312的超集，两者是同一种编码，检测正确的概率是74%，language字段指出的语言是'Chinese'
data = '离离原上草，一岁一枯荣'.encode('gbk')
print(chardet.detect(data))
# 检测编码 utf-8
data = '离离原上草，一岁一枯荣'.encode('utf-8')
print(chardet.detect(data))
# 检测日文
data = '最新の主要ニュース'.encode('euc-jp')
print(chardet.detect(data))

# ************************ 获取系统信息 *************************

# CPU逻辑数量
print(psutil.cpu_count())
# CPU物理核心，2说明是双核超线程, 4则是4核非超线程
print(psutil.cpu_count(logical=False))
# 统计CPU的用户/系统/空闲时间
print(psutil.cpu_times())
# CPU使用率，每秒刷新一次，累计10次
# for x in range(10):
#     print(psutil.cpu_percent(interval=1, percpu=True))
# 获取内存信息和交换内存信息，返回的是字节为单位的整数
print(psutil.virtual_memory())
print(psutil.swap_memory())
# 获取磁盘分区信息，磁盘使用和磁盘IO信息，opts中包含rw表示可读写，journaled表示支持日志
print(psutil.disk_partitions())
print(psutil.disk_usage('/'))
print(psutil.disk_io_counters())
# 获取网络信息:获取网络读写字节／包的个数, 获取网络接口信息, 获取网络接口状态
print(psutil.net_io_counters())
print(psutil.net_if_addrs())
print(psutil.net_if_stats())
# 获取当前网络连接信息
# print(psutil.net_connections())
# 获取进程信息
print(psutil.pids()) # 所有进程ID
p = psutil.Process(10537) # 获取指定进程ID=10537
print(p.name()) # 进程名称
print(p.exe()) # 进程exe路径
# print(p.cwd()) # 进程工作目录
# print(p.cmdline()) # 进程启动的命令行
print(p.ppid) # 父进程ID
print(p.parent()) # 父进程
print(p.children()) # 子进程列表
print(p.status()) # 进程状态
print(p.username()) # 进程用户名
print(p.create_time()) # 进程创建时间
# print(p.terminate()) # 进程终端
# print(p.cpu_times()) # 进程使用的CPU时间
# print(p.memory_info()) # 进程使用的内存
# print(p.open_files()) # 进程打开的文件
# print(p.connections()) # 进程相关网络连接
# print(p.num_threads()) # 进程的线程数量
# print(p.threads()) # 所有线程信息
# print(p.environ()) # 进程环境变量
# print(p.terminal()) # 结束进程
# psutil还提供了一个test()函数，可以模拟出ps命令的效果
# psutil.test()

# ************************ virtualenv ***************************

# virtualenv就是用来为一个应用创建一套“隔离”的Python运行环境。
# 首先，我们用pip安装virtualenv：
# $ pip3 install virtualenv
# 然后，假定我们要开发一个新的项目，需要一套独立的Python运行环境，可以这么做：
#
# 第一步，创建目录：
# Mac:~ michael$ mkdir myproject
# Mac:~ michael$ cd myproject/
# Mac:myproject michael$
#
# 第二步，创建一个独立的Python运行环境，命名为venv：
# Mac:myproject michael$ virtualenv --no-site-packages venv
# Using base prefix '/usr/local/.../Python.framework/Versions/3.4'
# New python executable in venv/bin/python3.4
# Also creating executable in venv/bin/python
# Installing setuptools, pip, wheel...done.
# 命令virtualenv就可以创建一个独立的Python运行环境，我们还加上了参数--no-site-packages，
# 这样，已经安装到系统Python环境中的所有第三方包都不会复制过来，这样，我们就得到了一个不带任何第三方包的“干净”的Python运行环境。
# 新建的Python环境被放到当前目录下的venv目录。有了venv这个Python环境，可以用source进入该环境：
# Mac:myproject michael$ source venv/bin/activate
# (venv)Mac:myproject michael$
# 注意到命令提示符变了，有个(venv)前缀，表示当前环境是一个名为venv的Python环境。
# 下面正常安装各种第三方包，并运行python命令：
# (venv)Mac:myproject michael$ pip install jinja2
# ...
# Successfully installed jinja2-2.7.3 markupsafe-0.23
# (venv)Mac:myproject michael$ python myapp.py
# ...
# 在venv环境下，用pip安装的包都被安装到venv这个环境下，系统Python环境不受任何影响。也就是说，venv环境是专门针对myproject这个应用创建的。
# 退出当前的venv环境，使用deactivate命令：
# (venv)Mac:myproject michael$ deactivate
# Mac:myproject michael$
# 此时就回到了正常的环境，现在pip或python均是在系统Python环境下执行。
# 完全可以针对每个应用创建独立的Python运行环境，这样就可以对每个应用的Python环境进行隔离。
# virtualenv是如何创建“独立”的Python运行环境的呢？原理很简单，就是把系统Python复制一份到virtualenv的环境，
# 用命令source venv/bin/activate进入一个virtualenv环境时，virtualenv会修改相关环境变量，让命令python和pip均指向当前的virtualenv环境。