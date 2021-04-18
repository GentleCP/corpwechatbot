#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
-----------------File Info-----------------------
            Name: command.py
            Description: send message from terminal directly
            Author: GentleCP
            Email: 574881148@qq.com
            WebSite: https://blog.gentlecp.com
            Create Date: 2021/4/18 
-----------------End-----------------------------
"""
from argparse import ArgumentParser
from corpwechatbot.app import AppMsgSender
from corpwechatbot.chatbot import CorpWechatBot


def app(content, type='text'):
    '''
    send by app
    :param content: text or markdown
    :return:
    '''
    app = AppMsgSender()
    if type == 'markdown':
        app.send_markdown(content)
    else:
        app.send_text(content)


def bot(content, type='text'):
    '''
    send by bot
    :param content: text or markdown
    :return:
    '''
    bot = CorpWechatBot()
    if type == 'markdown':
        bot.send_markdown(content)
    else:
        bot.send_text(content)


def main():
    cwb_argparse = ArgumentParser('python interface for corpwechat message sending')
    cwb_argparse.add_argument('--use', '-u', default='app', type=str, help='send by what(app/bot)?')
    cwb_argparse.add_argument('--text', '-t', default='', type=str, help='send a text message')
    cwb_argparse.add_argument('--markdown', '-m', default='', type=str, help='send a markdown content')
    args = cwb_argparse.parse_args()
    use_func = globals().get(args.use, 'app')  # 如果随便输入则按照app处理
    if args.text:
        # send text
        use_func(content=args.text)
    if args.markdown:
        use_func(content=args.markdown, type='markdown')

