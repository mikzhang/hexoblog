---
title: Hexo+Github搭建静态博客-01本地服务
date: 2017-07-27 16:26:21
tags:
---

# Hexo+Github搭建静态博客-01本地服务

## 安装Git和NodeJS环境

因为hexo需要依赖Git和NodeJs，所以需要先安装环境。

Git下载地址：https://git-scm.com/download/win
NodeJS下载地址：https://nodejs.org/download/
安装过程详见官网

## 安装hexo
>\$ npm install -g hexo-cli
>\$ hexo init &lt;your-hexo-site&gt;
>\$ cd &lt;your-hexo-site&gt;
>\$ npm install

## 使用 alpha-dust 主题
### 安装
>\$ cd &lt;your-hexo-site&gt;
>\$ git clone https://github.com/klugjo/hexo-theme-alpha-dust themes/alpha-dust

### 配置
修改/_config.yml中的blog的主题:
\# Extensions
\#\# Plugins: https://hexo.io/plugins/
\#\# Themes: https://hexo.io/themes/
theme: alpha-dust

### 写文章

>\$ hexo new "Hello World"
>\$ hexo s --debug

访问http://localhost:4000，确保站点正确运行。
