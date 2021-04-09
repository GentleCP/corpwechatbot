# corpwechat-bot
[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2FGentleCP%2Fcorpwechat-bot&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)
![python version](https://img.shields.io/badge/python-3.5+-blue)

`corpwechat-bot`是一个`python`封装的企业机器人&应用消息推送库，通过企业微信提供的api实现。

利用本库，你可以轻松地实现从服务器端发送一条文本、图片、视频、`markdown`等等消息到你的微信手机端，而不依赖于其他的第三方应用，如`ServerChan`。



## Requirements

> **注意**，本项目依赖于企业微信创建群聊机器人或应用，要想实现需要先注册一个属于你自己的企业微信号，这十分简便，参照[官方网址](https://work.weixin.qq.com/)即可

当你有了企业微信后，你还需要做一些配置，根据你自身的需求来做选择：

- **应用消息推送** ：应用消息推送需要在企业微信中创建一个第三方应用，[参照教程](https://open.work.weixin.qq.com/wwopen/helpguide/detail?t=selfBuildApp)
- **群聊机器人消息推送**：群聊机器人消息推送需要在你已有的企业群中添加一个机器人，然后获取相应的机器人`key`，[参照教程](https://jingyan.baidu.com/article/d45ad148cc79eb28552b80b5.html)

## Features
目前实现了两种推送消息方式，**应用消息推送**和**群聊机器人消息推送**，具体效果参考[使用教程](docs/usage.md)

- **应用消息推送**：该推送会直接传至你的个人微信上，你会像收到好友消息一样收到通知信息，**不需要安装企业微信**，具体包括：
  - [x] 文本消息: 最普通的消息，文字内容，最长不超过2048个字节
  - [x] 图片消息：发送一张图片，可选`jpg,png`，大小不超过2MB，目前仅支持通过图片路径发送.
  - [x] 语音消息：发送一条语音，大小不超过2MB，时长不超过60s，必须是`.amr`格式
  - [x] 视频消息：发送一段视频，大小不超过10MB，必须是`.mp4`格式
  - [x] 普通文件：其他类型的文件，大小不超过20MB（不小于5字节）
  - [x] markdown消息：传输markdown类型消息
  - [x] 图文消息：图片文字形式，带有跳转链接，适合做推广
  - [x] 文本卡片消息：以卡片形式呈现的文本，包含跳转链接
  - [ ] 小程序通知消息：应用需绑定小程序才可使用，尚未实现
  - [ ] 任务卡片消息：允许用户点击做出相应反馈的卡片，需绑定回调函数，尚未实现

- **群聊机器人消息推送**：该推送仅会发送消息到企业微信群聊中，经测试，个人微信的企业群聊不会收到机器人发送的消息，因此要收到消息**需安装企业微信**，具体包括：
  - [x] 文本消息：普通文字消息，最长不超过2048个字节
  - [x] 图片消息：图片大小不超过2M
  - [x] 图文消息：图片文字形式，带有跳转链接，适合打广告
  - [x] 文件消息：发送单个文件到群聊，大小在`5B~20MB`之间

## ChangeLog
[点此](docs/changelog.md)查看ChangeLog

## Usage
[点此](docs/usage.md)查看使用教程

## Author
[@GentleCP](https://github.com/GentleCP)

## Contibutors
- [@GentleCP](https://github.com/GentleCP)

## License
本项目遵守[GPL v3](LICENSE)开源协议
