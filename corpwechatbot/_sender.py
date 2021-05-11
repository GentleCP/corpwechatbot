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
import configparser
from pathlib import Path
from abc import abstractmethod, ABC
from queue import Queue
from configparser import ConfigParser
from cptools import LogHandler

from corpwechatbot.error import KeyConfigError, MethodNotImplementedError
from corpwechatbot.util import Singleton

KEY_PATH = Path.home().joinpath('.corpwechatbot_key')


class Sender(ABC):
    '''
    Abstract class of sender, define the interface of all the senders
    '''

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
    def send_voice(self, *args, **kwargs):
        '''
        发送语音消息
        '''


    @abstractmethod
    def send_video(self, *args, **kwargs):
        '''
        发送视频消息
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
    def send_card(self, *args, **kwargs):
        '''
        发送卡片消息
        '''


    @abstractmethod
    def send_taskcard(self, *args, **kwargs):
        '''
        发送卡片消息
        '''


class MsgSender(Sender, Singleton):
    """
    The parent class of all the notify classes
    """

    def __init__(self, *args, **kwargs):
        super(MsgSender, self).__init__()
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
        self._media_api = ''
        self.key_cfg = ConfigParser()

    def send_text(self, *args,**kwargs):
        '''
        send text message
        :return:
        '''
        raise MethodNotImplementedError


    def send_image(self, *args, **kwargs):
        '''
        send image message
        :return:
        '''
        raise MethodNotImplementedError


    def send_voice(self, *args, **kwargs):
        '''
        发送语音消息
        '''
        raise MethodNotImplementedError


    def send_video(self, *args, **kwargs):
        '''
        发送视频消息
        '''
        raise MethodNotImplementedError


    def send_news(self, *args, **kwargs):
        '''
        send news
        :return:
        '''
        raise MethodNotImplementedError


    def send_markdown(self, *args, **kwargs):
        '''
        send markdown message
        :return:
        '''
        raise MethodNotImplementedError


    def send_file(self, *args, **kwargs):
        '''
        send file
        :return:
        '''
        raise MethodNotImplementedError



    def send_card(self, *args, **kwargs):
        '''
        发送卡片消息
        '''
        raise MethodNotImplementedError


    def send_taskcard(self, *args, **kwargs):
        '''
        发送卡片消息
        '''
        raise MethodNotImplementedError


    def _get_corpkeys(self, **kwargs):
        '''
        当没有直接传入keys时，尝试从本地文件`$HOME/.corpwechatbot_key`获取
        :param kwargs:
        :return:
        '''
        def get_local_keys(section:str, options:[]):
            self.logger.debug('You have not deliver a key parameter, try to get it from local files')
            if KEY_PATH.is_file():
                self.key_cfg.read(KEY_PATH)
                try:
                    for option in options:
                        yield self.key_cfg.get(section, option)
                except (configparser.NoSectionError,configparser.NoOptionError) as e:
                    raise KeyConfigError
            else:
                raise FileNotFoundError(f'Can not find file `{KEY_PATH}`')

        if 'key' in kwargs.keys():
            # chatbot settings
            if kwargs.get('key'):
                return {
                    'key': kwargs.get('key')
                }
            else:
                return {
                    'key' : next(get_local_keys(section='chatbot', options=['key']))
                }
        elif 'corpid' in kwargs.keys() or 'corpsecret' in kwargs.keys() or 'agentid' in kwargs.keys() :
            corpid, corpsecret, agentid = kwargs.get('corpid',''), kwargs.get('corpsecret',''),kwargs.get('agentid','')
            if corpid and corpsecret and agentid:
                return {
                    'corpid' : corpid,
                    'corpsecret': corpsecret,
                    'agentid': agentid,
                }
            else:
                res = {}
                options = ['corpid', 'corpsecret', 'agentid']
                for k,v in zip(options, get_local_keys(section='app', options=options)):
                    res.update({k: v})
                return res


    def _get_media_id_or_None(self,
                              media_type:str,
                              p_media:Path):
        '''
        获取media id，微信要求文件先上传到其后端服务器，再获取相应media id
        :param media_type:
        :param p_media:
        :return:
        '''
        files = {
            (None, (p_media.name, p_media.open('rb'), f'{media_type}/{p_media.suffix[1:]}'))
        }
        res = requests.post(self._media_api, files=files).json()
        if res.get('errcode') == 0:
            self.logger.debug("media_id获取成功")
            return res.get('media_id')
        else:
            self.logger.error(f"media_id获取失败，原因:{res.get('errmsg')}")
            return None


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

