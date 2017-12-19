# !/usr/bin/env python
# -*- coding: utf-8 -*-

import re, http.cookiejar, os, ssl
from urllib import parse, request


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

    def abc(self, a, b, c):
        '''''回调函数 
        @a:已经下载的数据块 
        @b:数据块的大小 
        @c:远程文件的大小 
        '''
        per = 100.0 * a * b / c
        if per > 100:
            per = 100
        print ('%.2f%%' % per)

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


if __name__ == '__main__':
    # ************** 电影Top100 *************** #
    mySpider = DouBanSpider()
    print('豆瓣电影爬取开始...')
    mySpider.start_spider()
    print('豆瓣电影爬取结束...')

    # **************《猎场热门影评》*************** #
    # reviewSpider = ReviewSpider()
    # reviewSpider.start_spider()
