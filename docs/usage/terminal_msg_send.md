# 本地密钥配置与终端消息推送

## 企业微信本地配置文件
默认情况下，在初始化推送实例的时候，都会要求传入相应的关键参数，但在程序中直接写这些敏感信息并不是一个好选项，因此新版本支持在本地用户目录(`~`)下创建一个`.corpwechatbot_key`文件，写入如下配置信息：
```python
[app]
corpid=  
corpsecret=
agentid=
[chatbot]
key=
```
这样，在实例化一个类时，就不需要再显式地传入`corpid,corpsecret,key`等参数了，如下：

```python
from corpwechatbot.app import AppMsgSender
from corpwechatbot import CorpWechatBot

app = AppMsgSender()  # 不传参，直接从本地`~/.corpwechatbot_key`读取
app.send_text(content="如果我是DJ，你会爱我吗？")

bot = CorpWechatBot()
bot.send_text(content='Hello World!')
```

同时由于配置信息都统一存储在本地，意味着你任何一个新的项目也可以不需要专门设置一个文件来存储这些敏感数据了

> 如果你不知道`~`目录在哪，可以通过如下代码获取：
>
> ```python
> from pathlib import Path
> 
> print(Path.home())
> ```
> 在`v0.6.0`之后，支持本地创建多个密钥文件，并在实例化`AppMsgSender`的时候传入文件路径进行指定密钥的实例化，如下：
>```python
>from corpwechatbot.app import AppMsgSender
>
>app = AppMsgSender(key_path="~/.corpwechatbot_key2")
>```


## 终端快速发送消息
很多时候，我们希望直接在终端敲一行代码就将消息发送到了我们的手机上，**在`v0.2.0`版本后支持啦！！！** 使用前需先**配置本地密钥文件**

目前支持：

### 文本消息

```python
# 应用消息
cwb -u='app' -t='hello world'  # 通过应用发送消息
cwb -t='hello world'  # 更快捷的方式

# 群聊机器人消息
cwb -u='bot' -t='hello world'
```
### markdwn消息

```python
cwb -u='app' -m='hello world'  
cwb -m='# Hello World'  # 更快捷的方式

# 群聊机器人消息
cwb -u='bot' -m='hello world'
```

- **动图演示**

![](../img/teminal_msgsend.gif)