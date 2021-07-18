#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
-----------------File Info-----------------------
            Name: app.py
            Description: 企业微信应用消息推送
            Author: GentleCP
            Email: me@gentlecp.com
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
from typing import List, Dict

from corpwechatbot._sender import MsgSender
from corpwechatbot.error import TokenGetError, MethodNotImplementedError
from corpwechatbot.util import is_image, is_voice, is_video, is_file

CUR_PATH = Path(__file__)
TOKEN_PATH = CUR_PATH.parent.joinpath('token.json')  # 存储在本项目根目录下


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
        self._token_key = hashlib.sha1(bytes(self._corpid + self._agentid, encoding='utf-8')).hexdigest()

        self.access_token = self.get_assess_token()
        self._web_interface = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}'
        self._media_interface = 'https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={}&type={}'
        self._webhook = self._web_interface.format(self.access_token)
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
            return self.__get_access_token(token_dict)
        else:
            try:
                token = token_dict[self._token_key]
            except KeyError:
                # 该agentid对应token不存在
                self.logger.debug("token不存在，获取token")
                return self.__get_access_token(token_dict)
            else:
                now = time.time()
                if now - TOKEN_PATH.stat().st_mtime >= 2 * 3600:
                    self.logger.debug("token过期，重新获取token")
                    return self.__get_access_token(token_dict)
                return token

    def __get_access_token(self, token_dict={}):
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

    def __list2str(self, datas: []):
        '''
        将传入的list数据转换成 | 划分的字符串
        e.g. ['user1', 'user2'] -> 'user1|user2'
        :param datas:
        :return:
        '''
        return "".join([item + '|' for item in datas])[:-1]

    def __send_res_check(self, send_res, data):
        '''
        检查消息推送的结果，若token失效，则重新获取并再次发送消息
        :param send_res:
        :param data:
        :return: send_res
        '''
        if send_res.get('errcode') == 0:
            return send_res
        elif send_res.get('errcode') == 40014:
            # invalid access token, refresh token
            self.logger.info("尝试重新获取token并发送消息")
            self.access_token = self.__get_access_token()  # 运行时长超过token周期导致token更新，无需访问本地token
            self._webhook = self._web_interface.format(self.access_token)
            return self._post(data)
        else:
            self.logger.error(f"发送失败! 原因：{send_res['errmsg']}")
            return send_res

    def _send(self,
              msg_type: str = '',
              data: dict = {},
              media_path: Optional[str] = '',
              **kwargs):
        '''
        新的统一内部发送接口，供不同消息推送接口调用
        :param msg_type: 
        :param data: 
        :param media_path: 只有需要media id的时候才传入
        :param kwargs:
        :return: 
        '''
        media_types = {'image', 'voice', 'video', 'file'}
        # prepare data
        if not (kwargs.get('touser') or kwargs.get('toparty') or kwargs.get('totag')):
            # 三者均为空，默认发送全体成员
            kwargs['touser'] = ['@all']
        data.update({
            "touser": self.__list2str(kwargs.get('touser', [])),
            "toparty": self.__list2str(kwargs.get('toparty', [])),
            "totag": self.__list2str(kwargs.get('totag', [])),
            "msgtype": msg_type,  # 注意这里msg_type已经是正确了，后面的改动不影响
            "agentid": self._agentid,
            "safe": kwargs.get('safe'),
            "enable_id_trans": kwargs.get('enable_id_trans'),
            "enable_duplicate_check": kwargs.get('enable_duplicate_check'),
            "duplicate_check_interval": kwargs.get('duplicate_check_interval')
        })
        # 检查消息类型是否需要获取media_id, 如需要，则获取，并做相应检查
        if msg_type in media_types:
            # 发送媒体消息
            self._media_api = self._media_interface.format(self.access_token, msg_type)
            media_res = self._get_media_id(media_type=msg_type, p_media=Path(media_path))
            data[msg_type] = {
                "media_id": media_res.get('media_id', None)
            }
        elif msg_type == 'mpnews':
            # mpnews比较特殊，单独处理
            self._media_api = self._media_interface.format(self.access_token, 'image')
            media_res = self._get_media_id(media_type='image', p_media=Path(media_path))
            data[msg_type]["articles"][0]["thumb_media_id"] = media_res.get('media_id', None)
        send_res = self._post(data)
        if send_res.get('errcode') == 0:
            return send_res
        elif send_res.get('errcode') == 40014:
            # invalid access token, refresh token
            self.logger.info("尝试重新获取token并发送消息")
            self.access_token = self.__get_access_token()  # 运行时长超过token周期导致token更新，无需访问本地token
            self._webhook = self._web_interface.format(self.access_token)
            # 如果是media还需要更新media_api
            if msg_type in media_types:
                self._media_api = self._media_interface.format(self.access_token, msg_type)
                media_res = self._get_media_id(media_type=msg_type, p_media=Path(media_path))
                data[msg_type] = {
                    "media_id": media_res.get('media_id', None)
                }
            elif msg_type == 'mpnews':
                self._media_api = self._media_interface.format(self.access_token, 'image')
                media_res = self._get_media_id(media_type='image', p_media=Path(media_path))
                data[msg_type]["articles"][0]["thumb_media_id"] = media_res.get('media_id', None)
            return self._post(data)
        else:
            self.logger.error(f"发送失败! 原因：{send_res['errmsg']}")
            return send_res

    def send_image(self,
                   image_path: str,
                   **kwargs):
        '''
        发送图片，支持jpg、png、bmp
        :param image_path: 图片存储路径
        :return:
        '''
        if not is_image(image_path):
            self.logger.error(self.errmsgs['image_error'])
            return {
                'errcode': 404,
                'errmsg': self.errmsgs['image_error']
            }
        return self._send(msg_type='image', media_path=image_path, **kwargs)

    def send_voice(self,
                   voice_path: str,
                   **kwargs):
        '''
        发送语音，2MB，播放长度不超过60s，仅支持AMR格式
        :param voice_path:
        :return:
        '''

        if not is_voice(voice_path):
            self.logger.error(self.errmsgs['voice_error'])
            return {
                'errcode': 404,
                'errmsg': self.errmsgs['voice_error']
            }
        return self._send(msg_type='voice', media_path=voice_path, **kwargs)

    def send_video(self,
                   video_path: str,
                   **kwargs):
        '''
        发送视频
        :param video_path:
        :return:
        '''
        if not is_video(video_path):
            self.logger.error(self.errmsgs['video_error'])
            return {
                'errcode': 404,
                'errmsg': self.errmsgs['video_error']
            }
        return self._send(msg_type='video', media_path=video_path, **kwargs)

    def send_file(self,
                  file_path: str,
                  **kwargs):
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
        return self._send(msg_type='file', media_path=file_path, **kwargs)

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
            self.logger.error(self.errmsgs['text_error'])
            return {
                'errcode': 404,
                'errmsg': self.errmsgs['text_error']
            }
        data = {
            "text": {
                "content": content
            },
        }
        return self._send(msg_type='text', data=data, **kwargs)

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
            },
        }
        return self._send(msg_type='news', data=data, **kwargs)

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
            self.logger.error(self.errmsgs['mpnews_error'])
            return {
                'errcode': 404,
                'errmsg': self.errmsgs['mpnews_error']
            }
        data = {
            "mpnews": {
                "articles": [
                    {
                        "title": title,
                        "author": author,
                        "content_source_url": content_source_url,
                        "content": content,
                        "digest": digest
                    }
                ]
            }}
        return self._send(msg_type='mpnews', data=data, media_path=image_path, **kwargs)

    def send_markdown(self,
                      content: str,
                      **kwargs):
        '''
        发送markdown消息
        :param content: markdown文本数据或markdown文件路径
        :return:
        '''
        if not content:
            self.logger.error(self.errmsgs['markdown_error'])
            return {
                'errcode': 404,
                'errmsg': self.errmsgs['markdown_error']
            }
        md_path = Path(content)
        if md_path.is_file():
            content = md_path.read_text()
        data = {
            "markdown": {
                "content": content,
            },
        }
        return self._send(msg_type='markdown', data=data, **kwargs)

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
            self.logger.error(self.errmsgs['card_error'])
            return {
                'errcode': 404,
                'errmsg': self.errmsgs['card_error']
            }
        data = {
            "textcard": {
                "title": title,
                "description": desp,
                "url": url,
                "btntxt": btntxt
            },
        }
        return self._send(msg_type='textcard', data=data, **kwargs)

    def send_taskcard(self,
                      title: str,
                      desp: Optional[str],
                      url: str,
                      task_id: str,
                      btn: List[Dict],
                      **kwargs):
        '''
        发送任务发片消息
        :param title: 标题，不超过128个字节，超过会自动截断（支持id转译）
        :param desp: 描述，不超过512个字节，超过会自动截断（支持id转译）
        :param url: 点击后跳转的链接。最长2048字节，请确保包含了协议头(http/https)，需要先自行配置回调服务
        :param task_id: 任务id，同一个应用发送的任务卡片消息的任务id不能重复，只能由数字、字母和“_-@”组成，最长支持128字节
        :param btn: 按钮列表，按钮个数为1~2个，btn的例子如下，各个具体参数的含义参考：https://open.work.weixin.qq.com/api/doc/90000/90135/90236#%E4%BB%BB%E5%8A%A1%E5%8D%A1%E7%89%87%E6%B6%88%E6%81%AF
        "btn":[
            {
                "key": "key111",
                "name": "批准",
                "color":"red",
                "is_bold": true
            },
            {
                "key": "key222",
                "name": "驳回"
            }
        ]
        :param kwargs: 其他的通用参数，在此统一处理
        -------接收方的数据----
        {
           'ToUserName': 企业号,
           'FromUserName': 发送消息的用户名
           'MsgType': 'event',
           'CreateTime': '1624762869',
           'EventKey': 事件key，服务端根据key值确定用户点击的情况
           'TaskId': 任务id，这个必须是唯一的，在同一应用中发过之后不能重复(建议通过时间戳hash结合的方式生成)
           'Agentid': 应用id
        }
        :return:
        '''
        if not (title and task_id and btn):
            self.logger.error(self.errmsgs['taskcard_error'])
            return {
                'errcode': 404,
                'errmsg': self.errmsgs['taskcard_error']
            }
        data = {
            "interactive_taskcard": {
                "title": title,
                "description": desp,
                "url": url,
                "task_id": task_id,
                "btn": btn,
            },
        }
        return self._send(msg_type='interactive_taskcard', data=data, **kwargs)

if __name__ == '__main__':
    app = AppMsgSender()
    # app.send_text('123')
    app.send_image('../tests/data/test.png')