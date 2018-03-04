我们欢迎有能力的组织和个人镜像我们的软件仓库。以下是推荐的申请流程：

1. 在本仓库开一个 pr，说明相关情况，并在 mirrors.yaml 文件中添加预计建立镜像的相关信息。同时在 pr 中提供一个邮件地址。
2. 等待含有 rsync 用户名和密码的邮件。
3. 等镜像初始化完成之后，pr 将被合并。

推荐的同步命令：

```sh
RSYNC_PASSWORD=<你的rsync密码> rsync -rtlivH --delete-after --delay-updates --safe-links --max-delete=1000 --contimeout=60 <你的rsync用户名>@sync.repo.archlinuxcn.org::repo .
```

关于同步频率：我们的打包机器人 lilac 每天 CST 1、9、17 点多会开始打包，因此建议同步频率6、7小时一次，尽量避开 lilac 打包的时间段。

你也可以发送邮件到 repo 位于 archlinuxcn.org 来申请。

