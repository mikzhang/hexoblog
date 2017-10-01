---
title: Vim-Python支持
date: 2017-10-01 10:03:37
categories: Vim
tags:
    - Vim
---

Vim 集成 Python 编程环境时, 需要 Python 支持, 但有的环境并不支持 python2, 而支持 python3, 所以需要配置 Vim 进行支持

<!-- more -->

1. Ctrl+Alt+T 打开命令终端，输入: vim --version |grep python 查看vim是否支持python
{% asset_img 20161029201019726.png %}
我这个vim只支持python3，不支持python
2. 安装py2包，在命令终端下输入: sudo apt-get install vim-nox-py2
3. 可以再次用vim –version|grep python 查看此时vim是否支持python，若支持到此为止，若不支持，请执行第四步。 
4. 在命令终端输入:sudo update-alternatives –config vim
{% asset_img 20161029201825239.png %}
我这里是第三项属于python，第二项属于python3，故想打开哪一项支持就输入它的编号就可以了（0，1，2，3）。

