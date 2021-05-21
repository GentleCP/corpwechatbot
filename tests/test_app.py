#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
-----------------File Info-----------------------
            Name: test_app.py
            Description: 测试应用消息推送
            Author: GentleCP
            Email: 574881148@qq.com
            WebSite: https://blog.gentlecp.com
            Create Date: 2021/4/8 
-----------------End-----------------------------
"""

import unittest
from corpwechatbot.app import AppMsgSender


class TestAppMsgSender(unittest.TestCase):
    ams = AppMsgSender()

    def test_send_text(self):
        '''
        测试文本发送
        :return:
        '''
        res = self.ams.send_text(content="Hi, it's GentleCP", safe=1)
        self.assertEqual(res.get('errcode', 1), 0)

    def test_send_voice(self):
        '''
        测试语音发送
        :return:
        '''
        res = self.ams.send_voice(voice_path="data/test.amr")
        self.assertEqual(res.get('errcode', 1), 0)

    def test_send_image(self):
        '''
        测试图片发送
        :return:
        '''
        res = self.ams.send_image(image_path="data/test.png", safe=1)
        self.assertEqual(res.get('errcode', 1), 0)

    def test_send_video(self):
        '''
        测试视频发送
        :return:
        '''
        res = self.ams.send_video(video_path="data/test.mp4", safe=1)
        self.assertEqual(res.get('errcode', 1), 0)

    def test_send_file(self):
        '''
        测试文件发送
        :return:
        '''
        res = self.ams.send_file(file_path="data/test.txt", safe=1)
        self.assertEqual(res.get('errcode', 1), 0)

    def test_send_news(self):
        '''
        测试图文消息发送
        :return:
        '''
        res = self.ams.send_news(title="Hi, it's GentleCP",
                                 desp="Welcome to my world!",
                                 url="https://blog.gentlecp.com",
                                 picurl="https://gitee.com/gentlecp/ImgUrl/raw/master/20210313141425.jpg")
        self.assertEqual(res.get('errcode', 1), 0)

    def test_send_markdown(self):
        '''
        测试markdown发送
        :return:
        '''
        res = self.ams.send_markdown(content="# Hi \n > 好家伙，我tm直接好家伙")
        self.assertEqual(res.get('errcode', 1), 0)

    def test_send_card(self):
        '''
        测试卡片消息发送
        :return:
        '''
        res = self.ams.send_card(title='求索｜CP',
                                 desp='CP的个人博客',
                                 url="https://blog.gentlecp.com",
                                 btntxt="more",
                                 )
        self.assertEqual(res.get('errcode', 1), 0)

    def test_send_mpnews(self):
        res = self.ams.send_mpnews(title='你好，我是CP',
                                   image_path='data/test.png',
                                   content='<a href="https://blog.gentlecp.com">Hello World</a>',
                                   content_source_url='https://blog.gentlecp.com',
                                   author='GentleCP',
                                   digest='这是一段描述',
                                   safe=1)
        self.assertEqual(res.get('errcode', 1), 0)


if __name__ == '__main__':
    unittest.main()
