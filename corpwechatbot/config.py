#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------File Info-----------------------
Name: config.py
Description:
Author: GentleCP
Email: me@gentlecp.com
Create Date: 8/4/2021 
-----------------End-----------------------------
"""

OFFICIAL_APIS = {
    'GET_ACCESS_TOKEN': '/cgi-bin/gettoken?corpid={}&corpsecret={}',
    'MESSAGE_SEND': '/cgi-bin/message/send?access_token={}',
    'APPCHAT_CREATE': '/cgi-bin/appchat/create?access_token={}',
    'APPCHAT_SEND': '/cgi-bin/appchat/send?access_token={}',
    'MEDIA_UPLOAD': '/cgi-bin/media/upload?access_token={}&type={}',

    'WEBHOOK_SEND': '/cgi-bin/webhook/send?key={}',
    'WEBHOOK_MEDIA_UPLOAD': '/cgi-bin/webhook/upload_media?key={}&type=file'
}