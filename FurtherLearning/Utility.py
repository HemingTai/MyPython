# !/usr/bin/env python3
# -*- coding: utf-8 -*-

__author = 'Hem1ng'


import os, requests
from pathlib import Path
from contextlib import closing

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
    with closing(requests.get(url, stream=True)) as r:
        video_name = os.path.basename(url)
        chunk_size = 1024*1024
        content_size = int(r.headers['content-length'])
        totalCount = 0
        with open(video_name, 'wb') as f:
            for data in r.iter_content(chunk_size=chunk_size):
                f.write(data)
                totalCount += len(data)
                print('正在下载%.4f%%' % (totalCount / content_size)*100)