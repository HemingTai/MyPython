from PIL import Image, ImageFilter, ImageDraw, ImageFont
import random
import requests

# ******************************** 图片处理 ***************************************

# 高斯模糊效果
im = Image.open('pic7_05@2x.png')
im2 = im.filter(ImageFilter.BLUR)
im2.save('blur.png')

# 随机字母
def rndChar():
    return chr(random.randint(65, 90))
# 随机颜色
def rndColor():
    return (random.randint(64,255), random.randint(64,255), random.randint(64,255))
# 随机颜色
def rndColor2():
    return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))

width = 240
height = 60
image = Image.new('RGB', (width, height), (255, 255, 255))
font = ImageFont.truetype('Arial.ttf', 36)
draw = ImageDraw.Draw(image)
# 填充像素
for x in range(width):
    for y in range(height):
        draw.point((x, y), fill=rndColor())
# 输出文字
for t in range(4):
    draw.text((60 * t + 10, 10), rndChar(), font=font, fill=rndColor2())
image = image.filter(ImageFilter.BLUR)
image.save('verify.jpg','jpeg')

# ************************** 网络请求 *************************************

# GET请求
r = requests.get('https://www.douban.com')
if r.status_code == 200:
    print(r.text)

# 带参数传入dict
r = requests.get('https://www.douban.com/search', params={'q':'python', 'cat':'1001'})
print(r.url)
if r.status_code == 200:
    # requests自动检测编码，可以使用encoding属性查看
    print(r.encoding)
    # 用content属性获得bytes对象
    print(r.content)

# requests的方便之处还在于，对于特定类型的响应，例如JSON，可以直接获取
r1 = requests.get('https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20%3D%202151330&format=json')
print(r1.json())

# 需要传入HTTP Header时，我们传入一个dict作为headers参数
r2 = requests.get('https://www.douban.com/', headers={'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit'})
print(r2.text)

# 要发送POST请求，只需要把get()方法变成post()，然后传入data参数作为POST请求的数据
r3 = requests.post('https://accounts.douban.com/login', data={'form_email': 'abc@example.com', 'form_password': '123456'})

# requests默认使用application/x-www-form-urlencoded对POST数据编码。如果要传递JSON数据，可以直接传入json参数
param = {'key':'value'}
r4 = requests.post('url', json=param)

# 上传文件需要更复杂的编码格式，但是requests把它简化成files参数
# 在读取文件时，注意务必使用'rb'即二进制模式读取，这样获取的bytes长度才是文件的长度
# 把post()方法替换为put()，delete()等，就可以以PUT或DELETE方式请求资源
upload_files = {'file': open('report.xls', 'rb')}
r5 = requests.post('url', files=upload_files)

# 除了能轻松获取响应内容外，requests对获取HTTP响应的其他信息也非常简单。例如，获取响应头
print(r.headers)

# requests对Cookie做了特殊处理，使得我们不必解析Cookie就可以轻松获取指定的Cookie
print(r.cookies)
print(r.cookies['ts'])

# 要在请求中传入Cookie，只需准备一个dict传入cookies参数
cs = {'token': '12345', 'status': 'working'}
r = requests.get('url', cookies=cs)

# 最后，要指定超时，传入以秒为单位的timeout参数
r = requests.get('url', timeout= 30)

