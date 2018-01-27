---
title: Regex
date: 2017-10-01 10:03:37
categories: Regex
tags:
    - Regex
---


<!-- more -->

1. Ctrl+Alt+T 打开命令终端，输入: vim --version |grep python 查看vim是否支持python
{% asset_img 20161029201019726.png %}
我这个vim只支持python3，不支持python
2. 安装py2包，在命令终端下输入: sudo apt-get install vim-nox-py2
|:---|:---|:---|:---|
4. 在命令终端输入:sudo update-alternatives –config vim
{% asset_img 20161029201825239.png %}
我这里是第三项属于python，第二项属于python3，故想打开哪一项支持就输入它的编号就可以了（0，1，2，3）。
5. 想知道Vim中使用的Python版本，你可以在编辑器中运行: python import sys; print(sys.version)

