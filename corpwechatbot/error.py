#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
-----------------File Info-----------------------
            Name: error.py
            Description:
            Author: GentleCP
            Email: 574881148@qq.com
            WebSite: https://blog.gentlecp.com
            Create Date: 2021/4/24 
-----------------End-----------------------------
"""
from pathlib import Path
KEY_PATH = Path.home().joinpath('.corpwechatbot_key')

class NetworkError(Exception):

    def __str__(self):
        return '网络连接异常'


class MediaGetError(Exception):

    def __str__(self):
        return 'media_id获取异常'


class TokenGetError(Exception):

    def __init__(self, errmsg='token请求失败'):
        self.errmsg = errmsg

    def __str__(self):
        return self.errmsg


class MethodNotImplementedError(Exception):

    def __str__(self):
        return 'This method has not been implemented yet, your are not able to use it right now'


class KeyConfigError(Exception):

    def __str__(self):
        return f'Can not get the keys from {KEY_PATH}, make sure you have set the correct sections and options'