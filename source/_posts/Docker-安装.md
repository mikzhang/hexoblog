---
title: Docker-安装
date: 2017-10-01 10:03:37
categories: Docker
tags:
    - Docker
---

本文环境 Ubuntu 16.04 LTS

<!-- more -->

## 前提条件
Docker 要求 Ubuntu 系统的内核版本高于 3.10 ，查看本页面的前提条件来验证你的 Ubuntu 版本是否支持 Docker。

通过 uname -r 命令查看你当前的内核版本
```
runoob@runoob:~$ uname -r
```

## 使用脚本安装 Docker

### 获取最新版本的 Docker 安装包

```
runoob@runoob:~$ wget -qO- https://get.docker.com/ | sh
```
如果上述资源不可用, 可以尝试国内资源
```
curl -sSL https://get.daocloud.io/docker | sh
```
安装体验版或测试版，体验最新Docker。
```
curl -sSL https://get.daocloud.io/docker-experimental | sh
curl -sSL https://get.daocloud.io/docker-test | sh
```

安装完成后有个提示：
```
    If you would like to use Docker as a non-root user, you should now consider
    adding your user to the "docker" group with something like:

    sudo usermod -aG docker runoob
   Remember that you will have to log out and back in for this to take effect!  
```
当要以非root用户可以直接运行docker时，需要执行 sudo usermod -aG docker runoob 命令，然后重新登陆，否则会有如下报错

### 离线安装 Docker
根据自己的操作系统在下载列表中下载相应的 Docker 离线包，然后在终端中运行下面的命令安装 Docker。
```
tar -zxvf docker-offline-17.09.1-ce-<operating-system>.tar.gz
cd docker-offline-17.09.1-ce-<operating-system>
sudo chmod +x install.sh
sudo bash install.sh
```

### 卸载Docker

```
sudo apt-get remove docker docker-engine
```
卸载Docker后,/var/lib/docker/目录下会保留原Docker的镜像,网络,存储卷等文件. 如果需要全新安装Docker,需要删除/var/lib/docker/目录

### 启动docker 后台服务

```
runoob@runoob:~$ sudo service docker start
```

### 镜像加速
鉴于国内网络问题，后续拉取 Docker 镜像十分缓慢，我们可以需要配置加速器来解决，我使用的是网易的镜像地址：http://hub-mirror.c.163.com。

新版的 Docker 使用 /etc/docker/daemon.json（Linux） 或者 %programdata%\docker\config\daemon.json（Windows） 来配置 Daemon。

请在该配置文件中加入（没有该文件的话，请先建一个）：
```
{
  "registry-mirrors": ["http://hub-mirror.c.163.com"]
}
```


ref:
[http://get.daocloud.io/#install-docker](http://get.daocloud.io/#install-docker)
[https://download.daocloud.io/Docker_Mirror/Docker](https://download.daocloud.io/Docker_Mirror/Docker)

