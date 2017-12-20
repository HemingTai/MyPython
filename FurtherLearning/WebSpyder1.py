# !/usr/bin/env python
# -*- coding: utf-8 -*-

import re, http.cookiejar, os, requests, time
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
            'form_password': 'daihuiming112911',
            'captcha-solution': 'regret',
            'captcha-id': '5KKmZCLHbNrys9v1ZzydQRNa:en',
            'remember':'on',
            'login': '登录'
        }
        form_data['captcha-id']=id
        # form_data['captcha-solution']=solution
        return form_data

    # 登录豆瓣
    def login_douban(self):
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

    # 爬虫入口
    def start_spider(self):
        # self.login_douban()
        page = 0
        print('热门影评爬取开始...')
        while self.__page__ < 10:
            page += 1
            print('爬取第%s页热评' % page)
            content = self.__getHTMLContent__(self.__page__)
            self.__getReviewLinkAndTitle__(content)
            self.__page__ += 1
        print('热门影评爬取结束...')
        print('影评内容爬取开始...')
        num = 0
        for review in self.__reviews__:
            num += 1
            print('爬取第%s条热评内容...' % num)
            self.__getResponse__(review['url'])
        print('影评内容爬取结束...')
        for c in self.__resp__:
            print(c)

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
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img alt="Overhead shot of assorted bouquet of tulips in bloom in spring, Vienna" src="https://images.unsplash.com/photo-1456415333674-42b11b9f5b7b?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=426&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 290px;"></div><div class="bQJ8Z"><a title="View the photo by Gábor Juhász" class="_23lr1" href="/photos/B1Zyw7sdm5w"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img src="https://images.unsplash.com/photo-1490323948794-cc6dde6e8f5b?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=391&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 267px;"></div><div class="bQJ8Z"><a title="View the photo by Brenda Godinez" class="_23lr1" href="/photos/OY6QR6-EiWQ"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img src="https://images.unsplash.com/photo-1502477639450-ccb7a6e7c391?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=379&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 258px;"></div><div class="bQJ8Z"><a title="View the photo by Meireles Neto" class="_23lr1" href="/photos/Cn56Qekcygc"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img src="https://images.unsplash.com/photo-1506395308321-904a71783d60?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=861&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 586px;"></div><div class="bQJ8Z"><a title="View the photo by Brooke Lark" class="_23lr1" href="/photos/AgD6OBNXF0Q"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img alt="Silhouettes of riders on horseback against the radiant sun breaking through the trees" src="https://images.unsplash.com/photo-1466495227171-d05d7e3ac2b3?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=355&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 242px;"></div><div class="bQJ8Z"><a title="View the photo by Tobias Keller" class="_23lr1" href="/photos/ucdh5HMkRMg"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img src="https://images.unsplash.com/photo-1469536526925-9b5547cd5d68?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=378&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 258px;"></div><div class="bQJ8Z"><a title="View the photo by George Hiles" class="_23lr1" href="/photos/ed-hLWaknyk"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img alt="Polar bear with half-closed eyes and wet fur in a dark cave in Bronx Zoo" src="https://images.unsplash.com/photo-1501789924847-cbbec7dabcf7?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=379&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 258px;"></div><div class="bQJ8Z"><a title="View the photo by tyler gebhart" class="_23lr1" href="/photos/EM2qDcsiRj0"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img src="https://images.unsplash.com/photo-1448907399011-d1b62a3ba38d?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=406&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 276px;"></div><div class="bQJ8Z"><a title="View the photo by Robby Schlegel" class="_23lr1" href="/photos/T84Q30L8xZw"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img alt="A person typing on a netbook with plants, pencils, a smartphone and glasses on the desk table" src="https://images.unsplash.com/photo-1487611459768-bd414656ea10?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=379&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 258px;"></div><div class="bQJ8Z"><a title="View the photo by Corinne Kutz" class="_23lr1" href="/photos/tMI2_-r5Nfo"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img src="https://images.unsplash.com/photo-1503264116251-35a269479413?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=379&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 258px;"></div><div class="bQJ8Z"><a title="View the photo by Aperture Vintage" class="_23lr1" href="/photos/SshYpuf607g"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img src="https://images.unsplash.com/photo-1507908708918-778587c9e563?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=852&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 581px;"></div><div class="bQJ8Z"><a title="View the photo by Johny Goerend" class="_23lr1" href="/photos/Oz2ZQ2j8We8"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img src="https://images.unsplash.com/photo-1512927638316-b12f8c1abcc4?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=379&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 258px;"></div><div class="bQJ8Z"><a title="View the photo by Joe Green" class="_23lr1" href="/photos/LKwo0PfwSTs"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img src="https://images.unsplash.com/photo-1512318601939-07bf29f1b74e?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=379&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 258px;"></div><div class="bQJ8Z"><a title="View the photo by Thomas Peham" class="_23lr1" href="/photos/8RapT49-eqI"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img src="https://images.unsplash.com/photo-1512549961816-1f925c94d9db?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=757&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 516px;"></div><div class="bQJ8Z"><a title="View the photo by Saz B" class="_23lr1" href="/photos/U4dqUuwbWoA"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img src="https://images.unsplash.com/photo-1512290793455-dd2f915493bc?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=657&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 448px;"></div><div class="bQJ8Z"><a title="View the photo by Annie Spratt" class="_23lr1" href="/photos/bxt-tWSF-Ko"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img src="https://images.unsplash.com/photo-1488643637913-82a3820cf051?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=379&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 258px;"></div><div class="bQJ8Z"><a title="View the photo by Daniele Levis Pelusi" class="_23lr1" href="/photos/aRf1hjEHlhA"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img alt="Green and orange trees in Yosemite during autumn" src="https://images.unsplash.com/photo-1500171945981-bd5ddaa2ee00?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=852&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 581px;"></div><div class="bQJ8Z"><a title="View the photo by Ivana Cajina" class="_23lr1" href="/photos/g6B4rdvegMc"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img alt="Classic sunset silhouette of couple kissing with sea wind frizzing their hair" src="https://images.unsplash.com/reserve/165aTVpzTXGMXu1azUdy_IMG_8468.JPG?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=377&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 257px;"></div><div class="bQJ8Z"><a title="View the photo by Alejandra Quiroz" class="_23lr1" href="/photos/F5hTTI4Hlv4"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img src="https://images.unsplash.com/photo-1495431088732-09e59535d241?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=379&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 258px;"></div><div class="bQJ8Z"><a title="View the photo by Eugene Lim" class="_23lr1" href="/photos/X3MNSra7o9s"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img src="https://images.unsplash.com/photo-1507667522877-ad03f0c7b0e0?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=853&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 581px;"></div><div class="bQJ8Z"><a title="View the photo by Marcelo Vaz" class="_23lr1" href="/photos/ka6WGHXcFMY"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img src="https://images.unsplash.com/photo-1487750022055-974f66325e0f?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=379&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 258px;"></div><div class="bQJ8Z"><a title="View the photo by paul morris" class="_23lr1" href="/photos/myu2QyUgL2k"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img src="https://images.unsplash.com/photo-1495802515684-de80695df90e?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=379&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 258px;"></div><div class="bQJ8Z"><a title="View the photo by Bill Hamway" class="_23lr1" href="/photos/GOhA-vkKzDg"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img src="https://images.unsplash.com/photo-1505851543971-19811a8f4c21?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=852&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 581px;"></div><div class="bQJ8Z"><a title="View the photo by Bryan Goff" class="_23lr1" href="/photos/NPyXoUUlrqg"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img alt="A hand holding a vintage video camera with stickers on it" src="https://images.unsplash.com/photo-1485811055483-1c09e64d4576?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=379&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 258px;"></div><div class="bQJ8Z"><a title="View the photo by Sticker Mule" class="_23lr1" href="/photos/cPSroMqTRQg"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img src="https://images.unsplash.com/photo-1495464101292-552d0b52fe41?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=379&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 258px;"></div><div class="bQJ8Z"><a title="View the photo by Kinson Leung" class="_23lr1" href="/photos/5xVPhqbC4bQ"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img src="https://images.unsplash.com/photo-1507032336878-13f159192baa?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=379&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 258px;"></div><div class="bQJ8Z"><a title="View the photo by Rina Miele" class="_23lr1" href="/photos/-7_yLivAnMc"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img src="https://images.unsplash.com/photo-1501879779179-4576bae71d8d?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=379&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 258px;"></div><div class="bQJ8Z"><a title="View the photo by Vladimir Riabinin" class="_23lr1" href="/photos/diMBLU4FzDQ"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img alt="A roe deer grazing on grass next to a forest road" src="https://images.unsplash.com/photo-1427434991195-f42379e2139d?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=320&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 218px;"></div><div class="bQJ8Z"><a title="View the photo by Vladimir Kudinov" class="_23lr1" href="/photos/vmlJcey6HEU"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img src="https://images.unsplash.com/photo-1494253188410-ff0cdea5499e?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=379&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 258px;"></div><div class="bQJ8Z"><a title="View the photo by Martin Jernberg" class="_23lr1" href="/photos/UdURxHDhrgY"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img src="https://images.unsplash.com/photo-1507608158173-1dcec673a2e5?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=379&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 258px;"></div><div class="bQJ8Z"><a title="View the photo by Autumn Studio" class="_23lr1" href="/photos/221wufG10eg"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img src="https://images.unsplash.com/photo-1510279770292-4b34de9f5c23?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=379&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 258px;"></div><div class="bQJ8Z"><a title="View the photo by Iswanto Arif" class="_23lr1" href="/photos/OJ74pFtrYi0"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img src="https://images.unsplash.com/photo-1506802913710-40e2e66339c9?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=852&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 581px;"></div><div class="bQJ8Z"><a title="View the photo by Alex Loup" class="_23lr1" href="/photos/HDjExSGuWUw"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img alt="Glass of blended tropical coconut drink surrounded by fresh coconuts" src="https://images.unsplash.com/photo-1473115209096-e0375dd6b3b3?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=379&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 258px;"></div><div class="bQJ8Z"><a title="View the photo by Alexander Mils instagram.com/alexandermils" class="_23lr1" href="/photos/ocku3zjNM7k"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img alt="Boat passes through calm ripples on a foggy day on the water" src="https://images.unsplash.com/photo-1422112528461-3186878f87dc?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=426&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 290px;"></div><div class="bQJ8Z"><a title="View the photo by Ryan Wilson" class="_23lr1" href="/photos/1fyccRaS_u4"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img src="https://images.unsplash.com/photo-1487715433499-93acdc0bd7c3?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=349&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 238px;"></div><div class="bQJ8Z"><a title="View the photo by Luca Baggio" class="_23lr1" href="/photos/eKU3JGNCCMg"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img alt="Coastal town of Vernazza in Italy, its buildings glowing orange as the sun sets behind a mountain" src="https://images.unsplash.com/photo-1499678329028-101435549a4e?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=379&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 258px;"></div><div class="bQJ8Z"><a title="View the photo by Anders Jildén" class="_23lr1" href="/photos/cYrMQA7a3Wc"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img src="https://images.unsplash.com/photo-1506351421178-63b52a2d2562?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=320&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 218px;"></div><div class="bQJ8Z"><a title="View the photo by Duy Nguyen" class="_23lr1" href="/photos/9WwWGeHEbmQ"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img alt="Rustic cabin on a serene lake surrounded by mountains" src="https://images.unsplash.com/photo-1470020337050-543c4e581988?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=379&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 258px;"></div><div class="bQJ8Z"><a title="View the photo by Darius Soodmand" class="_23lr1" href="/photos/piG9Ye_oHrI"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img src="https://images.unsplash.com/photo-1494971416041-5b9ec17a814b?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=379&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 258px;"></div><div class="bQJ8Z"><a title="View the photo by Raphael Koh" class="_23lr1" href="/photos/MzIiekUr6m8"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img src="https://images.unsplash.com/photo-1509957660513-3cfee07defec?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=361&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 246px;"></div><div class="bQJ8Z"><a title="View the photo by Willian Justen de Vasconcellos" class="_23lr1" href="/photos/8QA3xEsKD0s"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img src="https://images.unsplash.com/photo-1455717974081-0436a066bb96?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=852&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 581px;"></div><div class="bQJ8Z"><a title="View the photo by Teddy Kelley" class="_23lr1" href="/photos/cmKPOUgdmWc"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img src="https://images.unsplash.com/photo-1506084868230-bb9d95c24759?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=852&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 581px;"></div><div class="bQJ8Z"><a title="View the photo by Calum Lewis" class="_23lr1" href="/photos/8Nc_oQsc2qQ"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img alt="An iPhone, an Apple Watch and a digital camera on a wooden surface" src="https://images.unsplash.com/photo-1483383490964-8335c18b6666?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=426&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 290px;"></div><div class="bQJ8Z"><a title="View the photo by Aaron Burden" class="_23lr1" href="/photos/_5SvtBPDKhU"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img alt="A person holding bouquet of white carnations and pink roses wrapped in decorative paper" src="https://images.unsplash.com/photo-1494336850228-54adc1dd87ad?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=852&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 581px;"></div><div class="bQJ8Z"><a title="View the photo by Lizzie" class="_23lr1" href="/photos/ZlDnZb3i15Y"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img alt="Rocks jut out from the reflective surface of a shallow lake in the mountains" src="https://images.unsplash.com/photo-1492854536278-1f94bbec5732?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=379&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 258px;"></div><div class="bQJ8Z"><a title="View the photo by Sean Afnan" class="_23lr1" href="/photos/i17Ln-C-qhE"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img alt="A squirrel with a dark background." src="https://images.unsplash.com/photo-1504006833117-8886a355efbf?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=379&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 258px;"></div><div class="bQJ8Z"><a title="View the photo by Geran de Klerk" class="_23lr1" href="/photos/bKhETeDV1WM"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img alt="Looking up at dark clouds from the base of a modern skyscraper in Bucharest." src="https://images.unsplash.com/photo-1448357019934-caa4696bb949?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=852&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 580px;"></div><div class="bQJ8Z"><a title="View the photo by Ciprian Lipenschi" class="_23lr1" href="/photos/OULAwYI3AGs"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img alt="An aerial shot of vacationers on a sandy beach with blue umbrellas and deck chairs" src="https://images.unsplash.com/photo-1488120299791-f9241bdf10c9?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=347&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 237px;"></div><div class="bQJ8Z"><a title="View the photo by Mikael Cho" class="_23lr1" href="/photos/_3TDkAttcaM"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img alt="Person looks at a abandoned plane crash site in Solheimasandur Plane Wreck" src="https://images.unsplash.com/photo-1489595461171-4764773fd3a2?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=406&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 276px;"></div><div class="bQJ8Z"><a title="View the photo by Mahkeo" class="_23lr1" href="/photos/m76_jjV-rRI"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img alt="A drone shot of a frozen lake in Bozeman" src="https://images.unsplash.com/photo-1490635816794-8fd653ab48ee?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=379&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 258px;"></div><div class="bQJ8Z"><a title="View the photo by Stephen Pedersen" class="_23lr1" href="/photos/JSCQUok9y9Q"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img alt="A person kayaking by the mountains in Swiftcurrent Lake" src="https://images.unsplash.com/photo-1468549940493-46152524296c?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=436&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 297px;"></div><div class="bQJ8Z"><a title="View the photo by Nitish Meena" class="_23lr1" href="/photos/RWAIyGmgHTQ"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img alt="The Echo Lake in the dusk surrounded by trees and a mountain covered in snow" src="https://images.unsplash.com/photo-1497996377197-e4b9024658a4?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=379&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 258px;"></div><div class="bQJ8Z"><a title="View the photo by Levi Bare" class="_23lr1" href="/photos/xCfHL21VpDk"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img src="https://images.unsplash.com/photo-1443866835201-3aed4094be2a?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=379&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 258px;"></div><div class="bQJ8Z"><a title="View the photo by Anna Jiménez Calaf" class="_23lr1" href="/photos/oyRcqwv0YnA"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img alt="A man standing on a grass-covered ledge with view on craggy mountain peaks" src="https://images.unsplash.com/photo-1470138831303-3e77dd49163e?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=379&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 258px;"></div><div class="bQJ8Z"><a title="View the photo by Joshua Earle" class="_23lr1" href="/photos/8MbdD0pHXGY"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img src="https://images.unsplash.com/photo-1495389948407-1a7dfe01c1c2?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=379&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 258px;"></div><div class="bQJ8Z"><a title="View the photo by Tanja Heffner" class="_23lr1" href="/photos/jJyN5k-BRqY"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img src="https://images.unsplash.com/photo-1504681869696-d977211a5f4c?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=1011&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 689px;"></div><div class="bQJ8Z"><a title="View the photo by James Donaldson" class="_23lr1" href="/photos/toPRrcyAIUY"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img src="https://images.unsplash.com/photo-1510849090660-6c8e1908c3c9?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=382&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 260px;"></div><div class="bQJ8Z"><a title="View the photo by Pana  Vasquez" class="_23lr1" href="/photos/9-imF7FAT-k"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img src="https://images.unsplash.com/photo-1511211883643-af111278ec5c?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=379&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 258px;"></div><div class="bQJ8Z"><a title="View the photo by Aaron Barnaby" class="_23lr1" href="/photos/dp2m5glF2Y4"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img src="https://images.unsplash.com/photo-1509514378902-b575b690bb13?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=852&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 581px;"></div><div class="bQJ8Z"><a title="View the photo by Matt Brockie" class="_23lr1" href="/photos/fkJl4HrTeM0"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img alt="Young wild red fox looks up in a wildflower field" src="https://images.unsplash.com/photo-1500531359996-c89a0e63e49c?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=379&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 258px;"></div><div class="bQJ8Z"><a title="View the photo by Nathan Anderson" class="_23lr1" href="/photos/7TGVEgcTKlY"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img src="https://images.unsplash.com/photo-1505833467875-2506f61a70eb?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=426&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 290px;"></div><div class="bQJ8Z"><a title="View the photo by Valentin" class="_23lr1" href="/photos/i4nhd3HE3Pk"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img alt="A person taking notes in a red notebook with a dinosaur on its cover while standing" src="https://images.unsplash.com/photo-1485458029194-00cff7de3ef7?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=379&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 258px;"></div><div class="bQJ8Z"><a title="View the photo by Sticker Mule" class="_23lr1" href="/photos/B6-8HwbRJz4"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img src="https://images.unsplash.com/photo-1508288155660-625e378b3fc9?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=379&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 258px;"></div><div class="bQJ8Z"><a title="View the photo by louis amal" class="_23lr1" href="/photos/ic6CAdKfDZQ"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img src="https://images.unsplash.com/photo-1506277020973-664d64ae9be0?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=426&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 290px;"></div><div class="bQJ8Z"><a title="View the photo by Shobhit Dutta" class="_23lr1" href="/photos/o2_1mppPM9k"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img alt="Musician playing trumpet alone in an empty forest field" src="https://images.unsplash.com/photo-1486092642310-0c4e84309adb?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=379&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 258px;"></div><div class="bQJ8Z"><a title="View the photo by Priscilla Du Preez" class="_23lr1" href="/photos/NP3KdAQc6c4"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img src="https://images.unsplash.com/photo-1501371703172-850ab6b6e282?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=698&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 475px;"></div><div class="bQJ8Z"><a title="View the photo by Alan Labisch" class="_23lr1" href="/photos/DdjJ91eIFVc"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img alt="Western University industrial power plant" src="https://images.unsplash.com/photo-1494818889428-42c443ab9f69?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=379&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 258px;"></div><div class="bQJ8Z"><a title="View the photo by Scott Webb" class="_23lr1" href="/photos/KF6EEForBB0"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img src="https://images.unsplash.com/photo-1500817487388-039e623edc21?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=848&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 578px;"></div><div class="bQJ8Z"><a title="View the photo by Samuel Ferrara" class="_23lr1" href="/photos/dKJXkKCF2D8"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img src="https://images.unsplash.com/photo-1509886745582-64bd84c3560e?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=379&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 258px;"></div><div class="bQJ8Z"><a title="View the photo by Vincent van Zalinge" class="_23lr1" href="/photos/aSYexjDxnX4"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img alt="Aerial view of the foggy atmosphere over mountains in Scotland" src="https://images.unsplash.com/photo-1469386220931-a05a3a71cbb5?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=379&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 258px;"></div><div class="bQJ8Z"><a title="View the photo by Alex Holyoake" class="_23lr1" href="/photos/Kxqnus0K8o8"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img alt="Two white vases with pink and white blossom branches on a table" src="https://images.unsplash.com/photo-1490312278390-ab64016e0aa9?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=379&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 258px;"></div><div class="bQJ8Z"><a title="View the photo by Maarten Deckers" class="_23lr1" href="/photos/0-frPETzEVs"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img src="https://images.unsplash.com/photo-1484542959923-de288ec85ce1?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=379&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 258px;"></div><div class="bQJ8Z"><a title="View the photo by Linda Xu" class="_23lr1" href="/photos/z0FNUvpunYs"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img alt="A shirtless man with tattoos on his body and rings on his fingers having a punk haircut in London" src="https://images.unsplash.com/photo-1475868530036-7e1f42b9c91c?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=410&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 280px;"></div><div class="bQJ8Z"><a title="View the photo by Clem Onojeghuo" class="_23lr1" href="/photos/WvS0rSIFAJE"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img alt="An upside down photograph of a blonde-haired woman in a greenhouse" src="https://images.unsplash.com/photo-1494948100334-41fd7a60ee8f?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=379&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 258px;"></div><div class="bQJ8Z"><a title="View the photo by Tanja Heffner" class="_23lr1" href="/photos/uDC-nZxHzbU"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img src="https://images.unsplash.com/photo-1508238024271-28d62d849697?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=379&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 258px;"></div><div class="bQJ8Z"><a title="View the photo by jens johnsson" class="_23lr1" href="/photos/_CBi1sMAFn4"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img src="https://images.unsplash.com/photo-1439886183900-e79ec0057170?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=348&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 237px;"></div><div class="bQJ8Z"><a title="View the photo by Andreas P." class="_23lr1" href="/photos/XN_CrZWxGDM"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img src="https://images.unsplash.com/photo-1478145046317-39f10e56b5e9?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=852&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 581px;"></div><div class="bQJ8Z"><a title="View the photo by Brooke Lark" class="_23lr1" href="/photos/1Rm9GLHV0UA"></a></div></div></div></div><div class="_1OvAL _2T3hc _27nWV">
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img src="https://images.unsplash.com/photo-1464061884326-64f6ebd57f83?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=379&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 258px;"></div><div class="bQJ8Z"><a title="View the photo by Alberto Restifo" class="_23lr1" href="/photos/wpMQWrjwPLs"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img src="https://images.unsplash.com/photo-1484506097116-1bcba4fa7568?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=379&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 258px;"></div><div class="bQJ8Z"><a title="View the photo by Jakob Owens" class="_23lr1" href="/photos/TMxUnMAAwFA"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img alt="People climbing a rock formation in the middle of the sea at Trevellas Cove" src="https://images.unsplash.com/photo-1490921045028-16ab0b47b757?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=757&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 516px;"></div><div class="bQJ8Z"><a title="View the photo by Matt Cannon" class="_23lr1" href="/photos/bb6VgZv-AaA"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img alt="The enormous Burj Khalifa skyscraper in the skyline of Dubai" src="https://images.unsplash.com/photo-1465414829459-d228b58caf6e?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=377&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 257px;"></div><div class="bQJ8Z"><a title="View the photo by Roman Logov" class="_23lr1" href="/photos/f5QWC1a3tOA"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img src="https://images.unsplash.com/photo-1494441822480-6bda707f0bd0?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=379&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 258px;"></div><div class="bQJ8Z"><a title="View the photo by Brandon Wong" class="_23lr1" href="/photos/qZMiOEmkaJI"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img src="https://images.unsplash.com/photo-1505762088641-031f116a9906?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=379&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 258px;"></div><div class="bQJ8Z"><a title="View the photo by Clayton Caldwell" class="_23lr1" href="/photos/nFAKTXxah1Q"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img src="https://images.unsplash.com/photo-1506605133577-b04c59c80a71?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=426&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 290px;"></div><div class="bQJ8Z"><a title="View the photo by Iswanto Arif" class="_23lr1" href="/photos/6yiq2HPIW7Q"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img alt="A waterfall pouring into a river by a large green hill and valley" src="https://images.unsplash.com/photo-1466872732082-8966b5959296?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=379&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 258px;"></div><div class="bQJ8Z"><a title="View the photo by Koushik C" class="_23lr1" href="/photos/JT8IWAaxpQk"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img src="https://images.unsplash.com/photo-1468103933896-2c34a78104c2?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=379&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 258px;"></div><div class="bQJ8Z"><a title="View the photo by Wil Stewart" class="_23lr1" href="/photos/QYFTkPFqzv4"></a></div></div></div>
    #                  <div class="_1pn7R" data-test="photo-component"><div class="_3vgBX"><div class=""><img alt="The sky full of stars with blue and pink hues over the rock formations." src="https://images.unsplash.com/photo-1497294815431-9365093b7331?dpr=2&amp;auto=format&amp;fit=crop&amp;w=568&amp;h=379&amp;q=60&amp;cs=tinysrgb" class="KW7g_ _1hz5D" style="width: 100%; height: 258px;"></div><div class="bQJ8Z"><a title="View the photo by Pawel Nolbert" class="_23lr1" href="/photos/62OK9xwVA0c"></a></div></div></div>
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
    for item in datas:
        if item['time']+'-'+item['name']+'.jpg' in fileNames:
            print('图片已存在')
        else:
            saveImg(item['img'],item['time']+'-'+item['name'])


