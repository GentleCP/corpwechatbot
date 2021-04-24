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
from pathlib import Path
from argparse import ArgumentParser
from corpwechatbot.app import AppMsgSender
from corpwechatbot.chatbot import CorpWechatBot

def send_md(use='app', content=''):
    md_path = Path(content)
    if md_path.is_file():
        content = md_path.read_text()
    if use == 'bot':
        bot = CorpWechatBot()
        bot.send_markdown(content)
    else:
        app = AppMsgSender()
        app.send_markdown(content)

def send_txt(use='app', content=''):
    if use == 'bot':
        bot = CorpWechatBot()
        bot.send_text(content)
    else:
        app = AppMsgSender()
        app.send_text(content)


def main():
    cwb_argparse = ArgumentParser('python interface for corpwechat message sending')
    cwb_argparse.add_argument('--use', '-u', default='app', type=str, help='send by what(app/bot)?')
    cwb_argparse.add_argument('--text', '-t', default='', type=str, help='send a text message')
    cwb_argparse.add_argument('--markdown', '-m', default='', type=str, help='send a markdown content')
    args = cwb_argparse.parse_args()
    if args.text:
        # send text
        send_txt(use=args.use, content=args.text)
    if args.markdown:
        send_md(use=args.use, content=args.markdown)

