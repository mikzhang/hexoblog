﻿---
title: SQLite
date: 2018-01-01 10:03:37
categories: SQLite
tags:
    - SQLite
---

SQLite 的一个重要的特性是零配置的，这意味着不需要复杂的安装或管理。本章将讲解 Windows、Linux 上的安装设置。

<!-- more -->

## 在 Windows 上安装 SQLite

- 请访问 [SQLite 下载页面](http://www.sqlite.org/download.html)，从 Windows 区下载预编译的二进制文件。
- 您需要下载 `sqlite-tools-win32-*.zip` 和 `sqlite-dll-win32-*.zip` 压缩文件。
- 创建文件夹 C:\sqlite，并在此文件夹下解压上面两个压缩文件，将得到 sqlite3.def、sqlite3.dll 和 sqlite3.exe 文件。
- 添加 C:\sqlite 到 PATH 环境变量，最后在命令提示符下，使用 sqlite3 命令，将显示如下结果。

```
C:\>sqlite3
SQLite version 3.7.15.2 2013-01-09 11:53:05
Enter ".help" for instructions
Enter SQL statements terminated with a ";"
sqlite>
```

## 在 Linux 上安装 SQLite
目前，几乎所有版本的 Linux 操作系统都附带 SQLite。所以，只要使用下面的命令来检查您的机器上是否已经安装了 SQLite。
```
$sqlite3
SQLite version 3.7.15.2 2013-01-09 11:53:05
Enter ".help" for instructions
Enter SQL statements terminated with a ";"
sqlite>
```

如果没有看到上面的结果，那么就意味着没有在 Linux 机器上安装 SQLite。因此，让我们按照下面的步骤安装 SQLite：

请访问 SQLite 下载页面，从源代码区下载 `sqlite-autoconf-*.tar.gz`。

步骤如下：
```
$tar xvfz sqlite-autoconf-3071502.tar.gz
$cd sqlite-autoconf-3071502
$./configure --prefix=/usr/local
$make
$make install
```
上述步骤将在 Linux 机器上安装 SQLite，您可以按照上述讲解的进行验证。

ref:
[http://www.runoob.com/sqlite/sqlite-installation.html](http://www.runoob.com/sqlite/sqlite-installation.html)
