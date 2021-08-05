# 群聊机器人消息推送

## 推送接口演示
> ⚠️注意！机器人发送的群聊只能在企业微信群聊中收到（个人微信中不会显示）！！！

要使用群聊机器人实现消息推送，你需要先实例化一个`CorpWechatBot`对象，如下：
```python
from corpwechatbot.chatbot import CorpWechatBot
# fromo corpwechatbot import CorpWechatBot  # both will work
bot = CorpWechatBot(key='')  # 你的机器人key，通过群聊添加机器人获取

# 如果你在本地配置添加了企业微信本地配置文件，也可以直接初始化CorpWechatBot，而无需再显式传入密钥参数
# bot = CorpWechatBot()
```
接着，你就可以利用接口实现快速的机器人群里消息推送，具体包括：
### 文本消息

```python
bot.send_text(content='Hello World')
```
> ![](../img/bot.png)

### 图片消息

```python
bot.send_image(image_path='test.png')
```
> ![img_8.png](../img/bot_image.png)

### markdown消息

```python
bot.send_markdown(content='# 面对困难的秘诀 \n > 加油，奥利给！')
```
> ![img_9.png](../img/bot_markdown.png)

### 图文消息

```python
bot.send_news(title='性感刘公，在线征婚',
              desp='刘公居然要征婚了？这到底是人性的扭曲，还是道德的沦丧？...',
              url='https://blog.gentlecp.com',
              picurl='https://gitee.com/gentlecp/ImgUrl/raw/master/20210313141425.jpg')
```
> ![img_10.png](../img/bot_news.png)


## 更多参数使用

上面只是简单地列出了每个消息推送接口的使用，对于一般使用已经足够了，如果你还有更细致的要求，例如@某人或@全体成员，需要配置以下参数：

群聊消息中发送text消息时可以指定`@`的成员

- `mentioned_list:[]`: userid列表，提醒群众某个成员，userid通过企业通讯录查看，`@all`则提醒所有人
- `mentioned_mobile_list:[]`: 手机号列表，提醒手机号对应的成员，`@all`代表所有人，当不清楚userid时可替换

```python
# 一个演示程序
from corpwechatbot.chatbot import CorpWechatBot

bot = CorpWechatBot(key='')  # 你的机器人key，通过群聊添加机器人获取
bot.send_text(content='Hello World',
              mentioned_list=['sb'],
              mentioned_mobile_list=['110'])

```
> ![img_11.png](../img/bot_at.png)

## 获取相关用户数据方法

进入企业微信后台->通讯录

- 如何获取userID
![](../img/get_userid.png)
- 如何获取mobile  
![img_15.png](../img/get_mobile.png)