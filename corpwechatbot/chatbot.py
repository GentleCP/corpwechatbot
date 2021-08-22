#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
-----------------File Info-----------------------
            Name: chatbot.py
            Description: 企业微信机器人主体
            Author: GentleCP
            Email: me@gentlecp.com
            WebSite: https://www.gentlecp.com
            Create Date: 2021/4/6 
-----------------End-----------------------------
"""
import base64
from pathlib import Path
from hashlib import md5
from typing import Optional
from cptools import LogHandler

from corpwechatbot.util import is_image, is_file
from corpwechatbot._sender import MsgSender
from corpwechatbot.config import OFFICIAL_APIS


class CorpWechatBot(MsgSender):
    """
    企业微信机器人，支持文本、markdown、图片、图文、文件类型数据的发送
    """

    def __init__(self,
                 key: str = '',
                 log_level: int = 20):
        super().__init__(log_level)
        self.key = self._get_corpkeys(key=key).get('key', '')
        self.headers = {'Content-Type': 'application/json; charset=utf-8'}
        self.webhook_send_api = self.base_url.format(OFFICIAL_APIS['WEBHOOK_SEND'].format(self.key))
        self._media_api = self.base_url.format(OFFICIAL_APIS['WEBHOOK_MEDIA_UPLOAD'].format(self.key))

    def _get_corpkeys(self, key: str = ''):
        '''
        get key from parameter or local
        :param key:
        :return:
        '''
        if key:
            return {
                'key': key
            }
        return {
            'key': next(self._get_local_keys(section='chatbot', options=['key']))
        }

    def _send(self,
              msg_type: str = '',
              data: dict = {},
              media_path: Optional[str] = '',
              **kwargs):
        '''
        :param msg_type:
        :param data:
        :param media_path:
        :return:
        '''
        data['msgtype'] = msg_type
        if msg_type == 'image':
            img_content = Path(media_path).open('rb').read()
            img_base64 = base64.b64encode(img_content).decode()
            img_md5 = md5(img_content).hexdigest()
            data['image']['base64'] = img_base64
            data['image']['md5'] = img_md5
        elif msg_type == 'markdown':
            md_path = Path(data['markdown']['content'])
            if md_path.is_file():
                data['markdown']['content'] = md_path.read_text()
        elif msg_type == 'file':
            media_res = self._get_media_id(media_type='file', p_media=Path(media_path))
            data[msg_type]['media_id'] = media_res.get('media_id', '')
        return self._post(self.webhook_send_api, data)

    def send_text(self, content, mentioned_list=[], mentioned_mobile_list=[]):
        '''
        发送文本消息，
        :param content: 文本内容，最长不能超过2048字节，utf-8编码
        :param mentioned_list: userid列表，提醒群众某个成员，userid通过企业通讯录查看，'@all'则提醒所有人
        :param mentioned_mobile_list: 手机号列表，提醒手机号对应的成员，'@all'代表所有人，当不清楚userid时可替换
        :return: 消息发送结果
        '''
        if not content:
            self.logger.error(self.errmsgs['text_error'])
            return {
                'errcode': 404,
                'errmsg': self.errmsgs['text_error']
            }
        data = {
            "text": {
                "content": content,
                "mentioned_list": mentioned_list,
                "mentioned_mobile_list": mentioned_mobile_list
            }
        }
        return self._send(msg_type='text', data=data)

    def send_image(self, image_path=''):
        '''
        发送图片类型，限制大小2M，支持JPG，PNG格式
        :param image_path: 图片文件路径
        :return: result
        '''
        if not is_image(image_path):
            self.logger.error(self.errmsgs['image_error'])
            return {
                'errcode': 404,
                'errmsg': self.errmsgs['image_error']
            }
        data = {
            "image": {
                "base64": '',
                "md5": '',
            }
        }
        return self._send(msg_type='image', data=data, media_path=image_path)

    def send_news(self, title='', desp='', url='', picurl=''):
        '''
        发送图文消息
        :param title: 图文标题，不超过128个字节，超过会自动截断
        :param desp: 图文描述，可选，不超过512个字节，超过会自动截断
        :param url: 跳转链接
        :param picurl: 图片url，支持JPG、PNG格式，较好的效果为大图 1068*455，小图150*150。
        :return:
        '''
        if not (title and url):
            self.logger.error(self.errmsgs['news_error'])
            return {
                'errcode': 404,
                'errmsg': self.errmsgs['news_error']
            }
        data = {
            "news": {
                "articles": [
                    {
                        "title": title,
                        "description": desp,
                        "url": url,
                        "picurl": picurl
                    }
                ]
            }
        }
        return self._send(msg_type='news', data=data)

    def send_markdown(self, content=''):
        '''
        发送markdown类型数据，支持markdown语法
        :param content: mardkown原始数据或markdown文件路径
        :return: 消息发送结果
        '''
        if not content:
            self.logger.error(self.errmsgs['markdown_error'])
            return {
                'errcode': 404,
                'errmsg': self.errmsgs['markdown_error']
            }
        data = {
            "markdown": {
                "content": content
            }
        }
        return self._send(msg_type='markdown', data=data)

    def send_file(self, file_path: str):
        '''
        发送文件
        :param file_path:
        :return:
        '''
        if not is_file(file_path):
            self.logger.error(self.errmsgs['file_error'])
            return {
                'errcode': 404,
                'errmsg': self.errmsgs['file_error']
            }
        data = {
            "file": {
                "media_id": '',
            }
        }
        return self._send(msg_type='file', data=data, media_path=file_path)

if __name__ == "__main__":
    bot = CorpWechatBot(log_level=20)
    bot.send_text('123')