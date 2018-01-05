# !/usr/bin/env python
# -*- coding: utf-8 -*-

import re, http.cookiejar, os, requests, time, configparser,queue, threading
from urllib import parse, request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


__author__ = 'Hem1ng'

'''
    豆瓣电影Top100爬虫
'''
class DouBanSpider(object):

    def __init__(self):
        self.__page__ = 1
        self.cur_url = 'https://movie.douban.com/top250?start={page}&filter='
        self.datas = []
        self.picLinks = []
        self._top_num = 1

    # 获取当前页面内容
    def __getHTMLContent__(self, cur_page):
        url = self.cur_url
        my_page = (request.urlopen(url.format(page=(cur_page - 1)*25))).read().decode('utf-8')
        return my_page

    # 获取电影名称
    def __find_title__(self, my_page):
        temp_data = []
        # .*?是非贪婪模式匹配，一旦第一次匹配结束就不再往后继续匹配了
        # .*是贪婪模式匹配，第一次匹配结束继续往后匹配，直到字符串结束
        # re.S表示将.(表示除了换行符以外的所有字符)的作用扩展到整个字符串，包括换行符。
        movie_items = re.findall(r'<span.*?class="title">(.*?)</span>', my_page, re.S)
        for index, item in enumerate(movie_items):
            if item.find('&nbsp;') == -1:
                temp_data.append('Top'+str(self._top_num)+' '+item)
                self._top_num += 1
        self.datas.extend(temp_data)

    # 获取电影的缩略图链接
    def __find_picLinks__(self, my_page):
        movie_picLinks = re.findall(r'<img width="100" alt=.*?src=(.*?)class="">', my_page, re.S)
        for index, link in enumerate(movie_picLinks):
            self.picLinks.append(link)

    # 回调函数 @a:已经下载的数据块 @b:数据块的大小 @c:远程文件的大小
    def abc(self, a, b, c):
        per = 100.0 * a * b / c
        if per > 100:
            per = 100
        print ('%.2f%%' % per)

    # 下载图片
    def __downloadPic__(self, url, index):
        imageName = os.path.join(os.path.abspath('.'), str(index)+'.jpg')
        request.urlretrieve(url, imageName, self.abc)

    # 爬虫入口
    def start_spider(self):
        while self.__page__ <= 4:
            my_page = self.__getHTMLContent__(self.__page__)
            self.__find_title__(my_page)
            self.__find_picLinks__(my_page)
            self.__page__ += 1
        for index, link in enumerate(self.picLinks):
            print(index,link)
            self.__downloadPic__(link,index)
            break

'''
    豆瓣上关于《猎场》的前100条热门影评
'''
class ReviewSpider(object):

    def __init__(self):
        self.__page__ = 0
        self.__resp_page__ = 0
        self.__reviews__ = []
        self.__resp__ = []
        self.__pageUrl__ = 'https://movie.douban.com/subject/26322642/discussion/?start={page}&sort_by=vote'
        self.__respUrl__ = '{hostUrl}?start={respPage}&author=0#comments'

    # 获取热门影评页面内容
    def __getHTMLContent__(self, cur_page):
        url = self.__pageUrl__.format(page=cur_page*20)
        response = request.urlopen(url)
        page = response.read().decode('utf-8')
        return page

    # 获取热门影评标题和链接
    def __getReviewLinkAndTitle__(self, content):
        temp_data = re.findall(r'<a.*?href="(.*?)".*?title="(.*?)".*?class="">', content)
        for item in temp_data:
            self.__reviews__.append({'title':item[1],'url':item[0]})

    # 获取评论回复页数
    def __getResponsePageNumber__(self, content):
        temp_data = re.findall(r'<a href=".*" >(\d+)</a>', content)
        return(int(temp_data[-1]))

    # 获取影评和回复页面内容
    def __getResponseContent__(self, hostUrl, cur_page):
        url = self.__respUrl__.format(hostUrl=hostUrl, respPage=cur_page * 100)
        response = request.urlopen(url)
        page = response.read().decode('utf-8')
        # if cur_page == 0:
        #     respPages = self.__getResponsePageNumber__(page)
        #     return (page, respPages)
        # else:
        return page

    # 获取每条影评的内容
    def __getResponse__(self, reviewLink):
        resp = self.__getResponseContent__(reviewLink, self.__resp_page__)
        temp_data = re.findall(r'<p>(.*?)</p>', resp)
        self.__resp__.append(''.join(temp_data))

    # 构建请求头及表单信息
    def structure_loginHeaders(self, id, solution):
        form_data = parse.urlencode(self.__get_form_data__(id, solution)).encode(encoding='utf-8')
        user_agent = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2)'
                      'AppleWebKit/537.36 (KHTML, like Gecko)'
                      'Chrome/63.0.3239.84 Safari/537.36')
        request_header = {
            'Referer':'https://movie.douban.com/subject/26322642/discussion/?sort_by=vote',
            'User-Agent':user_agent
        }
        return form_data, request_header

    # 获取表单提交信息
    def __get_form_data__(self,id=None,solution=None):
        form_data = {
            'source': 'main',
            'redir': 'https://movie.douban.com/subject/26322642/discussion/?sort_by=vote',
            'form_email': '964085993@qq.com',
            'form_password': '***替换密码***',
            'captcha-solution': 'regret',
            'captcha-id': '5KKmZCLHbNrys9v1ZzydQRNa:en',
            'remember':'on',
            'login': '登录'
        }
        form_data['captcha-id']=id
        # form_data['captcha-solution']=solution
        return form_data

    # 登录豆瓣
    def __login_douban__(self):
        url = 'https://accounts.douban.com/login'
        fileName = 'cookie.txt'
        cookie = http.cookiejar.MozillaCookieJar(fileName)
        opener = request.build_opener(request.HTTPCookieProcessor(cookie))
        request.install_opener(opener)
        form_data, request_header = self.structure_loginHeaders('Qh9r9aDiCLRuRZt9eDIrBiCW:en',None)
        req = request.Request(url,data=form_data,headers=request_header)
        resp = request.urlopen(req)
        cookie.save(ignore_discard=True, ignore_expires=True)
        text = resp.read().decode()
        print(text)
        captcha_src = re.findall(r'<img id="captcha_image" src="(.*?)".*?/>', text)
        print(captcha_src)
        captcha_id = re.findall(r'<img id="captcha_image" src="https://.*id=(.*?):en&amp;size=s".*?/>', text)
        # if len(captcha_id):
        #     form_data, request_header = self.structure_loginHeaders(captcha_id[0],'sneeze')
        print('id =',captcha_id)

    def loginDoubanWithRequests(self):
        loginUrl = 'https://accounts.douban.com/login'
        loginData = {
            'source': 'main',
            'redir': 'https://www.douban.com/people/59490556/',
            'form_email': '964085993@qq.com',
            'form_password': 'daihuiming112911',
            'captcha-solution': 'position',
            'captcha-id': 'r8YBi57G7aJ2VCHqKnEcXfKS:en',
            'remember': 'on',
            'login': '登录'
        }
        header = {
            'Referer': 'https://www.douban.com/login',
            'Host': 'accounts.douban.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2)' 'AppleWebKit/537.36 (KHTML, like Gecko)' 'Chrome/63.0.3239.84 Safari/537.36'
        }

        # session = requests.session()
        # resp = session.post(loginUrl,data=loginData,headers=header)
        # r = session.get('https://www.douban.com/settings/')
        cookies = {'bid':'yQsMh13PJfs','ps':'y','push_doumail_num':'0','push_noty_num':'0','ue':'"964085993@qq.com"	','ap':'1','ck':'NSsp','dbcl2':'"59490556:et0rMKMIL/I"', '__utmc':'30149280','__utmz':'30149280.1513834668.1.1.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/login', '__utma':'30149280.988031542.1513834668.1513834668.1513834668.1','__utmv':'30149280.5949','__utmt':'', '__utmb':'','__yadk_uid':'Gyx8o19L8IwW4YsPKir1odHLuoyyRWuc','_pk_id.100001.8cb4':'ea8d4cc08f313e2e.1513834667.1.1513834667.1513834667.','_pk_ref.100001.8cb4':'%5B%22%22%2C%22%22%2C1513834667%2C%22https%3A%2F%2Faccounts.douban.com%2Flogin%3Falias%3D964085993%2540qq.com%26redir%3Dhttps%253A%252F%252Fwww.douban.com%26source%3DNone%26error%3D1011%22%5D'}
        # r = session.get('https://www.douban.com/settings/',cookies=cookies)
        # 需要登录分两种情况：
        # 第一种手动登陆后从浏览器获取登陆后的cookie，再请求需要登录的页面
        # 第二种通过用户名密码（甚至验证码）进行post请求
        r = requests.get('https://www.douban.com/settings/', cookies=cookies)
        print(r.content.decode('utf-8'))

    # 爬虫入口
    def start_spider(self):
        # cf = configparser.ConfigParser()
        # cf.read('config')
        # cookies = cf.items('cookies')
        # print(cookies)
        # cookiesDic = dict(cookies)
        # print(cookiesDic)
        self.loginDoubanWithRequests()


        # self.__login_douban__()
        # page = 0
        # print('热门影评爬取开始...')
        # while self.__page__ < 3:
        #     page += 1
        #     print('爬取第%s页热评' % page)
        #     content = self.__getHTMLContent__(self.__page__)
        #     self.__getReviewLinkAndTitle__(content)
        #     self.__page__ += 1
        # print('热门影评爬取结束...')
        # print('影评内容爬取开始...')
        # num = 0
        # for review in self.__reviews__:
        #     num += 1
        #     print('爬取第%s条热评内容...' % num)
        #     self.__getResponse__(review['url'])
        # print('影评内容爬取结束...')
        # for c in self.__resp__:
        #     print(c)

def makeDir(path):
    path = path.strip()
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)

def saveImg(url, name):
    img = requests.get(url)
    time.sleep(3)
    fileName = name+'.jpg'
    with open(fileName,'ab') as f:
        f.write(img.content)
        print('保存成功')

def downloadImage(q):
    while True:
        try:
            url = q.get_nowait()
            i = q.qsize()
        except Exception as e:
            print(e)
            break
        img = requests.get(url, stream=True)
        fileName = str(i) + '.jpg'
        with open(fileName, 'wb') as f:
            f.write(img.content)
            print('保存成功')

def scroll_down(driver, times):
    for i in range(times):
        print('执行第%s次下拉操作' % str(i+1))
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);') # 执行js实现网页下拉到底
        print('第%s次下拉操作执行完毕' % str(i+1))
        print('等待网页加载')
        time.sleep(10) # 等待网页加载
        print(driver.page_source)

if __name__ == '__main__':
    # ************** 电影Top100 *************** #
    # mySpider = DouBanSpider()
    # print('豆瓣电影爬取开始...')
    # mySpider.start_spider()
    # print('豆瓣电影爬取结束...')

    # **************《猎场热门影评》*************** #
    # reviewSpider = ReviewSpider()
    # reviewSpider.start_spider()

    # html_doc = '''
    # <html>
    #     <head>
    #         <title>The Dormouse's story</title>
    #     </head>
    #     <body>
    #         <p class="title"><b>The Dormouse's story</b></p>
    #         <p class="story">Once upon a time there were three little sisters, and their names were
    #             <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
    #             <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a>,and
    #             <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
    #         they lived at the bottom of a well.</p>
    #         <p class="story">...</p>
    #     </body>
    # </html>
    # '''
    # soup = BeautifulSoup(html_doc,'lxml')
    # find = soup.find('p')
    # print(type(find)) #p标签的类型:Tag
    # print(find) #完整的p标签
    # print(find.name) #p标签的名称
    # print(find['class']) #p标签属性class的值
    # print(find.string) #p标签的内容:NavigableString
    # print(soup) #表示整个html页面内容
    # print(soup.head) #表示查找head标签
    # print(soup.p) #查找第一个p标签
    # for child in soup.body.children: #遍历body标签里面的所有子标签
    #     print(child)
    # print(soup.title.parent) #查找title标签的父标签
    # for parent in soup.a.parents: #查找a标签的所有父标签
    #     if parent is None:
    #         print(parent)
    #     else:
    #         print(parent.name)
    # print('***',soup.a.next_sibling) #a标签的后面兄弟标签
    # print('###',soup.a.previous_sibling) #a标签的前面兄弟标签
    # find_all( name , attrs , recursive , string , **kwargs )
    # name 参数：可以查找所有名字为 name 的tag。
    # attr 参数：就是tag里的属性。
    # string 参数：搜索文档中字符串的内容。
    # recursive 参数： 调用tag的 find_all() 方法时，Beautiful Soup会检索当前tag的所有子孙节点。如果只想搜索tag的直接子节点，可以使用参数 recursive=False 。
    # print(soup.find_all('title')) #查找所有的title标签结果为list
    # print(soup.find_all('a',id='link3')) #查找所有id=link3的a标签
    # print(soup.find(string=re.compile(r'sister')))
    #
    # markup = "<b><!--Hey, buddy. Want to buy a used parser?--></b>"
    # soup1 = BeautifulSoup(markup, 'lxml')
    # print(soup1.b.string) #获取注释
    # r = '''<div id="gridMulti" class="_3_WtK _2TNYr _1C-lZ" data-test="photos-grid-view">
    #             <div class="_1OvAL _2T3hc _27nWV">
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img alt="A cautious fox walking across the forest floor on a spring's day" src="https://images.unsplash.com/photo-1440658172029-9d9e5cdc127c?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=344&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 234px;"></div><div class="bQJ8Z"><a title="View the photo by Andreas Rønningen" class="_23lr1" href="/photos/w3lQVmuK8fw"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img alt="A herd of grey and white horses on a green pasture in Wales" src="https://images.unsplash.com/photo-1478028928718-7bfdb1b32095?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=379&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 258px;"></div><div class="bQJ8Z"><a title="View the photo by Samantha Scholl" class="_23lr1" href="/photos/usk52YRwGrM"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img src="https://images.unsplash.com/photo-1490633874781-1c63cc424610?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=379&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 258px;"></div><div class="bQJ8Z"><a title="View the photo by Ksenia Makagonova" class="_23lr1" href="/photos/LuK-MuZ-yf0"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img src="https://images.unsplash.com/photo-1505816328275-34db3b7cef14?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=379&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 258px;"></div><div class="bQJ8Z"><a title="View the photo by Jonatan Pie" class="_23lr1" href="/photos/hFU3FJfVycM"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img src="https://images.unsplash.com/photo-1483524091138-eef1bc4cbe54?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=379&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 258px;"></div><div class="bQJ8Z"><a title="View the photo by Janko Ferlič" class="_23lr1" href="/photos/2ye7E7HQm04"></a></div></div></div>'''

    # soup = BeautifulSoup(r, 'lxml')
    # all_img = soup.find_all('img', class_='KW7g_ _1hz5D')
    # imgDir = os.path.join(os.path.abspath('.'),'img')
    # makeDir(imgDir)
    # os.chdir(imgDir)
    # for index, img in enumerate(all_img):
    #     saveImg(img['src'],str(index))

    # chromedriver = '/Applications/Google Chrome.app/Contents/MacOS/chromedriver'
    # driver = webdriver.Chrome(chromedriver) # 指定使用的浏览器
    # driver.get('http://www.python.org') # 请求网址
    # print(driver.title)
    # assert 'Python' in driver.title # 看看Python是否在网页的表其中，如果不在则终止程序，否则程序继续
    # elem = driver.find_element_by_name('q') # 找到name为q的元素，这里是个搜索框
    # elem.clear() # 清空搜索框的内容
    # elem.send_keys('pycon') # 在搜框中输入pycon
    # elem.send_keys(Keys.RETURN) # 相当于回车，提交
    # assert 'No results found.' not in driver.page_source # 如果当前页面文本中有'No results found.'则终止程序
    # driver.close() # 关闭webdriver

    driver = webdriver.PhantomJS()
    driver.get('http://music.163.com/#/artist/album?id=3691&limit=105&offset=0')
    driver.switch_to.frame('g_iframe')
    soup = BeautifulSoup(driver.page_source, 'lxml')
    ul = soup.find('ul', id='m-song-module')
    all_li = ul.find_all('li')
    datas = []
    for li in all_li:
        album_img = li.find('img')['src']
        endpos = album_img.index('?')
        album_name = li.find('a',class_='tit s-fc0').string
        album_time = li.find('span').string
        datas.append({'img':album_img[:endpos],'name':album_name,'time':album_time})
    imgDir = os.path.join(os.path.abspath('.'),'img')
    makeDir(imgDir)
    os.chdir(imgDir)
    fileNames = os.listdir(imgDir) # 获取当前路径下所有文件及子文件夹的名字
    # 单线程下载图片
    # for item in datas:
    #     if item['time']+'-'+item['name']+'.jpg' in fileNames:
    #         print('图片已存在')
    #     else:
            # saveImg(item['img'],item['time']+'-'+item['name'])

    # 多线程下载图片
    q = queue.Queue()
    for urlItem in datas:
        q.put(urlItem['img'])
    t = threading.Thread(target=downloadImage, args=(q,))
    t.start()
    t.join()
