#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
-----------------File Info-----------------------
            Name: test_chatbot.py
            Description:
            Author: GentleCP
            Email: 574881148@qq.com
            WebSite: https://blog.gentlecp.com
            Create Date: 2021/4/7 
-----------------End-----------------------------
"""

import unittest
from corpwechatbot.chatbot import CorpWechatBot


class TestCorpWechatBot(unittest.TestCase):
    """
    企业微信机器人测试用例
    """
    cwb = CorpWechatBot()

    def test_send_text(self):
        '''
        测试text文本发送
        :return:
        '''
        res = self.cwb.send_text(content="Hi, it's GentleCP", mentioned_list=['@all'], mentioned_mobile_list=['@all'])
        self.assertEqual(res.get('errcode', 1), 0)

    def test_send_markdown(self):
        '''
        测试markdown发送
        :return:
        '''
        markdown = "# Hi\n > It's GentleCP, know more things about me by click [here](https://blog.gentlecp.com)"
        res = self.cwb.send_markdown(content=markdown)
        self.assertEqual(res.get('errcode', 1), 0)


    def test_send_image(self):
        '''
        测试图片发送
        :return:
        '''
        res = self.cwb.send_image(image_path='data/test.png')
        self.assertEqual(res.get('errcode', 1), 0)


    def test_send_news(self):
        '''
        测试图文消息发送
        :return:
        '''
        res = self.cwb.send_news(title='求索｜CP',
                                 desp='CP的个人博客',
                                 url='https://blog.gentlecp.com',
                                 picurl='https://gitee.com/gentlecp/ImgUrl/raw/master/20210313141425.jpg')
        self.assertEqual(res.get('errcode', 1), 0)


if __name__ == '__main__':
    unittest.main()


