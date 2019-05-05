---
title: Linux_Cmd_cp_两个有用的命令
date: 2017-08-14 10:00:00
categories: Linux
tags:
    - Linux
    - Cmd
---

Linux cp_两个有用的命令

<!-- more -->

## 高效用法 1：更新你的文件夹

比如说在我的电脑上有一个存放各种文件的文件夹，另外我要不时的往里面添加一些新文件，而且我会不时地修改一些文件，例如我手机里下载的照片或者是音乐。

假设我收集的这些文件对我而言都很有价值，我有时候会想做个拷贝，就像是“快照”一样将文件保存在其它媒体。当然目前有很多程序都支持备份，但是我想更为精确的将目录结构复制到可移动设备中，方便于我经常使用这些离线设备或者连接到其它电脑上。

cp 命令提供了一个易如反掌的方法。例子如下：

在我的 Pictures 文件夹下，我有这样一个文件夹名字为 Misc。为了方便说明，我把文件拷贝到 USB 存储设备上。让我们开始吧！
```
me@desktop:~/Pictures$ cp -r Misc /media/clh/4388-D5FE
me@desktop:~/Pictures$
```
输入这个命令 cp -r Misc /media/clh/4388-D5FE 并执行后 ，拷贝 Misc 目录下所有文件（这个 -r 参数，全称 “recursive”，递归处理，意思为本目录下所有文件及子目录一起处理）到我的 USB 设备的挂载目录 /media/clh/4388-D5FE。

执行命令后回到之前的提示，大多数命令继承了 Unix 的特性，在命令执行后，如果没有任何异常什么都不显示，在任务结束之前不会显示像 “execution succeeded” 这样的提示消息。如果想获取更多的反馈，就使用 -v 参数让执行结果更详细。

假设我要在原始拷贝路径下 ~/Pictures/Misc 下添加一些新文件，现在我想只拷贝新的文件到我的存储设备上，我就使用 cp 的“更新”和“详细”选项。
```
me@desktop:~/Pictures$ cp -r -u -v Misc /media/clh/4388-D5FE
'Misc/asunder.png' -> '/media/clh/4388-D5FE/Misc/asunder.png'
'Misc/editing tags guayadeque.png' -> '/media/clh/4388-D5FE/Misc/editing tags guayadeque.png'
'Misc/misc on usb.png' -> '/media/clh/4388-D5FE/Misc/misc on usb.png'
me@desktop:~/Pictures$
```
上面的第一行中是 cp 命令和具体的参数（-r 是“递归”， -u 是“更新”，-v 是“详细”）。接下来的三行显示被复制文件的信息。

通常来说，参数 -r 也可用更详细的风格 --recursive。但是以简短的方式，也可以这么连用 -ruv。

## 高效用法 2：版本备份
我在开发的时候定期给我的代码版本进行备份,假设我正在编写一个非常有用的 Python 程序，作为一个喜欢不断修改代码的开发者，我会在一开始编写一个程序简单版本，然后不停的往里面添加各种功能直到它能成功的运行起来。比方说我的第一个版本就是用 Python 程序打印出 “hello world”。这只有一行代码的程序就像这样：
```
print 'hello world'
```
然后我将这个代码保存成文件命名为 test1.py。现在程序可以运行了，我想在添加新的内容之前进行备份。我决定使用带编号的备份选项，如下：
```
clh@vancouver:~/Test$ cp --force --backup=numbered test1.py test1.py
clh@vancouver:~/Test$ ls
test1.py &nbsp;test1.py.~1~
clh@vancouver:~/Test$
```
所以，上面的做法是什么意思呢？

1. 这个 --backup=numbered 参数意思为“我要做个备份，而且是带编号的连续备份”。所以一个备份就是 1 号，第二个就是 2 号，等等。

2. 如果源文件和目标文件名字是一样的。通常我们使用 cp 命令去拷贝成自己，会得到这样的报错信息：
cp: 'test1.py' and 'test1.py' are the same file
在特殊情况下，如果我们想备份的源文件和目标文件名字相同，我们使用 --force 参数。

3. 我使用 ls （意即 “list”）命令来显示现在目录下的文件，名字为 test1.py 的是原始文件，名字为 test1.py.~1~ 的是备份文件

假如现在我要加上第二个功能，在程序里加上另一行代码，可以打印 “Kilroy was here.”。现在程序文件 test1.py 的内容如下：
```
print 'hello world'
print 'Kilroy was here'
```
看到 Python 编程多么简单了吗？不管怎样，如果我再次执行备份的步骤，结果如下：
```
clh@vancouver:~/Test$ cp --force --backup=numbered test1.py test1.py
clh@vancouver:~/Test$ ls
test1.py test1.py.~1~ test1.py.~2~
clh@vancouver:~/Test$
```
现在我有有两个备份文件： test1.py.~1~ 包含了一行代码的程序，和 test1.py.~2~ 包含两行代码的程序。

ref:
[https://linux.cn/article-8766-1.html](https://linux.cn/article-8766-1.html)

