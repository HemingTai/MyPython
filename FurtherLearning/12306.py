# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests, re
from enum import Enum

__author__ = 'Hem1ng'


class Ticket(object):
    def __init__(self):
        self.trainId = ''               # 车次
        self.originalStationCode = ''   # 始发站编码
        self.originalStationName = ''   # 始发站名称
        self.terminalStationCode = ''   # 终点站编码
        self.terminalStationName = ''   # 终点站名称
        self.onStationCode = ''         # 出发站编码
        self.onStationName = ''         # 出发站名称
        self.offStationCode = ''        # 到达站编码
        self.offStationName = ''        # 到达站名称
        self.travelTime = ''            # 出发时间
        self.arrivalTime = ''           # 到达时间
        self.durationTimeH = ''         # 历时(小时)
        self.durationTimeM = ''         # 历时(分钟)
        self.seat_SW = ''               # 商务座|特等座
        self.seat_YD = ''               # 一等座
        self.seat_ED = ''               # 二等座
        self.seat_SRW = ''              # 高级软卧
        self.seat_RW = ''               # 软卧
        self.seat_DW = ''               # 动卧
        self.seat_YW = ''               # 硬卧
        self.seat_R = ''                # 软座
        self.seat_Y = ''                # 硬座
        self.seat_W = ''                # 无座
        self.seat_O = ''                # 其他

    def __repr__(self):
        return '车次：%s 出发站：%s 到达站：%s 出发时间：%s 到达时间：%s 历时：%s 二等座：%s\n' %(self.trainId,self.onStationName,self.offStationName,self.travelTime,self.arrivalTime,self.durationTimeH,self.seat_ED)

ALLSTATIONCODE = None
ALLSTATIONNAME = None
ALLType = {'普通票':'ADULT','成人票':'ADULT','学生票':'0x00'}
SEAT = Enum('SEAT',('SW','YD','ED','SRW','RW','DW','YW','R','Y','W','O'))

# 获取所有站点的code
def getAllStationCode():
    response = requests.get('https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9035')
    # 由于是js代码，所以要截取 var station_names ='@bjb|北京北...';
    originalString = response.text.split('=')[1]
    # 去掉最后面的;然后使用正则提取站点名和对应的编码
    group = re.findall('@(.+?)\|(.+?)\|(.+?)\|(.+?)\|(.+?)\|(.+?)', originalString[:-1])
    global ALLSTATIONCODE, ALLSTATIONNAME
    ALLSTATIONCODE = {item[1]:item[2] for item in group}
    ALLSTATIONNAME = {item[2]:item[1] for item in group}
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
def getAllTicketInfo(*, date, fromStation, toStation, ticketType='ADULT'):
    if not ALLSTATIONCODE or not ALLSTATIONNAME or not ALLType:
        raise ValueError
    if not date or not fromStation or not toStation or not ticketType:
        raise ValueError
    response = requests.get('https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date='+date+'&leftTicketDTO.from_station='+fromStation+'&leftTicketDTO.to_station='+toStation+'&purpose_codes='+ticketType)
    data = response.json()
    results = data['data']['result']
    ticketList = []
    for item in results:
        item_list = item.split('|')

        ticket = Ticket()
        ticket.trainId = item_list[3]
        ticket.originalStationCode = item_list[4]
        ticket.originalStationName = ALLSTATIONNAME[item_list[4]]
        ticket.terminalStationCode = item_list[5]
        ticket.terminalStationName = ALLSTATIONNAME[item_list[5]]
        ticket.onStationCode = item_list[6]
        ticket.onStationName = ALLSTATIONNAME[item_list[6]]
        ticket.offStationCode = item_list[7]
        ticket.offStationName = ALLSTATIONNAME[item_list[7]]
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
def getSelectedTicket(*, date, onStation, offStation, ticketType='ADULT'):
    selectedTicketList = []
    for ticket in getAllTicketInfo(date=date,fromStation=onStation,toStation=offStation, ticketType=ticketType):
        if ticket.onStationCode == onStation and ticket.offStationCode == offStation:
            selectedTicketList.append(ticket)
    return selectedTicketList

# 根据历时筛选
def getDurationTicket(*, date, duration, onStation, offStation, ticketType='ADULT'):
    if not isinstance(duration, int):
        raise TypeError
    durationTicketList = []
    for ticket in getSelectedTicket(date=date, onStation=onStation, offStation=offStation, ticketType=ticketType):
        if int(ticket.durationTimeM) <= duration:
            durationTicketList.append(ticket)
    return durationTicketList

# 根据座位筛选
def getSeatTicketList(*, date, duration, onStation, offStation, ticketType='ADULT', seatType=SEAT.ED):
    if not isinstance(seatType, SEAT):
        raise TypeError
    seatTicketList = []
    for ticket in getDurationTicket(date=date, duration=duration, onStation=onStation, offStation=offStation, ticketType=ticketType):
        if ticket.onStationCode == onStation and ticket.offStationCode == offStation:
            if seatType == SEAT.ED and ticket.seat_ED != '无' :
                if ticket.seat_ED == '有' or int(ticket.seat_ED) > 0:
                    seatTicketList.append(ticket)
    return seatTicketList

if __name__ == '__main__':
    date = '2018-09-20'
    departure = '上海虹桥'
    destination = '南昌西'
    departure_on = '上海虹桥'
    destination_off = '南昌西'
    ticketType = '成人票'
    duration = 180
    # 先获取所有站点code
    getAllStationCode()
    # 获取筛选出发站和到达站后的车次信息
    # selectedTicketList = getSelectedTicket(date=date, onStation=ALLSTATIONCODE[departure_on], offStation=ALLSTATIONCODE[destination_off], ticketType=ALLType[ticketType])
    # 获取筛选历时后的车次信息
    # durationTicketList = getDurationTicket(date=date,duration=duration, onStation=ALLSTATIONCODE[departure_on], offStation=ALLSTATIONCODE[destination_off], ticketType=ALLType[ticketType])
    # 获取筛选座位后的车次信息
    seatTicketList = getSeatTicketList(date=date, duration=duration, onStation=ALLSTATIONCODE[departure_on], offStation=ALLSTATIONCODE[destination_off], ticketType=ALLType[ticketType], seatType=SEAT.ED)
    print(seatTicketList)
