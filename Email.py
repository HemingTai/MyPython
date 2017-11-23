# <----------------------- SMTP ------------------------>
from email import encoders
from email.header import Header, decode_header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.utils import parseaddr, formataddr
from email.parser import Parser
import smtplib, poplib

# Python对SMTP支持有smtplib和email两个模块，email负责构造邮件，smtplib负责发送邮件
# 注意到构造MIMEText对象时，第一个参数就是邮件正文，第二个参数是MIME的subtype，传入'plain'表示纯文本，
# 最终的MIME就是'text/plain'，最后一定要用utf-8编码保证多语言兼容性
# msg = MIMEText('hello, send by Hem1ngTai with Python.', 'plain', 'utf-8')
# 输入发件地址和密码
# from_addr = input('From：')
# password = input('Password：')
# 输入收件地址和SMTP服务器地址
# to_addr = input('To：')
# smtp_sever = input('SMTP sever：')

# SMTP协议默认端口是25
# 我们用set_debuglevel(1)就可以打印出和SMTP服务器交互的所有信息。
# SMTP协议就是简单的文本命令和响应。
# login()方法用来登录SMTP服务器，
# sendmail()方法就是发邮件，由于可以一次发给多个人，所以传入一个list，
# 邮件正文是一个str，as_string()把MIMEText对象变成str
# sever = smtplib.SMTP(smtp_sever, 25)
# sever.set_debuglevel(1)
# sever.login(from_addr, password)
# sever.sendmail(from_addr, [to_addr], msg.as_string())
# sever.quit()


# 仔细观察，发现如下问题：
# 邮件没有主题；
# 收件人的名字没有显示为友好的名字，比如Mr Green <green@example.com>；
# 明明收到了邮件，却提示不在收件人中。
# 这是因为邮件主题、如何显示发件人、收件人等信息并不是通过SMTP协议发给MTA，而是包含在发给MTA的文本中的，
# 所以，我们必须把From、To和Subject添加到MIMEText中，才是一封完整的邮件
def _format_attr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

# 输入发件地址和密码
# from_addr = input('From：')
# password = input('Password：')
# 输入收件店址和SMTP服务器地址
# to_addr = input('To：')
# smtp_sever = input('SMTP sever：')

# 函数_format_addr()来格式化一个邮件地址。注意不能简单地传入name <addr@example.com>，
# 因为如果包含中文，需要通过Header对象进行编码。
# msg['To']接收的是字符串而不是list，如果有多个邮件地址，用,分隔即可
# msg = MIMEText('hello, again!.', 'plain', 'utf-8')
# 带附件的邮件可以看做包含若干部分的邮件：文本和各个附件本身，
# 所以，可以构造一个MIMEMultipart对象代表邮件本身，然后往里面加上一个MIMEText作为邮件正文，再继续往里面加上表示附件的MIMEBase对象即可
# 同时支持HTML和Plain格式，利用MIMEMultipart就可以组合一个HTML和Plain，要注意指定subtype是alternative
msg = MIMEMultipart('alternative')
# 要把图片嵌入到邮件正文中，我们只需按照发送附件的方式，先把邮件作为附件添加进去，然后，在HTML中通过引用src="cid:0"就可以把附件作为图片嵌入了。
# 如果有多个图片，给它们依次编号，然后引用不同的cid:x即可
msg.attach(MIMEText('<html><body><h1>Hello</h1>' +
    '<p>send by <a href="http://www.baidu.com">Baidu</a>...</p>' +
    '<p><img src="cid:0"></p>' +
    '</body></html>', 'html', 'utf-8'))
# 添加附件就是加上一个MIMEBase，从本地读取一个图片
with open('verify.jpg', 'rb') as f:
    # 设置附件的MIME和文件名，这里是png类型
    mime = MIMEBase('image', 'png', filename='verify.png')
    # 加上必要的头信息
    mime.add_header('Content-Disposition', 'attachment', filename='verify.png')
    mime.add_header('Content-ID', '<0>')
    mime.add_header('X-Attachment-Id', '0')
    # 把附件的内容读进来
    mime.set_payload(f.read())
    # 用Base64编码
    encoders.encode_base64(mime)
    # 添加到MIMEMultipart
    msg.attach(mime)
# msg['From'] = _format_attr('Hem1ngTai<%s>' % from_addr)
# msg['To'] = _format_attr('Chen1t<%s>' % to_addr)
# msg['Subject'] = Header('This is a test email sending by python', 'utf-8').encode()
# 使用标准的25端口连接SMTP服务器时，使用的是明文传输，发送邮件的整个过程可能会被窃听。
# 要更安全地发送邮件，可以加密SMTP会话，实际上就是先创建SSL安全连接，然后再使用SMTP协议发送邮件
# sever = smtplib.SMTP(smtp_sever, 587)
# 只需要在创建SMTP对象后，立刻调用starttls()方法，就创建了安全连接
# sever.starttls()
# sever.set_debuglevel(1)
# sever.login(from_addr, password)
# sever.sendmail(from_addr, [to_addr], msg.as_string())
# sever.quit()


# <----------------------- POP3 ------------------------>

email = input('Email：')
password = input('Password：')
pop3_server = input('POP3 server： ')

server = poplib.POP3_SSL(pop3_server, port='995')
server.user(email)
server.pass_(password)
server.set_debuglevel(1)
# 可选:打印POP3服务器的欢迎文字
print(server.getwelcome().decode('utf-8'))
# stat()返回邮件数量和占用空间
print('Message:%s Size:%s' % server.stat())
# list()返回所有邮件的编号
resp, mails, octets = server.list()
# 可以查看返回的列表类似[b'1 82923', b'2 2184', ...]
print(mails)
# 获取最新一封邮件, 注意索引号从1开始
index = len(mails)
resp, lines, octets = server.retr(index)
# lines存储了邮件的原始文本的每一行,
# 可以获得整个邮件的原始文本
msg_content = b'\r\n'.join(lines).decode('utf-8')
# 只需要一行代码就可以把邮件内容解析为Message对象
msg = Parser().parsestr(msg_content)
# 可以根据邮件索引号直接从服务器删除邮件:
# server.dele(index)
# 关闭连接
server.quit()

# 但是这个Message对象本身可能是一个MIMEMultipart对象，即包含嵌套的其他MIMEBase对象，嵌套可能还不止一层。
# 所以我们要递归地打印出Message对象的层次结构
# indent用于缩进显示
def print_info(msg, indent=0):
    if indent == 0:
        for header in ['From', 'To', 'Subject']:
            value = msg.get(header, '')
            if value:
                if header == 'Subject':
                    value = decode_str(value)
                else:
                    hdr, addr = parseaddr(value)
                    name = decode_str(hdr)
                    value = u'%s <%s>' % (name, addr)
            print('%s%s: %s' % (' ' * indent, header, value))
    if (msg.is_multipart()):
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            print('%spart %s' % (' ' * indent, n))
            print('%s--------------------' % (' ' * indent))
            print_info(part, indent + 1)

    else:
        content_type = msg.get_content_type()
        if content_type == 'text/plain' or content_type == 'text/html':
            content = msg.get_payload(decode=True)
            charset = guess_charset(msg)
            if charset:
                content = content.decode(charset)
            print('%sText: %s' % (' ' * indent, content + '...'))
        else:
            print('%sAttachment: %s' % (' ' * indent, content_type))
# 邮件的Subject或者Email中包含的名字都是经过编码后的str，要正常显示，就必须decode
def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value
# decode_header()返回一个list，因为像Cc、Bcc这样的字段可能包含多个邮件地址，所以解析出来的会有多个元素。上面的代码我们偷了个懒，只取了第一个元素。
# 文本邮件的内容也是str，还需要检测编码，否则，非UTF-8编码的邮件都无法正常显示
def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset

# 用Python的poplib模块收取邮件分两步：第一步是用POP3协议把邮件获取到本地，
# 第二步是用email模块把原始邮件解析为Message对象，
# 然后，用适当的形式把邮件内容展示给用户即可
print_info(msg,2)