---
title: Mysql-图解5种join连接和实例
date: 2017-10-13 00:00:00
categories: Mysql
tags:
    - Mysql
---

Join 连接在日常开发用得比较多，但大家都搞清楚了它们的使用区别吗？？一文带你上车~~

<!-- more -->

## 内连接 inner join

内连接是基于连接谓词将俩张表（如A和B）的列组合到一起产生新的结果表，在表中存在至少一个匹配时，INNER JOIN 关键字返回行。
![WX20190426-115417@2x.png](WX20190426-115417@2x.png)

下面是一个简单的使用案例 
![WX20190426-115530@2x.png](WX20190426-115530@2x.png)

以下是运行代码及结果 
![WX20190426-115604@2x.png](WX20190426-115604@2x.png)

## 左外连接 left join

左外连接Left join关键字会从左表那里返回所有的行，即使是在右表中没有匹配到的行 

![WX20190426-115711@2x.png](WX20190426-115711@2x.png)
![WX20190426-115744@2x.png](WX20190426-115744@2x.png)
![WX20190426-115810@2x.png](WX20190426-115810@2x.png)

## 右外连接 right join
右外连接关键字Right join会从右表那里返回所有的行，即使是在左表中没有匹配到的行 

![WX20190426-115902@2x.png](WX20190426-115902@2x.png)
![WX20190426-115924@2x.png](WX20190426-115924@2x.png)
![WX20190426-115947@2x.png](WX20190426-115947@2x.png)

## 全连接 full join
全连接的关键字Full join，只要其中某个表中存在匹配，Full join 就会返回行 

![WX20190426-120027@2x.png](WX20190426-120027@2x.png)
![WX20190426-120048@2x.png](WX20190426-120048@2x.png)
![WX20190426-120113@2x.png](WX20190426-120113@2x.png)

注意一点 mysql中是不支持Full join 的但是orcal等数据库是支持的。 
如果在mysql要使用Full join就会报以下错误 
![WX20190426-120150@2x.png](WX20190426-120150@2x.png)
解决办法：同时使用左连接和右连接 

以下是一个简单的例子
![WX20190426-120232@2x.png](WX20190426-120232@2x.png)

## 交叉连接 cross join
交叉连接一般使用的比较少，交叉连接又称笛卡尔连接或者叉乘连接，如果，A和B是俩个集合，他们的交叉连接就是A*B 

ref:
[https://mp.weixin.qq.com/s?__biz=MzI3ODcxMzQzMw==&mid=2247485697&idx=1&sn=aa41e25d02a92d0d83a597074f6d579c&chksm=eb538c37dc240521dd10df0498404a37fb81c61aef665efcae142831ca7b7bbfadfcdb53ff4e&scene=21#wechat_redirect](https://mp.weixin.qq.com/s?__biz=MzI3ODcxMzQzMw==&mid=2247485697&idx=1&sn=aa41e25d02a92d0d83a597074f6d579c&chksm=eb538c37dc240521dd10df0498404a37fb81c61aef665efcae142831ca7b7bbfadfcdb53ff4e&scene=21#wechat_redirect)
