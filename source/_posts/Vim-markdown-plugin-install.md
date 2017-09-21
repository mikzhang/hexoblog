---
title: Vim-markdown-plugin-install
date: 2017-09-21 00:00:00
categories: Vim
tags:
    - Vim
    - markdown
---


自从用了vim自后恨不得所有文字相关的写作都用vim来解决,最近开始接触markdown,所以网上搜了一圈markdown相关的插件,发现三个插件不错,语法高亮插件[vim-markdown](https://github.com/plasticboy/vim-markdown),实时预览插件[vim-instant-markdown](https://github.com/suan/vim-instant-markdown)和[python-vim-instant-markdown](https://github.com/isnowfy/python-vim-instant-markdown).

<!-- more -->

## vim-markdown插件

我用的是vundle管理插件,所以修改vim配置文件,添加
```
Plugin 'godlygeek/tabular'
Plugin 'plasticboy/vim-markdown'
```
之后执行
```
:PluginInstall
```

这里作者提到如用vundle管理插件,那么godlygeek/tabular这个插件必须在plasticboy/vim-markdown之前

安装好之后就可以看到语法高亮了(写这篇文章的时候用的是windows的gvim)
{% asset_img 1488218-9edc5fd3ca93295f.png %}

## vim-instant-markdown插件

这是一个实时预览的插件,当你用vim打开markdown文档的时候,会自动打开一个浏览器窗口,并且可以实时预览。此插件目前只支持OSX 和 Unix/Linuxes操作系统。

安装之前需要先安装node.js和并且安装了npm,这是作者的原文:
```
You first need to have node.js with npm installed.
[sudo] npm -g install instant-markdown-d
If you're on Linux, the xdg-utils package needs to be installed (is installed by default on Ubuntu).
Copy the after/ftplugin/markdown/instant-markdown.vim file from this repo into your ~/.vim/after/ftplugin/markdown/ (creating directories as necessary), or follow your vim package manager's instructions.
Ensure you have the line filetype plugin on in your .vimrc
Open a markdown file in vim and enjoy!
```

安装新版的node.js:
```
sudo add-apt-repository ppa:chris-lea/node.js
sudo apt-get update
sudo apt-get install nodejs
```
安装完node.js之后安装instant-markdown-d
```
sudo npm -g install instant-markdown-d
```

安装vim-instant-markdown插件:

在vim配置文件中添加:
```
Plugin 'suan/vim-instant-markdown'
```
vim里面执行:
```
:PluginInstall
```
安装完成后,只要vim打开了markdown类型的文件就会自动打开一个浏览器窗口实时预览


## python-vim-instant-markdown插件

python-vim-instant-markdown插件是用python写的,windows,linux都可以使用,安装这个插件需要python2支持,查看vim是否有python支持:
```
vim --version | grep +python
```
windows下的gvim已经有python2和python3的支持,只需要安装python2.7就可以使用。

安装依赖:
```
pip install markdown
pip install pygemnts
```
### vundle安装:

vim配置文件添加
```
Plugin 'isnowfy/python-vim-instant-markdown'
```
进入vim中执行:
```
:PluginInstall
```
### 直接安装:

将md_instant.vim和md_instant文件夹放到~/.vim/plugin/目录下,windows是vim安装目录的vimfiles/plugin文件夹。

### 使用

打开vim打开markdown文件后执行 **:Instantmd** 命令会自动打开一个浏览器窗口进行实时预览,如果浏览器没有自动打开窗口,可以访问http://localhost:7000/。

## markdown-preview
一个国人写的预览插件,觉得不错支持windows,还可以同步滚动
详情看github:[https://github.com/iamcco/markdown-preview.vim](https://github.com/iamcco/markdown-preview.vim)

ref:[http://www.jianshu.com/p/24aefcd4ca93](http://www.jianshu.com/p/24aefcd4ca93)
