#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Hem1ng'

'''
    url handlers
'''

# import re, time, json, logging, hashlib, base64, asyncio
from BBS_WebApp_Python.www.coroweb import get, post
from BBS_WebApp_Python.www.ormmodel import User, Comment, Blog, next_id

@get('/')
async def index(request):
    users = await User.findAll()
    return {
        '__template__':'templates/test.html',
        'users':users
    }