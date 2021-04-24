# ChangeLog

## v0.2.1: 21/04/24
- `fix`: 修复终端直接运行-u参数随意输入报错的问题
- `feat`: 现在支持在发送`markdown`信息的时候直接传入`markdown`文件路径
- `docs`: 添加专用用于`pypi`的文档
- `docs`: 添加为何使用`corpwechatbot`的文档说明到`README`

## v0.2.0: 21/04/18
- `feat`: 允许在本地创建文件读取企业微信配置，避免每次程序都要传入
- `feat`: 支持在命令行直接执行包发送信息，如`cwb -u='app' -t='hello world'`
- `fix`：token存储位置修改，初始设置保存到本地`site-packages`（后期将其移到`site-packages/corpwechatbot`目录下，方便统一）

## v0.1.0: 2021/04/09
- 项目初始化建立
- 添加群聊机器人消息推送
- 添加应用消息推送，暂不支持**小程序消息、任务卡片消息**