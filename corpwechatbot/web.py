#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------File Info-----------------------
Name: web.py
Description: web api support
Author: GentleCP
Email: me@gentlecp.com
Create Date: 2021/6/19
-----------------End-----------------------------
"""
import argparse
from fastapi import FastAPI
from fastapi import Response, Request
from WXBizMsgCrypt3 import WXBizMsgCrypt
from xml.etree.ElementTree import fromstring
import uvicorn

app = FastAPI()

def parse_args():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--port', '-p', default=8000, type=int, help="port to build web server")
    arg_parser.add_argument('--token', '-t', type=str, help='token set in corpwechat app')
    arg_parser.add_argument('--aeskey', '-a', type=str, help='encoding aeskey')
    arg_parser.add_argument('--corpid', '-c', type=str, help='your corpwechat id')
    args = arg_parser.parse_args()
    return args

args = parse_args()
wxcpt = WXBizMsgCrypt(args.token, args.aeskey, args.corpid)

@app.get("/")
async def verify(msg_signature: str,
                 timestamp: str,
                 nonce: str,
                 echostr: str):
    '''
    验证配置是否成功，处理get请求
    :param msg_signature:
    :param timestamp:
    :param nonce:
    :param echostr:
    :return:
    '''
    ret, sEchoStr = wxcpt.VerifyURL(msg_signature, timestamp, nonce, echostr)
    if ret == 0:
        return Response(content=sEchoStr.decode('utf-8'))
    else:
        print(sEchoStr)

@app.post("/")
async def recv(msg_signature: str,
               timestamp: str,
               nonce: str,
               request: Request):
    '''
    接收用户消息，可进行被动响应
    :param msg_signature:
    :param timestamp:
    :param nonce:
    :param request:
    :return:
    '''
    body = await request.body()
    ret, sMsg = wxcpt.DecryptMsg(body.decode('utf-8'), msg_signature, timestamp, nonce)
    decrypt_data = {}
    for node in list(fromstring(sMsg.decode('utf-8'))):
        decrypt_data[node.tag] = node.text
    # 解析后得到的decrypt_data: {"ToUserName":"企业号", "FromUserName":"发送者用户名", "CreateTime":"发送时间", "Content":"用户发送的内容", "MsgId":"唯一id，需要针对此id做出响应", "AagentID": "应用id"}
    # 用户应根据Content的内容自定义要做出的行为，包括响应返回数据，如下例子，如果发送的是123，就返回hello world

    # 处理任务卡片消息
    if decrypt_data.get('EventKey', '') == 'no':
        # 返回信息
        sRespData="""<xml>
   <ToUserName>{to_username}</ToUserName>
   <FromUserName>{from_username}</FromUserName>
   <CreateTime>{create_time}</CreateTime>
   <MsgType>update_taskcard</MsgType>
   <TaskCard>
       <ReplaceName>已处理</ReplaceName>
   </TaskCard>
</xml>
""".format(to_username=decrypt_data['ToUserName'],
           from_username=decrypt_data['FromUserName'],
           create_time=decrypt_data['CreateTime'],
           event_key=decrypt_data['EventKey'],
           agentid=decrypt_data['AgentId'])
    # 处理文本消息
    if decrypt_data.get('Content', '') == '我帅吗':
        sRespData = """<xml>
   <ToUserName>{to_username}</ToUserName>
   <FromUserName>{from_username}</FromUserName> 
   <CreateTime>{create_time}</CreateTime>
   <MsgType>text</MsgType>
   <Content>{content}</Content>
</xml>
""".format(to_username=decrypt_data['ToUserName'],
           from_username=decrypt_data['FromUserName'],
           create_time=decrypt_data['CreateTime'],
           content="帅得一逼",)
    ret, send_msg = wxcpt.EncryptMsg(sReplyMsg=sRespData, sNonce=nonce)
    if ret == 0:
        return Response(content=send_msg)
    else:
        print(send_msg)



if __name__ == "__main__":
    uvicorn.run("web:app", port=args.port, host='0.0.0.0', reload=False)
