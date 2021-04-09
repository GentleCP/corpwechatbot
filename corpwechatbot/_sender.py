#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
-----------------File Info-----------------------
            Name: _sender.py
            Description:
            Author: GentleCP
            Email: 574881148@qq.com
            WebSite: https://blog.gentlecp.com
            Create Date: 2021/4/8 
-----------------End-----------------------------
"""
import requests
import json
import time
from pathlib import Path
from abc import abstractmethod
from queue import Queue

from cptools import LogHandler


class NetworkError(Exception):
    """
    Network 请求
    """
    def __init__(self, errmsg='网络连接异常'):
        self.errmsg = errmsg

    def __str__(self):
        return self.errmsg

class MediaGetError(Exception):
    """
    media_id获取异常
    """
    def __init__(self, errmsg='media_id获取异常'):
        self.errmsg = errmsg

    def __str__(self):
        return self.errmsg

class TokenGetError(Exception):
    """
    token 获取失败异常
    """
    def __init__(self, errmsg='token请求失败'):
        self.errmsg = errmsg

    def __str__(self):
        return self.errmsg

class MsgSender(object):
    """
    The parent class of all the notify objects
    """
    def __init__(self, **kwargs):
        self.logger = LogHandler('MsgSender')
        self.queue = Queue(20)  # 官方限制每分钟20条消息
        self._webhook = None
        self.headers = None
        self.errmsgs = {
            'imageerror': '图片文件不合法',
            'texterror': '文本消息不合法',
            'newserror': '图文消息内容不合法',
            'markdownerror': 'markdown内容不合法',
            'voiceerror': '语音文件不合法',
            'videoerror': '视频文件不合法',
            'fileerror': '文件不合法',
            'carderror': '卡片消息不合法',
            'mediaerror': 'media_id获取失败',
        }

    @abstractmethod
    def send_text(self, *args,**kwargs):
        '''
        send text message
        :return:
        '''

    @abstractmethod
    def send_image(self, *args, **kwargs):
        '''
        send image message
        :return:
        '''


    @abstractmethod
    def send_news(self, *args, **kwargs):
        '''
        send news
        :return:
        '''


    @abstractmethod
    def send_markdown(self, *args, **kwargs):
        '''
        send markdown message
        :return:
        '''


    @abstractmethod
    def send_file(self, *args, **kwargs):
        '''
        send file
        :return:
        '''

    @abstractmethod
    def _get_media_id_or_None(self,
                              media_type:str,
                              p_media:Path):
        '''
        获取media id，微信要求文件先上传到其后端服务器，再获取相应media id
        :param media_type:
        :param p_media:
        :return:
        '''

    def _post(self, data):
        '''
        发送消息统一方法，要求utf-8编码，该方法在MsgSender中实现，但不可通过该抽象类进行调用
        :param data: 传输的数据字典
        :return: 消息发送成功与否
        '''
        now = time.time()
        self.queue.put(now)
        if self.queue.full():
            # 限制每分钟20条消息，当队列满时检验当前与队列头部时间差值，若小于1分钟，则进行睡眠等待
            interval_time = now - self.queue.get()
            if interval_time < 60:
                sleep_time = int(60 - interval_time) + 1
                self.logger.debug(f'机器人每分钟限制20条消息，当前已超出限制，需等待{sleep_time}s')
                time.sleep(sleep_time)
        try:
            post_data = json.dumps(data)
            response = requests.post(self._webhook, headers=self.headers, data=post_data)
        except requests.exceptions.HTTPError as exc:
            self.logger.error(f"发送失败， HTTP error:{exc.response.status_code} , 原因: {exc.response.reason}")
            raise
        except requests.exceptions.ConnectionError:
            self.logger.error("发送失败，HTTP connection error!")
            raise
        except requests.exceptions.Timeout:
            self.logger.error("发送失败，Timeout error!")
            raise
        except requests.exceptions.RequestException:
            self.logger.error("发送失败, Request Exception!")
            raise
        else:
            try:
                result = response.json()
            except json.decoder.JSONDecodeError:
                self.logger.error(f"服务器响应异常，状态码：{response.status_code}，响应内容：{response.text}")
                return result
            else:
                if result.get('errcode') == 0:
                    # 发送正常
                    self.logger.info('发送成功!')
                    return result
                else:
                    self.logger.error(f"发送失败!，原因：{result['errmsg']}")
                    return result

