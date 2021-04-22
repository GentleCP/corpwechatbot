# corpwechat-bot
[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2FGentleCP%2Fcorpwechat-bot&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)
![python version](https://img.shields.io/badge/python-3.5+-blue)
![pypi version](https://img.shields.io/pypi/v/corpwechatbot)

`corpwechat-bot`是一个`python`封装的企业机器人&应用消息推送库，通过企业微信提供的api实现。

利用本库，你可以轻松地实现从服务器端发送一条文本、图片、视频、`markdown`等等消息到你的微信手机端，而不依赖于其他的第三方应用，如`ServerChan`。

> 如果喜欢该项目，记得给个star，让更多人能够看到本项目♥️

## QuickStart
安装与使用一步到位：

```shell
pip install -U corpwechatbot
```

- **应用消息推送**：发送一条文本消息到你设置的应用，在手机个人微信上查看接收

```python
from corpwechatbot.app import AppMsgSender

app = AppMsgSender(corpid='',  # 你的企业id
                   corpsecret='',  # 你的应用凭证密钥
                   agentid='')   # 你的应用id
app.send_text(content="如果我是DJ，你会爱我吗？")
```
推送结果

![img.png](https://gitee.com/gentlecp/ImgUrl/raw/master/20210412090701.png)

> 现在支持直接从命令行发送消息，如`cwb -t='如果我是DJ，你会爱我吗？'`，效果同上，具体参考[使用教程](docs/usage.md#)

- **群聊机器人消息推送**：发送一条文本消息到你设置了机器人的群聊

```python
from corpwechatbot.chatbot import CorpWechatBot

bot = CorpWechatBot(key='')  # 你的机器人key，通过群聊添加机器人获取

bot.send_text(content='Hello World')
```

推送结果：

![](https://gitee.com/gentlecp/ImgUrl/raw/master/20210412090725.png)

## Features
目前支持的功能：
- **应用消息推送**：该推送会直接传至你的个人微信上，你会像收到好友消息一样收到通知信息，**不需要安装企业微信**，具体包括：
    - 文本消息: 最普通的消息，文字内容，最长不超过2048个字节
    - 图片消息：发送一张图片，可选`jpg,png`，大小不超过2MB，目前仅支持通过图片路径发送.
    - 语音消息：发送一条语音，大小不超过2MB，时长不超过60s，必须是`.amr`格式
    - 视频消息：发送一段视频，大小不超过10MB，必须是`.mp4`格式
    - 普通文件：其他类型的文件，大小不超过20MB（不小于5字节）
    - markdown消息：传输markdown类型消息
    - 图文消息：图片文字形式，带有跳转链接，适合做推广
    - 文本卡片消息：以卡片形式呈现的文本，包含跳转链接

- **群聊机器人消息推送**：该推送仅会发送消息到企业微信群聊中，经测试，个人微信的企业群聊不会收到机器人发送的消息，因此要收到消息**需安装企业微信**，具体包括：
    - 文本消息：普通文字消息，最长不超过2048个字节
    - 图片消息：图片大小不超过2M
    - 图文消息：图片文字形式，带有跳转链接，适合打广告
    - 文件消息：发送单个文件到群聊，大小在`5B~20MB`之间
    
- **终端一条命令式消息推送**：不需要写额外的`python`代码，直接在终端输入一条命令`cwb -t='hello world'`即可推送消息到手机微信上

## Usage
更多内容与具体使用请查看[github](https://github.com/GentleCP/corpwechat-bot)

## Author

[@GentleCP](https://github.com/GentleCP)

## Contibutors
- [@GentleCP](https://github.com/GentleCP)

## License
本项目遵守[GPL v3](LICENSE)开源协议
