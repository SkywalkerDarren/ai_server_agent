# AI Server Agent

子服务器AI助手，实现自然语言对子服务器进行监控和管理。如：部署释放云服务器，启停云服务器，监控游戏服务器状态，启动等。

本项目集成了kook api服务，阿里云api服务，openai服务。

# WIP

## key相关

[阿里云 access key](https://help.aliyun.com/zh/ram/user-guide/create-an-accesskey-pair?spm=a2c4g.53045.0.i1#task-2245479)

[kook开发者中心](https://developer.kookapp.cn/)

[openai key](https://platform.openai.com/api-keys)

## 首次启动流程：
检查当前是否存在名称为game-server的阿里云服务器

如果存在就上报当前服务器状态，退出启动流程

否则检查当前是否存在名称为game-template的阿里云启动模板

如果存在就使用这个模板进行新建服务器

如果不存在就提示用户新建模板，退出启动流程

检查当前是否存在名称为game-data的阿里云盘

如果不存在就提示用户创建云盘

如果存在就使用game-template模板创建新服务器

挂载game-data云盘到game-server服务器

等待服务器启动完成


# 监控服务开启服务器流程

检查名称为game-server的阿里云服务器是否存在

如果不存在则提示启动失败

如果存在则轮询检查服务器状态，超时时间5分钟

如果在运行中就提示服务器启动成功，提示用户当前服务器的ip和实例状态

如果在启动中就轮询到启动完成

如果停机中就轮询到已停机

如果已停机就调用启动服务器，继续轮询


# 监控服务器关闭服务器流程

检查名称为game-server的阿里云服务器是否存在

如果不存在则提示停止失败

如果存在则轮询检查服务器状态，超时时间5分钟

如果在运行中就停止服务器，继续轮询

如果在启动中就轮询到启动完成

如果停机中就轮询到已停机

如果已停机就提示用户已关闭服务器


# 监控服务检查服务器状态流程
