# !/usr/bin/env python3
# -*- coding: utf-8 -*-

__author = 'Hem1ng'


import os, requests
from pathlib import Path
from contextlib import closing
import mysql.connector

# 默认文件下载路径
DOWNLOAD_PATH = os.path.join(os.path.expanduser(r'~/Downloads'), 'Temp')
SAVE_PATH = os.path.join(os.path.abspath('.'), 'Temp61_70.html')

# ******************** 公共方法 ********************

# 设置文件下载路径
def setFileDownloadPath(path=DOWNLOAD_PATH):
    # 构造路径
    downloadPath = Path(path)
    # 如果路径不存在则创建路径
    if not downloadPath.exists():
        downloadPath.mkdir()
    os.chdir(path)

# 文件是否需要下载
def isFileNeededDownload(url):
    return checkFileIsDownloaded(url)

# 检测文件是否已经下载
def checkFileIsDownloaded(url, path=DOWNLOAD_PATH):
    file_name = os.path.basename(url)
    file_Names = os.listdir(path)
    # 如果文件名不存在则需要下载
    if not file_name in file_Names:
        return True
    else:
        return False

# 下载文件
def downloadFile(url):
    # 以路径的最后一部分作为文件的名字
    file_name = '{}'.format(os.path.basename(url))
    file = requests.get(url)
    with open(file_name,'wb') as f:
        f.write(file.content)

# 保存文件
def saveFile(path,data):
    with open(path, 'w') as f:
        f.write(data)

# 下载视频
def downloadVideo(url):
    if isFileNeededDownload(url):
        with closing(requests.get(url, stream=True)) as r:
            video_name = os.path.basename(url)
            chunk_size = 1024*1024
            content_size = int(r.headers['content-length'])
            totalCount = 0
            with open(video_name, 'wb') as f:
                for data in r.iter_content(chunk_size=chunk_size):
                    f.write(data)
                    totalCount += len(data)
                    currentCount = '%.4f' % (totalCount / content_size)
                    print('正在下载%.2f%%' % (float(currentCount)*100))
    else:
        print('视频已下载')

# 保存数据至数据库
def saveDataToDatabase(data):
    conn = mysql.connector.connect(user='root',password='99112911',database='Video')
    cur = conn.cursor()
    # 执行INSERT等操作后要调用commit()提交事务
    # MySQL的SQL占位符是%s
    if not isinstance(data, list):
        raise TypeError('type of data must be list')
    for item in data:
        cur.execute('insert into t_video (category, title, url) values (%s, %s, %s)', ('国产', item['title'], item['url']))
        if cur.rowcount > 0:
            print('插入数据成功...')
    conn.commit()
    cur.close()
    conn.close()

# 查询数据库数据
def queryDataFromDatabse():
    conn = mysql.connector.connect(user='root', password='99112911', database='Video')
    cur = conn.cursor()
    # cur.execute('select * from t_video where id = %s', ('1',))
    value = cur.fetchall()
    print(value)
    cur.close()
    conn.close()
