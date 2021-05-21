#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
-----------------File Info-----------------------
            Name: app.py
            Description: 企业微信应用消息推送
            Author: GentleCP
            Email: 574881148@qq.com
            WebSite: https://blog.gentlecp.com
            Create Date: 2021/4/7
-----------------End-----------------------------
"""
import time
import requests
import json
import hashlib
from typing import Optional
from pathlib import Path
from cptools import LogHandler

from corpwechatbot._sender import MsgSender
from corpwechatbot.error import TokenGetError, MethodNotImplementedError
from corpwechatbot.util import is_image, is_voice, is_video, is_file

CUR_PATH = Path(__file__)
TOKEN_PATH = CUR_PATH.parent.joinpath('token.json')  # 存储在本项目根目录下


class KeyNotFound(Exception):

    def __str__(self):
        return f'Can not find file `{str(Path.home())}/.corpwechatbot_key`'


class AppMsgSender(MsgSender):
    """
    应用消息推送器，支持文本、图片、语音、视频、文件、文本卡片、图文、markdown消息推送
    """

    def __init__(self,
                 corpid: str = '',
                 corpsecret: str = '',
                 agentid: str = ''):
        '''
        :param corpid: 企业id
        :param corpsecret: 应用密钥
        :param agentid: 应用id
        '''
        super().__init__()
        corpkeys = self._get_corpkeys(corpid=corpid, corpsecret=corpsecret, agentid=agentid)
        self._corpid = corpkeys.get('corpid', '')
        self._corpsecret = corpkeys.get('corpsecret', '')
        self._agentid = corpkeys.get('agentid', '')
        self._token_key = hashlib.sha1(bytes(self._corpid+self._agentid,encoding='utf-8')).hexdigest()

        self.access_token = self.get_assess_token()
        self._webhook = f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={self.access_token}'
        self.logger = LogHandler('AppMsgSender')

    def _get_corpkeys(self, corpid: str = '', corpsecret: str = '', agentid: str = ''):
        '''
        get keys for app from parameter or local
        :param corpid:
        :param corpsecret:
        :param agentid:
        :return:
        '''
        if corpid and corpsecret and agentid:
            return {
                'corpid': corpid,
                'corpsecret': corpsecret,
                'agentid': agentid,
            }
        else:
            # from local
            res = {}
            options = ['corpid', 'corpsecret', 'agentid']
            for k, v in zip(options, self._get_local_keys(section='app', options=options)):
                res.update({k: v})
            return res

    def get_assess_token(self):
        '''
        通过企业id和应用凭证密钥获取assess_token，用于消息推送，根据corpid和agentid识别不同的token
        '''
        try:
            token_dict = json.loads(TOKEN_PATH.read_text())
        except FileNotFoundError:
            # 尚未获取过token
            self.logger.debug('旧token获取失败，重新获取token')
            token_dict = {}
            return self._get_access_token(token_dict)
        else:
            try:
                token = token_dict[self._token_key]
            except KeyError:
                # 该agentid对应token不存在
                self.logger.debug("token不存在，获取token")
                return self._get_access_token(token_dict)
            else:
                now = time.time()
                if now - TOKEN_PATH.stat().st_mtime >= 2 * 3600:
                    self.logger.debug("token过期，重新获取token")
                    return self._get_access_token(token_dict)
                return token

    def _get_access_token(self, token_dict: {}):
        token_api = f'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={self._corpid}&corpsecret={self._corpsecret}'
        res = requests.get(token_api).json()
        if res.get('errcode') == 0:
            self.logger.info("token请求成功")
            token = res.get('access_token')
            token_dict.update({
                self._token_key: token
            })
            TOKEN_PATH.write_text(json.dumps(token_dict))
            return token
        else:
            raise TokenGetError(f"token请求失败，原因：{res.get('errmsg', 'None')}")

    def _list2str(self, datas: []):
        '''
        将传入的list数据转换成 | 划分的字符串
        e.g. ['user1', 'user2'] -> 'user1|user2'
        :param datas:
        :return:
        '''
        return "".join([item + '|' for item in datas])[:-1]

    def _send_media(self,
                    media_path: str,
                    media_type: str,
                    **kwargs):
        '''
        发送媒体文件统一发送模板
        :param media_path:
        :param media_type: 媒体类型，目前包括image, voice, video, file
        :param safe:
        :param kwargs: touser, toparty, totag
        :return:
        '''
        is_func = globals().get('is_' + media_type)  # 根据media类型，自动定位检测函数
        if not is_func(media_path):
            self.logger.error(self.errmsgs[f'{media_type}error'])
            return {
                'errcode': 404,
                'errmsg': self.errmsgs[f'{media_type}error']
            }
        else:
            # send media
            self._media_api = f'https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={self.access_token}&type={media_type}'
            media_id = self._get_media_id_or_None(media_type=media_type, p_media=Path(media_path))
            if media_id:
                if not (kwargs.get('touser') or kwargs.get('toparty') or kwargs.get('totag')):
                    # 三者均为空，默认发送全体成员
                    kwargs.update({'touser': ['@all']})
                data = {
                    "touser": self._list2str(kwargs.get('touser', [])),
                    "toparty": self._list2str(kwargs.get('toparty', [])),
                    "totag": self._list2str(kwargs.get('totag', [])),
                    "msgtype": media_type,
                    "agentid": self._agentid,
                    media_type: {
                        "media_id": media_id
                    },
                    "safe": kwargs.get('safe', 0)
                }
                return self._post(data)
            else:
                return {
                    'errcode': 405,
                    'errmsg': self.errmsgs['mediaerror']
                }

    def send_image(self,
                   image_path: str,
                   **kwargs):
        '''
        发送图片，支持jpg、png、bmp
        :param image_path: 图片存储路径
        :return:
        '''
        return self._send_media(media_path=image_path,
                                media_type='image',
                                **kwargs)

    def send_voice(self,
                   voice_path: str,
                   **kwargs):
        '''
        发送语音，2MB，播放长度不超过60s，仅支持AMR格式
        :param voice_path:
        :return:
        '''
        return self._send_media(media_path=voice_path,
                                media_type='voice',
                                **kwargs)

    def send_video(self,
                   video_path: str,
                   **kwargs):
        '''
        发送视频
        :param video_path:
        :return:
        '''
        return self._send_media(media_path=video_path,
                                media_type='video',
                                **kwargs)

    def send_file(self,
                  file_path: str,
                  **kwargs):
        '''
        发送文件
        :param file_path:
        :return:
        '''
        return self._send_media(media_path=file_path,
                                media_type='file',
                                **kwargs)

    def _send_content(self,
                      content_type: str,
                      data: dict,
                      **kwargs
                      ):
        '''
        除媒体文件外消息的统一发送模板
        :param content_type: 发送的数据类型
        :param data: 发送的数据独有字段
        :param kwargs: 特殊参数，包括touser,toparty, totag
        :return:
        '''
        if not (kwargs.get('touser') or kwargs.get('toparty') or kwargs.get('totag')):
            # 三者均为空，默认发送全体成员
            kwargs.update({'touser': ['@all']})
        data.update({
            "touser": self._list2str(kwargs.get('touser', [])),
            "toparty": self._list2str(kwargs.get('toparty', [])),
            "totag": self._list2str(kwargs.get('totag', [])),
            "msgtype": content_type,
            "agentid": self._agentid,
            "safe": kwargs.get('safe', 0),
            "enable_id_trans": kwargs.get('enable_id_trans', 0),
            "enable_duplicate_check": kwargs.get('enable_duplicate_check', 0),
            "duplicate_check_interval": kwargs.get('duplicate_check_interval', 1800)
        })
        return self._post(data)

    def send_text(self,
                  content: str,
                  **kwargs):
        '''
        发送text消息
        :param content: 消息内容，最长不超过2048个字节，超过将
        :param safe: 是否是保密消息，False表示可对外分享，True表示不能分享且内容显示水印，默认为False，下面方法同，不再重复解释
        :param kwargs: touser, toparty, totag
        :return: send result
        '''
        if not content:
            self.logger.error(self.errmsgs['texterror'])
            return {
                'errcode': 404,
                'errmsg': self.errmsgs['texterror']
            }
        else:
            data = {
                "text": {
                    "content": content
                },
            }
            return self._send_content(content_type='text', data=data, **kwargs)

    def send_news(self,
                  title: str,
                  desp: Optional[str],
                  url: str,
                  picurl: Optional[str],
                  **kwargs):
        '''
        发送图文消息
        :param title: 图文标题，不超过128个字节，超过会自动截断
        :param desp: 图文描述，可选，不超过512个字节，超过会自动截断
        :param url: 跳转链接
        :param picurl: 图片url，支持JPG、PNG格式，较好的效果为大图 1068*455，小图150*150。
        :return:
        '''
        if not (title and url):
            self.logger.error(self.errmsgs['newserror'])
            return {
                'errcode': 404,
                'errmsg': self.errmsgs['newserror']
            }
        else:
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
                },
            }
            return self._send_content(content_type='news', data=data, **kwargs)

    def send_mpnews(self,
                    title: str,
                    image_path: str,
                    content: str,
                    author: Optional[str],
                    content_source_url: Optional[str],
                    digest: Optional[str],
                    **kwargs):
        '''
        发送mpnews消息
        :param title: 图文标题
        :param image_path: 缩略图所在路径
        :param content: 图文消息内容
        :param author: 作者信息
        :param content_source_url: 点击跳转链接
        :param digest: 图文消息描述
        :param kwargs:
        :return:
        '''
        if not (title and image_path and content):
            self.logger.error(self.errmsgs['mpnewserror'])
            return {
                'errcode': 404,
                'errmsg': self.errmsgs['mpnewserror']
            }
        else:
            self._media_api = f'https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={self.access_token}&type=image'
            thumb_media_id = self._get_media_id_or_None(media_type='image',p_media=Path(image_path))
            data = {
                "mpnews": {
                    "articles": [
                        {
                            "title": title,
                            "thumb_media_id": thumb_media_id,
                            "author": author,
                            "content_source_url": content_source_url,
                            "content": content,
                            "digest": digest
                        }
                    ]
                },
            }
            return self._send_content(content_type='mpnews', data=data, **kwargs)


    def send_markdown(self,
                      content: str,
                      **kwargs):
        '''
        发送markdown消息
        :param content: markdown文本数据或markdown文件路径
        :return:
        '''
        if not content:
            self.logger.error(self.errmsgs['markdownerror'])
            return {
                'errcode': 404,
                'errmsg': self.errmsgs['markdownerror']
            }
        else:
            md_path = Path(content)
            if md_path.is_file():
                content = md_path.read_text()
            data = {
                "markdown": {
                    "content": content,
                },
            }
            return self._send_content(content_type='markdown', data=data, **kwargs)

    def send_card(self,
                  title: str,
                  desp: str,
                  url: str,
                  btntxt: Optional[str],
                  **kwargs):
        '''
        发送卡片消息
        :param title: 标题，不超过128个字节，超过会自动截断
        :param desp: 描述，不超过512个字节，超过会自动截断
        :param url: 点击后跳转的链接
        :param btntxt: 按钮文字。 默认为“详情”， 不超过4个文字，超过自动截断
        :return:
        '''
        if not (title and desp and url):
            self.logger.error(self.errmsgs['carderror'])
            return {
                'errcode': 404,
                'errmsg': self.errmsgs['carderror']
            }
        else:
            data = {
                "textcard": {
                    "title": title,
                    "description": desp,
                    "url": url,
                    "btntxt": btntxt
                },
            }
            return self._send_content(content_type='textcard', data=data, **kwargs)

    def send_taskcard(self, *args, **kwargs):
        raise MethodNotImplementedError


