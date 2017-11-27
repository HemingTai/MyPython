#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Hem1ng'

# 如果要部署到服务器时，通常需要修改数据库的host等信息，直接修改config_default.py不是一个好办法，更好的方法是编写一个config_override.py，用来覆盖某些默认设置
# 把config_default.py作为开发环境的标准配置，把config_override.py作为生产环境的标准配置，我们就可以既方便地在本地开发，又可以随时把应用部署到服务器上。
configs = {
    'runPort': 9000,
    'database': {
        'host': '127.0.0.1'
    }
}