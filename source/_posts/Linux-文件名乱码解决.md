---
title: Linux-文件名乱码解决
date: 2017-09-25 10:20:35
categories: Linux
tags:
    - Linux
---

Windows 下正常显示的文件名, 上传到 Linux 下后, 含有中文的文件名都显示乱码

<!-- more -->

文件是在Windows下创建的，而Windows的文件名中文编码默认GBK，Linux中默认文件名编码为UTF-8，编码不一致导致了文件名乱码的问题，解决这个问题需要对文件名进行转码，这个工具就是convmv。
SYNOPSIS：
```
convmv -f 源编码 -t 新编码 [options] FILES ... DIRECTORYS
```
本人用的是openSuSE，首先安装这个工具，man convmv查看用法
```
sudo zypper install convmv
```

然后，进行转码
```
convmv -f GBK -t zh_CN.UTF-8 -r the/directory
```
给出的提示显示了有意义的中文，但是ls还是没有变化！man一下，有一个选项--notest，这里不解释了，大家自己去看。

最后的命令：
```
convmv -f GBK -t zh_CN.UTF-8 -r --notest the/directory
```
