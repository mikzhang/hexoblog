---
title: Python-switch-2-latest-python3
date: 2017-09-19 14:23:56
categories: Python
tags:
    - Python
---

LinuxMint and Ubuntu installs python2.7 and python3.5 as default. But I want 2 install the latest Python3.6 and set it as the default python.

<!-- more -->

## check current python versions

use follow commands:
```
ran@ranux:~$ python -V
Python 2.7.12
ran@ranux:~$ python2 -V
Python 2.7.12
ran@ranux:~$ python3 -V
Python 3.5.2
ran@ranux:~$ 
```

## install python3.6 into Linux

```
$ sudo add-apt-repository ppa:jonathonf/python-3.6
$ sudo apt update
$ sudo apt install python3.6
```

## check installed python3.6

```
ran@ranux:~$ python3.6 -V
Python 3.6.3
```

old python3.5 is still exist, and it is still the default python3.
to change python3.6 just installed as the default python3, we need the tool '''update-alternatives'''.

## change default python3

```
ran@ranux:~$ update-alternatives --list python3
update-alternatives: error: no alternatives for python3
```

why like this? Cauz we didn't maintained them.
do as follows:
```
$ sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.5 1
$ sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 2
```

recheck alternatives:

```
ran@ranux:~$ update-alternatives --list python3
/usr/bin/python3.5
/usr/bin/python3.6
```

## switch 2 the latest python3

```
ran@ranux:~$ sudo update-alternatives --config python3
有 2 个候选项可用于替换 python3 (提供 /usr/bin/python3)。

  选择       路径              优先级  状态
------------------------------------------------------------
  0            /usr/bin/python3.6   2         自动模式
  1            /usr/bin/python3.5   1         手动模式
* 2            /usr/bin/python3.6   2         手动模式

要维持当前值[*]请按<回车键>，或者键入选择的编号：
```

then specify the latest python3 as default by select numbers.

## swith python2 2 python3
ps: do not do anything on python2, as many system tools may rely on it.
if you want 2 use python3 instead of python2, suggest you use virtualenv.
But, if you really really want 2 change python2 2 python3 on your system, do as follows

```
sudo update-alternatives --install /usr/bin/python python /usr/local/lib/python2.7 1
sudo update-alternatives --install /usr/bin/python python /usr/local/lib/python3.x 2
```
