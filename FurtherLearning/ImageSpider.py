# !/usr/bin/env python3
# -*- coding: utf-8 -*-

__author = 'Hem1ng'

import os, requests, time, queue, threading
from multiprocessing.pool import Pool
from functools import partial
from bs4 import BeautifulSoup
from pathlib import Path

# 爬虫爬取的原始url
ORIGINAL_URL = 'http://desk.zol.com.cn/youxi/yingxionglianmeng/'
# 网页的域名
HOST_URL = 'http://desk.zol.com.cn'
# 图片下载路径
DOWNLOAD_PATH = os.path.join(os.path.expanduser(r'~/Downloads'), 'Temp')


# ******************** 公共方法 ********************

# 设置图片下载路径
def setImageDownloadPath(path):
    # 构造路径
    downloadPath = Path(path)
    # 如果路径不存在则创建路径
    if not downloadPath.exists():
        downloadPath.mkdir()
    os.chdir(path)

# 图片是否需要下载
def isDownloadImage(url):
    return checkImageIsDownloaded(url)

# 检测图片是否已经下载
def checkImageIsDownloaded(path, url):
    image_name = os.path.basename(url)
    fileNames = os.listdir(path)
    # 如果文件名不存在则需要下载图片
    if not image_name in fileNames:
        return True
    else:
        return False

# 下载图片
def downloadImage(url):
    # 以路径的最后一部分作为图片的名字
    image_name = '{}'.format(os.path.basename(url))
    image = requests.get(url)
    with open(image_name,'wb') as f:
        f.write(image.content)

# *********** 爬取LOL壁纸下载链接并下载图片 ***********

class ImageSpider(object):

    def __init__(self):
        self.__image_links__ = []

    # 获取html页面内容
    def __get_htmlContent__(self, url):
        resp = requests.get(url)
        if resp.status_code == 200:
            try:
                content = resp.content.decode('gbk')
            except Exception:
                content = resp.content.decode('utf-8')
            return content

    # 获取所有html页面链接
    def __get_htmlLinks__(self, url):
        html_content = self.__get_htmlContent__(url)
        html_links = self.__parse_htmlLinks__(html_content)
        return html_links

    # 解析html网页内容以获取网页链接
    def __parse_htmlLinks__(self, htmlContent):
        soup = BeautifulSoup(htmlContent, 'lxml')
        all_li = soup.find_all('li', class_='photo-list-padding')
        html_links = []
        for li in all_li:
            a = li.find('a')
            html_links.append(HOST_URL+a['href'])
        return html_links

    # 获取所有图片的下载链接
    def __get_imageLinks__(self, url):
        html_content = self.__get_htmlContent__(url)
        self.__parse_imageLinkAndNextPageUrl__(html_content)

    # 解析html网页内容以获取图片链接
    def __parse_imageLinkAndNextPageUrl__(self, htmlContent):
        soup = BeautifulSoup(htmlContent, 'lxml')
        img = soup.find('img', id='bigImg')
        self.__image_links__.append(img['src'])
        a = soup.find('a', id='pageNext')
        if not a['href'] == 'javascript:;':
            temp_url = HOST_URL+a['href']
            self.__get_imageLinks__(temp_url)

    # 爬虫开始爬取
    def start_spider(self):
        time_start = time.time()
        print('页面爬取开始...')
        # 获取所有html链接
        html_links = self.__get_htmlLinks__(ORIGINAL_URL)
        print('解析图片链接...')
        # 获取所有图片下载链接
        for link in html_links:
            self.__get_imageLinks__(link)
        print('开始下载图片...')
        # 设置图片下载路径
        setImageDownloadPath(DOWNLOAD_PATH)

        # '''
        # ********** 多线程 ***********
        q = queue.Queue()
        for x in range(4):
            worker = DownloadWorker(q)
            # daemon=True是将线程设置为守护线程，也就是说如果主线程退出，则所有守护线程也会退出
            # daemon=False是将线程设置为非守护线程，也就是说非守护线程退出后主线程才会退出，即主线程的退出依赖于非守护线程的退出
            # *********** 测试实例 **************
            # 注释倒数第二或第三行代码观察效果
            # def func():
            #     time.sleep(5)
            #     print("finish")
            # threading.Thread(target=func).start()
            # threading.Thread(target=func, daemon=True).start()
            # print('aaa')
            # **********************************
            worker.daemon = True
            worker.start()
        # '''

        # '''
        # ********* 单线程、多线程公共部分 *********
        for url in self.__image_links__:
            # 检验是否需要下载图片
            if isDownloadImage(url):
        #********** 单线程 ***************
                # 单线程下载大约127s，请注意花费的时间因网络状况、快慢等不同会有所差异
                # downloadImage(url)
        # '''

        # '''
        # ********* 多线程 ***************
                # 多线程下载大约54秒，因为GIL的限制，同一时间仍然只有一个线程在执行，所以代码只是并发执行而不是并行执行。
                # 其比单线程下载更快的原因是因为下载图片是IO密集型的操作，当下载图片时处理器便空闲了下来，可以切换到其他线程继续执行，处理器花费的时间主要在等待网络连接上。
                q.put(url)
        q.join()
        # '''

        '''
        # *********** 多进程 **************
        # 多进程下载大约66秒，本事例当中多线程和多进程应该差不多时间，因为网络原因可能会有所差异
        # 如果你的代码是IO密集型的，选择Python的多线程和多进程差别可能不会太大，多进程可能比多线程更易使用，但需要消耗更大的内存。
        # 如果你的代码是CPU密集型的，那么多进程可能是不二选择，特别是对具有多个处理器的的机器而言。
        download = partial(downloadImage)
        with Pool(4) as p:
            p.map(download, self.__image_links__)
        '''

        print('共下载%s张图片'%len(self.__image_links__))
        time_end = time.time()
        print('共耗时',time_end - time_start)

# ************** 多线程下载图片 *******************

class DownloadWorker(threading.Thread):

    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            item = self.queue.get()
            if item is None:
                break
            url = item
            downloadImage(url)
            self.queue.task_done()


if __name__ == '__main__':

    imgSpider = ImageSpider()
    imgSpider.start_spider()


