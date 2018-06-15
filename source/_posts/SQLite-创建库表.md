---
title: SQLite-创建库表
date: 2018-01-01 10:03:37
categories: SQLite
tags:
    - SQLite
---

SQLite 创建库表

<!-- more -->

## 创建库

SQLite 的 sqlite3 命令被用来创建新的 SQLite 数据库。您不需要任何特殊的权限即可创建一个数据。

```
E:\py_wkspc\pswstoreapi>sqlite3 pswstore.db
SQLite version 3.24.0 2018-06-04 19:24:41
Enter ".help" for usage hints.
sqlite>
sqlite>
sqlite> .databases
main: E:\py_wkspc\pswstoreapi\pswstore.db
sqlite>
```
创建库的位置, 即为命令执行的目录

## 创建表

ref:
[http://www.runoob.com/sqlite/sqlite-create-database.html](http://www.runoob.com/sqlite/sqlite-create-database.html)
[https://www.yiibai.com/sqlite/create-table.html](https://www.yiibai.com/sqlite/create-table.html)
