---
title: Vim-Ctags
date: 2017-10-01 10:03:37
categories: Vim
tags:
    - Vim
    - Ctags
---

Ctags 在windows 下安装

<!-- more -->

下载 [Exuberant Ctags](http://ctags.sourceforge.net/)


下载一个支持windows的版本的，只要拷贝出ctags.exe这个文件就可以，把它放在$(home)\vim71下（也就是在vim的安装目录下找到.exe这样的文件所在的文件目录下）

特别重要的地方：
编辑_vimrc，在里面加入以下两句： 
```
set tags=tags; 
set autochdir 
```
注意第一个命令里的分号是必不可少的。这个命令让vim首先在当前目录里寻找tags文件，如果没有找到tags文件，或者没有找到对应的目标，就到父目录中查找，一直向上递归。因为tags文件中记录的路径总是相对于tags文件所在的路径，所以要使用第二个设置项来改变vim的当前目录。
