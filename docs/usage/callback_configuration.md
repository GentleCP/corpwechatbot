# 回调配置

## 配置步骤

> 本部分主要讲解如何配置企业微信的回调机制，主要参考[官方回调配置](https://open.work.weixin.qq.com/api/doc/90000/90135/90930) 和[官方接口代码](https://github.com/sbzhu/weworkapi_python)

目标：添加回调配置，支持更丰富的应用场景，如

- 用户发送消息给应用，识别关键词，返回不同的消息内容
- 用户点击应用菜单，转换为相应指令，执行自动化任务，接收任务卡片消息，根据卡片内容，用户可选择在移动端点击反馈
- 服务端（你的服务器）与移动端（你的微信&企业微信）实现更amazing的交互模式（💯如聊天机器人）

要求

- 一台有独立ip的服务器
- 简单的`fastapi`用法  

1. 在企业微信后台进入应用管理，选择一个应用，找到接收消息
![](https://cdn.jsdelivr.net/gh/GentleCP/ImgUrl/20210626140957.png)

2. 设置API接收消息的三个选项，如下
  ![](https://cdn.jsdelivr.net/gh/GentleCP/ImgUrl/20210626141701.png)
  
3. 参考[corpwechatbot-web (github.com)](https://gist.github.com/GentleCP/5d02f4e84b8c8905bcf67643223cd499)，在服务器上运行`web.py` 
```shell
python3 web.py -p=8000 -t="token" -a="aeskey" -c="corpid"
```
确认你的web服务成功启动，并能通过公网访问  

4.点击保存，如果正常，会提示API设置成功，记住这些配置信息
![](https://cdn.jsdelivr.net/gh/GentleCP/ImgUrl/20210626143027.png)

至此，你的服务器已经具备基本的请求和响应功能了，由于post的请求根据用户的需求各异，目前只是完成了一个简单的发送和响应功能，后续有时间再完善。

下面是请求响应的例子：
![](../img/callback_test.gif)