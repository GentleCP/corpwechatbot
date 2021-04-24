#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
-----------------File Info-----------------------
            Name: __init__.py.py
            Description:
            Author: GentleCP
            Email: 574881148@qq.com
            WebSite: https://www.gentlecp.com
            Create Date: 2021/4/6 
-----------------End-----------------------------
"""

from .__about__ import __name__, __description__, __url__, __version__
from .__about__ import __author__, __author_email__, __license__

from .chatbot import CorpWechatBot
from .app import AppMsgSender