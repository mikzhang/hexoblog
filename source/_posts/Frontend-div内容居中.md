---
title: Frontend_div内容居中
date: 2017-08-10 12:56:10
categories: Frontend
tags:
     - Frontend
---

<!-- more -->

## 问题
遇到一个问题。想让一个div中元素居中，使用padding:0 auto;width:1000px;
行不通， 使用margin：0 auto；的话，居中的两边背景色会用空白。

## 解决
把要居中的div 设置成 display: inline-block;，然后在父div加上 text-align: center; 让div居中。
