---
title: Linux_通过源码编译安装程序
date: 2018-01-10 10:00:00
categories: Linux
tags:
    - Linux
---

本文简单的记录了下，在linux下如何通过源码安装程序，以及相关的知识。

<!-- more -->

## 程序的组成部分

Linux下程序大都是由以下几部分组成:

- 二进制文件:也就是可以运行的程序文件
- 库文件:就是通常我们见到的lib目录下的文件
- 配置文件:这个不必多说，都知道
- 帮助文档:通常是我们在linux下用man命令查看的命令的文档

## linux下程序的存放目录

linux程序的存放目录大致有三个地方:

- /etc, /bin, /sbin, /lib  :系统启动就需要用到的程序，这些目录不能挂载额外的分区，必须在根文件系统的分区上
- /usr/bin,/usr/sbin,/usr/lib:操作系统核心功能，可以单独分区
- /usr/local/bin,/usr/local/sbin,/usr/local/lib,/usr/local/etc,/usr/local/man:这个用于安装第三方程序，分别对应了二进制文件、库文件、配置文件、帮助文档的目录

通常来说我们安装程序就安装在 /usr/local目录下

## 编译安装源程序

步骤:

1. 使用如下命令查看当前是否安装了gcc编译器，没有可以先用yum安装gcc
```
gcc --version  #查看是否安装gcc
```
2. 解压源码包，例如:
```
tar -xvf nginx-1.7.7.tar.gz #解压源码包
```
3. 进入解压好的源码包:
```
cd nginx-1.7.7 #进入源码包
```
4. 执行configure文件，此文件有两个功能:1、让用户选定编译特性；2、检查编译环境。configure执行后将生成MakeFile文件。例如:
```
./configure --prefix=/usr/local/nginx --conf-path=/etc/nginx/nginx.conf
```
    其中我们通过--prefix制定了安装路径，通过--conf-path制定了配置文件的具体位置。注意:不是所有的程序的configure参数都是一样的 可以使用 ./configure --help查看详细参数说明。如果该程序所依赖的库在当前系统中没有安装，则会导致configure最后报错，遇到这种情况就需要你先安装依赖库。
5. 执行make命令，编译程序
```
make
```
6. 编译成功后就可以安装了，执行如下命令
```
make install
```
到此程序就算安装完成了，但是不要忘了还有后续的配置哦

## 配置程序

步骤:

1. 修改PATH环境变量，以能够识别此程序的二进制文件路径；
修改/etc/profile文件，在文件中 添加
```
export PATH=$PATH:/path/to/somewhere　　#记得是可执行文件所在的目录，路径中不要包含可执行文件。
```
然后执行
```
source /etc/profile #是我们的修改生效 　　　
```
2. 默认情况下，系统搜索库文件的路径/lib, /usr/lib; 要增添额外搜寻路径(注意:有的程序不提供库文件，那就不需要此设置了)
在/etc/ld.so.conf.d/中创建以.conf为后缀名的文件，而后把要增添的路径直接写至此文件中；然后执行如下命令使其生效
```
ldconfig
```
3. 如果程序提供了库文件，也会相应的提供头文件，一般在安装目录的include目录下，系统默认扫描头文件的路径是:/usr/include。我们可以在/usr/include下用链接连接到我们安装程序的头文件。
```
ln -s /usr/local/nginx/include  /usr/include/yourname
```
4. 可能程序还提供了帮助文档，一般是安装目录下的man目录，为了我们可以使用man命令查看我们程序的帮助文档，我们需要:在/etc/man.config中添加一条MANPATH，指向我们的文档目录

## 删除软件

方法一、如果你知道要删除软件的具体名称，可以使用               
```
sudo apt-get remove --purge 软件名称  
sudo apt-get autoremove --purge 软件名称 
```

方法二、如果不知道要删除软件的具体名称，可以使用
```
dpkg --get-selections | grep ‘软件相关名称’
sudo apt-get purge 一个带core的package，如果没有带core的package，则是情况而定。
```

清理残留数据
```
dpkg -l |grep ^rc|awk '{print $2}' |sudo xargs dpkg -P 
```
