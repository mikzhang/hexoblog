---
title: Tmux-使用梳理
date: 2017-09-06 12:52:48
categories: Tmux
tags:
    - Tmux
---

Tmux是一个优秀的终端复用软件，类似GNU Screen，但来自于OpenBSD，采用BSD授权。使用它最直观的好处就是，通过一个终端登录远程主机并运行tmux后，在其中可以开启多个控制台而无需再“浪费”多余的终端来连接这台远程主机；是BSD实现的Screen替代品，相对于Screen，它更加先进：支持屏幕切分，而且具备丰富的命令行参数，使其可以灵活、动态的进行各种布局和操作。下面就Tmux的使用做一梳理

<!-- more -->

## 功能

-  提供了强劲的、易于使用的命令行界面。
-  可横向和纵向分割窗口。
-  窗格可以自由移动和调整大小，或直接利用四个预设布局之一。
-  支持 UTF-8 编码及 256 色终端。
-  可在多个缓冲区进行复制和粘贴。
-  可通过交互式菜单来选择窗口、会话及客户端。
-  支持跨窗口搜索。
-  支持自动及手动锁定窗口。

## 安装

ubuntu版本下直接apt-get安装
```
# sudo apt-get install tmux
```
centos7版本下直接yum安装
```
# yum install -y tmux
```
在Mac OS中安装
```
安装 Homebrew
$ ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
 
安装tmux
$ brew install tmux
```

## 使用

安装完成后输入命令tmux即可打开软件，界面十分简单，类似一个下方带有状态栏的终端控制台；但根据tmux的定义，在开启了tmux服务器后，会首先创建一个会话，而这个会话则会首先创建一个窗口，其中仅包含一个面板；也就是说，这里看到的所谓终端控制台应该称作tmux的一个面板，虽然其使用方法与终端控制台完全相同。
```
# tmux                                   //直接进入面板，如下使用效果：
```
{% asset_img 907596-20170303181719688-2083634286.png %}


## 快捷键

### 系统操作
```
?  列出所有快捷键；按q返回
d 脱离当前会话；这样可以暂时返回Shell界面，输入tmux attach能够重新进入之前的会话
D 选择要脱离的会话；在同时开启了多个会话时使用
Ctrl+z 挂起当前会话
r 强制重绘未脱离的会话
s 选择并切换会话；在同时开启了多个会话时使用
: 进入命令行模式；此时可以输入支持的命令，例如kill-server可以关闭服务器
[ 进入复制模式；此时的操作与vi/emacs相同，按q/Esc退出
~ 列出提示信息缓存；其中包含了之前tmux返回的各种提示信息
```

### 会话

| Command                 | Description               |
| ----------------------- | ------------------------- |
| `tmux ls` | 等同`tmux list-sessions`, 显示所有会话 |
| `tmux new -s <session-name>` | 新建会话并指定会话名称（建议制定会话名称，以便了解该会话用途）|
| `tmux new` | 新建会话（不指定会话名称）|
| `tmux a` | 等同`tmux attach`, 接入上一个会话 | 
| `tmux a -t <session-name>` | 接入指定名称的会话 |
| `tmux detach` | 断开当前会话（还可以在会话中使用快捷键：`control+b，再按d`）|
| `tmux kill-session -t session-name` | 关闭指定会话 |
| `tmux kill-session -a -t session-name` | 关闭除指定会话外的所有会话 |
| `tmux switch -t session_name` | 切换会话, 也可在会话中 `control+b，再按s 显示会话列表，再进行会话切换` |
| `tmux kill-server` | 销毁所有会话并停止tmux |

### 窗口操作

```
c 创建新窗口
& 关闭当前窗口
数字键 切换至指定窗口
p 切换至上一窗口
n 切换至下一窗口
l 在前后两个窗口间互相切换
w 通过窗口列表切换窗口
, 重命名当前窗口；这样便于识别
.  修改当前窗口编号；相当于窗口重新排序
f 在所有窗口中查找指定文本
```

### 面板操作
```
” 将当前面板平分为上下两块
% 将当前面板平分为左右两块
x 关闭当前面板
!  将当前面板置于新窗口；即新建一个窗口，其中仅包含当前面板
Ctrl+方向键 以1个单元格为单位移动边缘以调整当前面板大小
Alt+方向键 以5个单元格为单位移动边缘以调整当前面板大小
Space 在预置的面板布局中循环切换；依次包括even-horizontal、even-vertical、main-horizontal、main-vertical、tiled
q 显示面板编号
o 在当前窗口中选择下一面板
方向键 移动光标以选择面板
{ 向前置换当前面板
} 向后置换当前面板
Alt+o 逆时针旋转当前窗口的面板
Ctrl+o 顺时针旋转当前窗口的面板
```

ref: 
[https://www.cnblogs.com/kevingrace/p/6496899.html](https://www.cnblogs.com/kevingrace/p/6496899.html)
[https://robots.thoughtbot.com/a-tmux-crash-course](https://robots.thoughtbot.com/a-tmux-crash-course)
[https://www.cnblogs.com/aioria13/p/7191080.html](https://www.cnblogs.com/aioria13/p/7191080.html)
