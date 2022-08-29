#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------File Info-----------------------
Name: test_appchat.py
Description:
Author: GentleCP
Email: me@gentlecp.com
Create Date: 8/5/2021 
-----------------End-----------------------------
"""
from pathlib import Path
import unittest
from corpwechatbot.app import AppMsgSender


class TestAppchatMsgSend(unittest.TestCase):
    app = AppMsgSender(key_path=Path.home().joinpath(".corpwechatbot_key_dmd"))

    def test_send_text(self):
        """
        测试文本发送
        :return:
        """
        res = self.app.send_text(content="Hello World", chatid="123")
        self.assertEqual(res.get('errcode', 1), 0)

    def test_send_voice(self):
        """
        测试语音发送
        :return:
        """
        res = self.app.send_voice(voice_path="data/test.amr", chatid="123")
        self.assertEqual(res.get('errcode', 1), 0)

    def test_send_image(self):
        """
        测试图片发送
        :return:
        """
        res = self.app.send_image(image_path="data/test.png", chatid="123")
        self.assertEqual(res.get('errcode', 1), 0)

    def test_send_video(self):
        """
        测试视频发送
        :return:
        """
        res = self.app.send_video(video_path="data/test.mp4", chatid="123")
        self.assertEqual(res.get('errcode', 1), 0)

    def test_send_file(self):
        """
        测试文件发送
        :return:
        """
        res = self.app.send_file(file_path="data/test.txt", chatid="123")
        self.assertEqual(res.get('errcode', 1), 0)

    def test_send_news(self):
        """
        测试图文消息发送
        :return:
        """
        res = self.app.send_news(title="news测试",
                                 desp="内容！",
                                 url="https://www.baidu.com",
                                 picurl="https://gitee.com/gentlecp/ImgUrl/raw/master/20210313141425.jpg",
                                 chatid="123")
        self.assertEqual(res.get('errcode', 1), 0)

    def test_send_markdown(self):
        """
        测试markdown发送
        :return:
        """
        res = self.app.send_markdown(content="# Hi \n > 好家伙，我tm直接好家伙", chatid="123")
        self.assertEqual(res.get('errcode', 1), 0)

    def test_send_card(self):
        """
        测试卡片消息发送
        :return:
        """
        res = self.app.send_card(title='卡片测试',
                                 desp='卡片内容',
                                 url="https://www.baidu.com/",
                                 btntxt="more",
                                 chatid="123")
        self.assertEqual(res.get('errcode', 1), 0)

    def test_send_mpnews(self):
        res = self.app.send_mpnews(title='你好，我是CP',
                                   image_path='data/test.png',
                                   content='<a href="https://blog.gentlecp.com">Hello World</a>',
                                   content_source_url='https://blog.gentlecp.com',
                                   author='GentleCP',
                                   digest='这是一段描述',
                                   safe=1,
                                   chatid="123")
        self.assertEqual(res.get('errcode', 1), 0)


if __name__ == '__main__':
    unittest.main()
