# 更新日志
## v0.6.4: 22/08/29
- `fix`: 修复发送markdown消息时文件名过长导致的问题，现在仅读取`.md`结尾的文件，若文件不存在，则直接发送内容
## v0.6.3: 22/08/02
- `feat`: 现在支持在创建`AppMsgSender,CorpWechatBot`时提供`proxies`参数，通过代理发送消息，适合内网环境中无法直接连接外网的情况
## v0.6.2: 22/03/05
- `feat`: 现在创建群聊`app.create_chat(show_chat=True)`的时候可设置`show_chat`选项，表是否在群聊成功创建后发送第一条消息到群聊，让群聊显示在会话列表中，发送的消息会包含群聊id信息。

## v0.6.1: 21/08/22
- `fix`: 解决[issue](https://github.com/GentleCP/corpwechatbot/issues/9)
- `feat`: 支持用户自行决定是否显示日志，在初始化`AppMsgSender`,`CorpwechatBot`实例的时候传入`log_level`参数决定日志的显示等级，可选等级有：`50(CRITICAL), 40(ERROR), 30(WARNING), 20(INFO,默认), 10(DEBUG), 0(NOTSET)`, 下面是一个例子：
```python
import cptools
from corpwechatbot import AppMsgSender

app = AppMsgSender(log_level=20)  # 显示INFO及以上级别的log
app2 = AppMsgSender(log_level=cptools.INFO)  # 你也可以选择易读性更高的传入方式
```

## v0.6.0: 21/08/05
- `feat`: 支持应用群聊创建与消息推送
- `feat`: 支持多个本地文件key，用于存储多个密钥信息
- `refactor`: 优化重构部分代码，移除多余文件
- `doc`: 优化文档内容

## v0.5.2: 21/07/19
- `fix`: 修复token过期导致发送消息失败的问题，当程序长时间运行导致获取的token过期时，会自动更新token，并重新发送一遍失败的消息
![](https://cdn.jsdelivr.net/gh/GentleCP/ImgUrl/20210719204916.png)
## v0.5.1: 21/07/18
- `refactor`: 重构部分代码，提升简洁性
- `fix`: ~~修复token过期导致发送失败的问题（程序运行超过2小时）~~
> 经检查，本次修复的实际上是无效token的问题，并没解决token过期的问题

## v0.5.0: 21/06/27
- `feat`: 添加对任务卡片消息发送的支持
- `feat`: 添加服务器回调配置程序
- `docs`: 简化说明文档

## v0.4.0: 21/05/21
- `feat`: 添加对`mpnews`类型消息的支持，关于该类型的解释参考[官网](https://work.weixin.qq.com/api/doc/90000/90135/90236#%E5%9B%BE%E6%96%87%E6%B6%88%E6%81%AF%EF%BC%88mpnews%EF%BC%89)
- `feat`: 添加对参数`enable_id_trans`, `enable_duplicate_check`,`duplicate_check_interval`，现在你可以在发送消息的时候指定它们，具体参考官网
- `refactor`: 更改参数`safe`为`int`，含义与官网等同，优化部分代码

## v0.3.1: 21/05/17
- `fix`: 修复不同企业同一id应用的token存储冲突问题
## v0.3.0: 21/05/16
-  `feat`: 支持在同一个项目中创建多个应用消息推送

## v0.2.4: 21/05/11
- `fix`：修复因单例模式参数设置不正确导致实例化`AppMsgSender`异常的问题
- `v0.2.1`特性继承
- `v0.2.2`特性继承
- `v0.2.3`特性继承

## ~~v0.2.3: 21/05/10~~
- `fix`: 修复从`pypi`安装`corpwechatbot`出现的找不到`pypidoc.md`的错误

## ~~v0.2.2: 21/05/07~~

- `fix`: 1000004
- `refactor`: 优化重构`AppMsgSender`部分代码，更改传参机制
- `docs`: 更新使用文档和README文档的内容

## ~~v0.2.1: 21/04/24~~
- `fix`: 修复终端直接运行-u参数随意输入报错的问题
- `feat`: 现在支持在发送`markdown`信息的时候直接传入`markdown`文件路径
- `docs`: 添加专用用于`pypi`的文档
- `docs`: 添加为何使用`corpwechatbot`的文档说明到`README`

## v0.2.0: 21/04/18
- `feat`: 允许在本地创建文件读取企业微信配置，避免每次程序都要传入
- `feat`: 支持在命令行直接执行包发送信息，如`cwb -u='app' -t='hello world'`
- `fix`：token存储位置修改，初始设置保存到本地`site-packages`（后期将其移到`site-packages/corpwechatbot`目录下，方便统一）

## v0.1.0: 21/04/09
- 项目初始化建立
- 添加群聊机器人消息推送
- 添加应用消息推送，暂不支持**小程序消息、任务卡片消息**