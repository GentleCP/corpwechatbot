# 首页

<p align="center">
<a href="https://github.com/GentleCP/corpwechat-bot"><img width="300" src="https://gitee.com/gentlecp/ImgUrl/raw/master/20210425111523.png"></a>
</p>

<p align="center">
<a href="https://hits.seeyoufarm.com"><img src="https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2FGentleCP%2Fcorpwechat-bot&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false"/></a>
<a ><img src="https://img.shields.io/badge/python-3.5%2B-blue"/></a>
<a ><img src="https://img.shields.io/pypi/v/corpwechatbot"/></a>
</p>

:wave: `corpwechat-bot`是一个`python`封装的企业机器人&应用消息推送库，通过企业微信提供的api实现。

利用本库，你可以轻松地实现从服务器端发送一条文本、图片、视频、`markdown`等等消息到你的微信手机端，而不依赖于其他的第三方应用

![](img/work_mechanism.png)

## QuickStart

[快速开始](quickstart.md)能够让你在最快的时间内上手`corpwechatbot`，跳过较为繁杂的参数步骤，但如果你希望能使用更多`corpwechatbot`的功能，请查看**Usage**

## Usage
- 安装
```python
pip install -U corpwechatbot
```
- 使用     

[点此](使用教程/index.md)查看详细使用教程

## ChangeLog

你可以在[更新日志](changelog.md)中查看最新版本提交的功能和bug修复信息

## Todo
下面包括已经完成的功能、修复任务和未来会加入的新功能特性等内容

### Finished

> 已完成的开发任务，你可以在**ChangeLog**中查看更详细的完成情况

- [x] `fix`：token存储位置修改，初始设置保存到本地`site-packages`（后期将其移到`site-packages/corpwechatbot`目录下，方便统一）
- [x] `docs`：readme和usage更新
- [x] `feat`：终端快捷使用，一行命令式消息发送，例如`corpwechatbot -s "hello world"`直接发送一条文本消息
- [x] `refactor`：核心代码优化与重构
- [x] `docs` : 添加`QuickStart`
- [x] `feat`：允许将企业微信配置信息存储到本地文件读取
- [x] `fix`: 修复在指定标签和部门后依然默认发送给全体成员的问题
- [x] `feat`: 支持多个第三方应用消息推送
- [x] `feat`: 添加对`mpnews`的发送支持
- [x] `feat`: 添加对`taskcard`的发送支持
- [x] `feat`: 添加回调配置功能，该功能用以支持更丰富的使用场景，如
    - 用户发送消息给应用，识别关键词，返回不同的消息内容
    - 用户点击应用菜单，转换为相应指令，执行自动化任务，接收任务卡片消息，根据卡片内容，用户可选择在移动端点击反馈
    - 服务端（你的服务器）与移动端（你的微信&企业微信）实现更`amazing`的交互模式（💯如聊天机器人）
      >  该功能的基础原型已经完成，可在[回调配置](使用教程/index.md#_21)中查看，但还有待改进和测试的空间，暂未发布版本
      
- [x] `feat`: 支持对群聊应用消息推送
- [x] `feat`: 支持多个本地密钥文件共存

### Development Schedule

> 开发任务队列，排在前面的会优先考虑开发，如果你有希望实现的功能，可以提交`issue`进行说明，合理的会被采纳


## Author

[@GentleCP](https://github.com/GentleCP)

## License

本项目遵守[GPL v3](LICENSE)开源协议

## Sponsor

本项目完全出于公益性质开源使用，作者独自完成开发测试等一系列工作，如果它帮到了你，解决了你的痛点需求，你可以请作者喝杯阔乐，或者给这个项目一个`star`（右上角），激励作者继续更新完善本项目，非常感谢🙏

![](https://cdn.jsdelivr.net/gh/GentleCP/ImgUrl/1411624691159_.pic_hd.jpg)

