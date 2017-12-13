# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests, re

__author__ = 'Hem1ng'


class Ticket(object):
    def __init__(self):
        self.trainId = ''
        self.originalStation = ''
        self.terminalStation = ''
        self.onStation = ''
        self.offStation = ''
        self.travelTime = ''
        self.arrivalTime = ''
        self.durationTimeH = ''
        self.durationTimeM = ''
        self.seat_SW = ''
        self.seat_YD = ''
        self.seat_ED = ''
        self.seat_SRW = ''
        self.seat_RW = ''
        self.seat_DW = ''
        self.seat_YW = ''
        self.seat_R = ''
        self.seat_Y = ''
        self.seat_W = ''
        self.seat_O = ''

    def __repr__(self):
        return '%s    %s    %s    %s    %s    %s' %(self.trainId,self.onStation,self.offStation,self.travelTime,self.arrivalTime,self.durationTimeH)

# 获取所有站点的code
def getAllStationCode():
    response = requests.get('https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9035')
    # 由于是js代码，所以要截取 var station_names ='@bjb|北京北...';
    originalString = response.text.split('=')[1]
    # 去掉最后面的;然后使用正则提取站点名和对应的编码
    group = re.findall('@(.+?)\|(.+?)\|(.+?)\|(.+?)\|(.+?)\|(.+?)', originalString[:-1])
    allStation = {item[1]:item[2] for item in group}
    return allStation

# 历时转换成分钟用于筛选
def convertDurationTimeToMinutes(duration):
    if not isinstance(duration, str):
        raise TypeError
    duration_list = duration.split(':')
    if len(duration_list) >= 2:
        return int(duration_list[0])*60+int(duration_list[1])


'''
    列名              索引
    车次               3
    始发站             4
    终点站             5
    出发站             6
    到达站             7
    出发时间           8
    到达时间           9
    历时              10
    商务座/特等座      32
    一等座            31
    二等座            30
    高级软卧          21
    软卧             23
    动卧             33
    硬卧             28
    软座             24
    硬座             29
    无座             26
    其他             22
    备注             1
'''
# 获取所有火车票信息
#        date: 购票日期      字符串类型  2017-12-12
# fromStation: 出发站代号    字符串类型  AOH
#   toStation: 目的站代号    字符串类型  NKH
#        type: 成人票|学生票 字符串类型  ADULT|0x00

def getAllTicketInfo(date, fromStation, toStation, type):
    response = requests.get(
        'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date='+date+'&leftTicketDTO.from_station='+fromStation+'&leftTicketDTO.to_station='+toStation+'&purpose_codes='+type)
    data = response.json()
    results = data['data']['result']
    ticketList = []
    for item in results:
        item_list = item.split('|')

        ticket = Ticket()
        ticket.trainId = item_list[3]
        ticket.originalStation = item_list[4]
        ticket.terminalStation = item_list[5]
        ticket.onStation = item_list[6]
        ticket.offStation = item_list[7]
        ticket.travelTime = item_list[8]
        ticket.arrivalTime = item_list[9]
        ticket.durationTimeH = item_list[10]
        ticket.durationTimeM = convertDurationTimeToMinutes(item_list[10])
        ticket.seat_SW = item_list[32]
        ticket.seat_YD = item_list[31]
        ticket.seat_ED = item_list[30]
        ticket.seat_SRW = item_list[21]
        ticket.seat_RW = item_list[23]
        ticket.seat_DW = item_list[33]
        ticket.seat_YW = item_list[28]
        ticket.seat_R = item_list[24]
        ticket.seat_Y = item_list[29]
        ticket.seat_W = item_list[26]
        ticket.seat_O = item_list[22]

        ticketList.append(ticket)
        
    return ticketList

# 从出发站到目的站
def getSelectedTicket(*, onStation, offStation):
    selectedTicketList = []
    for ticket in getAllTicketInfo('2017-12-14','AOH','NKH','ADULT'):
        if not onStation:
            onStation = 'AOH'
        if not offStation:
            offStation = 'NKH'
        if ticket.onStation == onStation and ticket.offStation == offStation:
            selectedTicketList.append(ticket)
    return selectedTicketList

# 根据历时筛选
def getDurationTicket(*, duration):
    if not isinstance(duration, int):
        raise TypeError
    durationTicketList = []
    for ticket in getSelectedTicket(onStation='AOH', offStation='NKH'):
        if int(ticket.durationTimeM) <= duration:
            durationTicketList.append(ticket)
    return durationTicketList

print('车次    出发站    到达站    出发时间    到达时间    历时')
for t in getDurationTicket(duration=60):
    print(t)