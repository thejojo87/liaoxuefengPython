#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Thejojo'

'默认配置文件'

configs = {
    'db': {     # 定义数据库相关信息
        'host': '127.0.0.1',
        'port': 3307,
        'user': 'www-data',
        'password': 'www-data',
        'database': 'awesome'
    },
    'session': {
        'secret': 'thejojo'
    }
}