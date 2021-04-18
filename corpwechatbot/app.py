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
from configparser import ConfigParser
from typing import Optional
from pathlib import Path
from cptools import LogHandler

from corpwechatbot._sender import MsgSender
from corpwechatbot._sender import TokenGetError, MethodNotImplementedError
from corpwechatbot.util import is_image, is_voice, is_video, is_file

CUR_PATH = Path(__file__)
TOKEN_PATH = CUR_PATH.parent.joinpath('token.txt')  # 存储在本项目根目录下

class KeyNotFound(Exception):

    def __str__(self):
        return f'Can not find file `{str(Path.home())}/.corpwechatbot_key`'

class AppMsgSender(MsgSender):
    """
    应用消息推送器，支持文本、图片、语音、视频、文件、文本卡片、图文、markdown消息推送
    """
    def __init__(self,
                 corpid:str='',
                 corpsecret:str='',
                 agentid:str=''):
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

        self.access_token = self.get_assess_token()
        self._webhook = f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={self.access_token}'
        self.logger = LogHandler('AppMsgSender')


    def get_assess_token(self):
        '''
        通过企业id和应用凭证密钥获取assess_token，用于消息推送
        :param corpid: 企业id，获取方式：https://work.weixin.qq.com/api/doc/90000/90135/91039#14953/corpid
        :param corpsecret: 创建的应用凭证密钥，获取方式：https://work.weixin.qq.com/api/doc/90000/90135/91039#14953/secret
        :return: assess_token
        '''
        try:
            old_token = TOKEN_PATH.read_text()
        except FileNotFoundError:
            self.logger.debug('旧token获取失败，重新获取token')
            return self._get_access_token(self._corpid, self._corpsecret)
        else:
            now = time.time()
            if now - TOKEN_PATH.stat().st_mtime >= 2 * 3600:
                self.logger.debug("token过期，重新获取token")
                return self._get_access_token(self._corpid, self._corpsecret)
            else:
                return old_token


    def _get_access_token(self, corpid:str, corpsecret:str):
        token_api = f'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={corpsecret}'
        res = requests.get(token_api).json()
        if res.get('errcode') == 0:
            self.logger.info("token请求成功")
            TOKEN_PATH.write_text(res.get('access_token'))
            return res.get('access_token')
        else:
            raise TokenGetError(f"token请求失败，原因：{res.get('errmsg')}")


    def _list2str(self, datas:[]):
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
                    touser=['@all'],
                    toparty:Optional=[],
                    totag:Optional=[],
                    safe:Optional[bool]=False):
        '''
        发送媒体文件统一方法
        :param media_path:
        :param media_type: 媒体类型，目前包括image, voice, video, file
        :param touser:
        :param toparty:
        :param totag:
        :param safe:
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
                data =  {
                    "touser" : self._list2str(touser),
                    "toparty" : self._list2str(toparty),
                    "totag" : self._list2str(totag),
                    "msgtype" : media_type,
                    "agentid" : self._agentid,
                    media_type : {
                        "media_id" : media_id
                    },
                    "safe": 1 if safe else 0,
                }
                return self._post(data)
            else:
                return {
                    'errcode': 405,
                    'errmsg': self.errmsgs['mediaerror']
                }


    def send_text(self,
                  content:str,
                  touser=['@all'],
                  toparty:Optional=[],
                  totag:Optional=[],
                  safe:Optional=False):
        '''
        发送text消息
        :param content: 消息内容，最长不超过2048个字节，超过将截断
        :param touser: 要发送的用户，通过列表划分，输入成员ID，默认发送给全体，下面方法同，不再重复解释
        :param toparty: 要发送的部门，通过列表划分，输入部门ID，当touser为@all时忽略，下面方法同，不再重复解释
        :param totag: 发送给包含指定标签的人，通过列表划分，输入标签ID，当touser为@all时忽略，下面方法同，不再重复解释
        :param safe: 是否是保密消息，False表示可对外分享，True表示不能分享且内容显示水印，默认为False，下面方法同，不再重复解释
        :return:
        '''
        if not content:
            self.logger.error(self.errmsgs['texterror'])
            return {
                'errcode': 404,
                'errmsg': self.errmsgs['texterror']
            }
        else:
            data =  {
                "touser" : self._list2str(touser),
                "toparty" : self._list2str(toparty),
                "totag" : self._list2str(totag),
                "msgtype" : "text",
                "agentid" : self._agentid,
                "text" : {
                    "content" : content
                },
                "safe": 1 if safe else 0,
            }
            return self._post(data)



    def send_image(self,
                   image_path:str,
                   touser=['@all'],
                   toparty:Optional=[],
                   totag:Optional=[],
                   safe:Optional[bool]=False):
        '''
        发送图片，支持jpg、png、bmp
        :param image_path: 图片存储路径
        :param touser:
        :param toparty:
        :param totag:
        :param safe:
        :return:
        '''
        return self._send_media(media_path=image_path,
                                media_type='image',
                                touser=touser,
                                toparty=toparty,
                                totag=totag,
                                safe=safe)



    def send_voice(self,
                   voice_path:str,
                   touser=['@all'],
                   toparty:Optional=[],
                   totag:Optional=[],
                   safe:Optional[bool]=False):
        '''
        发送语音，2MB，播放长度不超过60s，仅支持AMR格式
        :param voice_path:
        :param touser:
        :param toparty:
        :param totag:
        :param safe:
        :return:
        '''
        return self._send_media(media_path=voice_path,
                                media_type='voice',
                                touser=touser,
                                toparty=toparty,
                                totag=totag,
                                safe=safe)


    def send_video(self,
                   video_path:str,
                   touser=['@all'],
                   toparty:Optional=[],
                   totag:Optional=[],
                   safe:Optional[bool]=False):
        '''
        发送视频
        :param video_path:
        :param touser:
        :param toparty:
        :param totag:
        :param safe:
        :return:
        '''
        return self._send_media(media_path=video_path,
                                media_type='video',
                                touser=touser,
                                toparty=toparty,
                                totag=totag,
                                safe=safe)


    def send_news(self,
                  title:str,
                  desp:Optional[str],
                  url:str,
                  picurl:Optional[str],
                  touser=['@all'],
                  toparty:Optional=[],
                  totag:Optional=[]):
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
                "touser" : self._list2str(touser),
                "toparty" : self._list2str(toparty),
                "totag" : self._list2str(totag),
                "msgtype" : "news",
                "agentid" : self._agentid,
                "news" : {
                    "articles" : [
                        {
                            "title" : title,
                            "description" : desp,
                            "url" : url,
                            "picurl" : picurl
                        }
                    ]
                },
            }
            return self._post(data)


    def send_markdown(self,
                      content: str,
                      touser=['@all'],
                      toparty:Optional=[],
                      totag:Optional=[]):
        '''
        发送markdown消息
        :param content: markdown文本数据
        :param touser:
        :param toparty:
        :param totag:
        :return:
        '''
        if not content:
            self.logger.error(self.errmsgs['markdownerror'])
            return {
                'errcode': 404,
                'errmsg': self.errmsgs['markdownerror']
            }
        else:
            data = {
                "touser" : self._list2str(touser),
                "toparty" : self._list2str(toparty),
                "totag" : self._list2str(totag),
                "msgtype": "markdown",
                "agentid" : self._agentid,
                "markdown": {
                    "content": content,
                },
                "enable_duplicate_check": 0,
                "duplicate_check_interval": 1800
            }
            return self._post(data)


    def send_file(self,
                  file_path:str,
                  touser=['@all'],
                  toparty:Optional=[],
                  totag:Optional=[],
                  safe:Optional[bool]=False):
        '''
        发送文件
        :param file_path:
        :param touser:
        :param toparty:
        :param totag:
        :param safe:
        :return:
        '''
        return self._send_media(media_path=file_path,
                                media_type='file',
                                touser=touser,
                                toparty=toparty,
                                totag=totag,
                                safe=safe)


    def send_card(self,
                  title:str,
                  desp:str,
                  url:str,
                  btntxt:Optional[str],
                  touser=['@all'],
                  toparty:Optional=[],
                  totag:Optional=[]):
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
                "touser" : self._list2str(touser),
                "toparty" : self._list2str(toparty),
                "totag" : self._list2str(totag),
                "msgtype" : "textcard",
                "agentid" : self._agentid,
                "textcard" : {
                    "title" : title,
                    "description" : desp,
                    "url" : url,
                    "btntxt": btntxt
                },
            }
            return self._post(data)


    def send_taskcard(self, *args, **kwargs):
        raise MethodNotImplementedError


if __name__ == '__main__':
    app = AppMsgSender()
    app.send_text('jhhh')



