---
title: Mysql-Linux-自启动
date: 2018-01-02 00:00:00
categories: Mysql
tags:
    - Mysql
---

这篇文章主要介绍了MySQL的自启动相关

<!-- more -->

##自启动

1. 欲使mysql开机自启动，首先需要注册mysql为ubuntu下的服务。
直接拷贝mysql.server文件至/etc/init.d/目录下即可。
```
sudo cp $MYSQL_HOME/support-files/mysql.server /etc/init.d/mysql.server
sudo chmod +x /etc/init.d/mysql.server
```

2. 修改my.cnf，指定mysql的启动用户
定义：命令1=”./mysql.server start –user=user1“，命令2=”./mysql.server start”。（注意，命令1、2的区别在于红色部分）

在编译安装mysql的过程中，若执行configure命令时指定“–user=user1”参数，则mysql将由用户user1启动，在mysql.server文件中会有“user=user1”这样一行来指定mysql的启动用户，但该行指定的启动用户并未生效。即，需要使用命令1来启动mysql，命令2启动失败。

为了使命令2生效，同时为了mysql开机自启动，需要修改my.cnf，在[mysqld]区块下添加“user=user1”这样一行。如此，便可使用命令2启动mysql，mysql也可以成功开机自启动。

3. 设置mysql开机自启动

让mysql开机自己启动 
```
$ sudo update-rc.d -f mysql.server defaults  
root@leroy-linux:/etc/init.d# update-rc.d -f mysql.server defaults
　　Adding system startup for /etc/init.d/mysql ...
　　/etc/rc0.d/K20mysql.server -> ../init.d/mysql.server
　　/etc/rc1.d/K20mysql.server -> ../init.d/mysql.server
　　/etc/rc6.d/K20mysql.server -> ../init.d/mysql.server
　　/etc/rc2.d/S20mysql.server -> ../init.d/mysql.server
　　/etc/rc3.d/S20mysql.server -> ../init.d/mysql.server
　　/etc/rc4.d/S20mysql.server -> ../init.d/mysql.server
　　/etc/rc5.d/S20mysql.server -> ../init.d/mysql.server
```
如果不想让mysql开机自己启动，可以使用 
```
$ sudo update-rc.d -f mysql.server remove  
root@sean-linux:/etc/init.d# update-rc.d -f mysql remove
　　Removing any system startup links for /etc/init.d/mysql ...
　　/etc/rc0.d/K21mysql.server
　　/etc/rc1.d/K21mysql.server
　　/etc/rc2.d/S19mysql.server
　　/etc/rc3.d/S19mysql.server
　　/etc/rc4.d/S19mysql.server
　　/etc/rc5.d/S19mysql.server
　　/etc/rc6.d/K21mysql.server
```
4. 服务的使用
启动mysql：service mysql.server start；
停止mysql：service mysql.server  stop；
查看mysql运行状态：service mysql.server  status。

另外，要确保mysql启动用户user1对$MYSQL_HOME具有读写权限，否则会因权限问题导致mysql启动失败。
（若无法启动 可考虑加上sudo）


## 补充
Ubuntu 取消 Apache及MySQL等自启动

1. 装个 sysv-conf-rc
2. sudo update-rc.d -f mysql remove 删除mysql随机器启动的服务
sudo update-rc.d -f apache2 remove 删除apache2随机器启动的服务
3. 查看/etc/rc2.d/里面的apache和mysql启动脚本，通常都是两个阿拉伯数字后再接一个英文字母，再加脚本名称。英文字母是S的都是会自动启动的，K则相反。所以只要找到apache和mysql的启动脚本，把S改成K就可以了

ref:
[http://blog.csdn.net/hackerwin7/article/details/22686819a](http://blog.csdn.net/hackerwin7/article/details/22686819)
