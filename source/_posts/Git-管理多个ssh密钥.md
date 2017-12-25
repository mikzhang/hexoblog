---
title: Git-管理多个ssh密钥
date: 2017-12-24 00:00:00
categories: Git
tags:
    - Git
---

对于Git多帐号的情况,它可以动态管理SSH-KEY。

<!-- more -->


## SSH之于Git的原理

Git提交时有Https和SSH两种验证方式,Https的方式需要帐号和密码比较好理解,不过它需要在每次提交时输入帐号和密码,有点麻烦；而SSH的功能可以粗暴的理解为记住帐号密码,不过对这个过程有人会有点疑惑。首先,我们用SSH命令生成一个公钥-私钥对,我们会把公钥添加到Git的服务器,把私钥放在本地。提交文件的时候Git服务器会用公钥和客户端提交私钥做验证（具体细节不究）,如果验证通过则提交成功,那么我们在把公钥添加到服务器的时候肯定是需要登录Git服务器的,这个过程其实可以理解为帐号和密码托管给SSH了,所以也是相当于输入了帐号密码,但是由SSH帮你记住了。这么理解是可以,但是SSH的意义不仅仅是这样,关于SSH的更详细内容看客可以自行再了解。

## 生成SSH-KEY

打开命令行、终端,用命令进入到你要保存SSH-KEY文件的文件夹,我们先用命令测试下终端是否支持SSH:
如果你的终端支持SSH,那么你可能看到类似如下的版本信息:
```
$ ssh -V
OpenSSH_7.2p2 Ubuntu-4ubuntu2.2, OpenSSL 1.0.2g  1 Mar 2016
```

测试时如果提示不识别SSH命令,需要安装SSH。
Ubuntu安装SSH:
```
sudo apt-get install openssh-client openssh-server
```
CentOS安装SSH:
```
yum install openssh-client openssh-server
```

接下来在刚才的文件夹,使用SSH命令在当前文件夹生成一对SSH-KEY:
```
ssh-keygen -t rsa -C "邮箱地址"
```
接下来会出来提示信息,完整的大概是这样:
```
$ ssh-keygen -t rsa -C "smallajax@foxmail.com"
Generating public/private rsa key pair.
Enter file in which to save the key (~/.ssh/id_rsa):
```
这里需要输入SSH-KEY的文件名字,这里名字理论上可以随便取,但是我们今天要说配置多个SSH-KEY,所以请分别查看以下两节:

- 单个Git帐号的配置——全局Git配置
- 多个Git帐号的配置——局部Git配置

## 单个Git帐号的配置——全局Git配置

大部分人使用Git一般是一个帐号,所以接着上面的讲。
上面说到输入ssh-keygen命令生成SSH-KEY密钥对文件时需要输入文件名称,如果你仅仅要配置一个帐号,那么我们输入默认名称即可:id_rsa。
接着会要求输入私钥的密码,并且需要确认密码,为了安全在密码输入的时候不会反显,什么都看不到,这个密码你自己设置,但是你一定要记住:
```
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
```
到这里生成SSH-KEY的事就完成了,你在当前文件夹会看到两个文件:
```
id_rsa  id_rsa.pub
```

SSH-KEY生成了,接着给服务器和客户端配置SSH-KEY。
第一步把id_rsa.pub中的公钥内容添加到Git的SSH中,如果你使用Github或者Gitlib,在个人设置中会找到。
第二步把SSH-KEY配置给SSH,让系统的SSH知道这个KEY。
Linux把id_rsa文件拷贝到~/.ssh文件夹下,命令如下:
```
cp id_rsa ~/.ssh/
```
Window把id_rsa文件拷贝到C:/Users/你的用户名/.ssh文件夹下。

拷贝完成后,把.ssh文件夹下的id_rsa文件添加到SSH-Agent,命令如下:
```
ssh-add id_rsa文件的路径
```
例如Linux:ssh-add ~/.ssh/id_rsa,如果命令行此时正在.ssh文件夹下:ssh-add id_rsa即可,Windows同理。

最后,执行以下命名配置Git全局用户和邮箱:
```
git config --global user.name "你的名字"
git config --global user.email "你的邮箱"
```
例如:
```
git config --global user.name "YanZhenjie"
git config --global user.email "smallajax@foxmail.com"
```
配置全局用户和邮箱完成后,我们可以查看: 
Linux用户打开~/.gitconfig文件即可看到配置:
```
vim ~/.gitconfig
```
Windows用户打开C:/Users/你的用户名/.gitconfig即可看到配置,内容大概如下:
```
[user]
    name = YanZhenjie
    email = smallajax@foxmail.com
```
此时配置全部结束,请查看下方测试SSH-KEY配置是否成功进行测试。


## 多个Git帐号的配置——局部Git配置

又有很多人同时使用多个Git帐号,比如Github、OSChina、Gitlib等,再接着上面讲配置多个Git帐号。

上面说到输入ssh-keygen命令生成SSH-KEY密钥对文件时需要输入文件名称,如果你要配置多个帐号,就根据爱好输入KEY文件的名字吧,例如为Github配置就输入:id_rsa_github,为OSChina配置就输入:id_rsa_oschina。

接着会要求输入私钥的密码,并且需要确认密码,为了安全在密码输入的时候不会反显,什么都看不到,这个密码你自己设置,但是你一定要记住:
```
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
```
到这里生成SSH-KEY的事就完成了,你在当前文件夹会看到两个文件:
```
id_rsa_github  id_rsa_github.pub
```
SSH-KEY生成了,接着给服务器和客户端配置SSH-KEY。

第一步把id_rsa_github.pub中的公钥内容添加到Git的SSH中,如果你使用Github或者Gitlib,在个人设置中会找到。
第二步为SSH配置私钥位置,这里和上面配置单个Git帐号不一样,不过单个帐号也可以按照多个帐号的配置方法来配置。
下面我们需要在.ssh文件夹新建一个名为config的文件,用它来配置多个SSH-KEY的管理。
Linux进入.ssh文件夹:cd ~/.ssh,新建config文件:touch config；或者:touch ~/.ssh/config。这里要注意,没有.ssh文件夹的要新建一个.ssh名的文件夹。
Window进入C:/Users/你的用户名/.ssh文件夹,右键新建一个文本文件,改名为config即可。这里要注意,没有.ssh文件夹的要新建一个.ssh名的文件夹。

下面来填写config文件的内容,我以Github、Gitlib、OSChina,局域网为例:
```
Host github.com
    HostName github.com
    User smallajax@foxmail.com
    PreferredAuthentications publickey
    IdentityFile /home/Workspace/ssh/id_rsa_github
Host gitlib.com
    HostName gitlib.com
    User smallajax@foxmail.com
    PreferredAuthentications publickey
    IdentityFile id_rsa_gitlib
Host oschina.com
    HostName oschina.com
    User smallajax@foxmail.com
    PreferredAuthentications publickey
    IdentityFile /D/Workspace/ssh/id_rsa_oschina
Host 192.168.1.222
    HostName 192.168.1.222
    User smallajax@foxmail.com
    PreferredAuthentications publickey
    IdentityFile /D/Workspace/ssh/id_rsa_oschina
```
解释一下,HostName是服务器的地址,User是用户名,PreferredAuthentications照抄即可,这里主要说的是IdentityFile,上面我们看到了三种情况,所以它的书写原则是:
填私钥文件的本地路径。
不论是Linux还是Windows都可以写相对路径,比如把id_rsa_xxx私钥文件放在.ssh文件夹下。
文件放在不同跟路径下时,需要写绝对路径 
Linux中没有放在.ssh文件夹内或者子文件夹。
Windows中没有放在C盘下时。注意据对路径变化,比如C盘下是/C/xo/abc、比如D盘下/D/ssh/id_rsa这样,还看不懂请参考上方例子。
拷贝完成后,把所有的id_rsa私钥文件添加到SSH-Agent,命令如下:
```
ssh-add id_rsa文件的路径
```
例如添加.ssh文件夹下的,Linux这样做:ssh-add ~/.ssh/id_rsa,如果你在.ssh文件夹下:ssh-add id_rsa即可,Windows同理。

最后,还剩下项目的用户和邮箱没有配置,和配个单个Git帐号的方式不同,这里我们需要为每个项目分别配置,所以要命令行进入仓库文件夹再设置。第一种情况是先从Git上pull仓库下来,第二种情况是本地初始化Git仓库,总之进入改仓库文件夹后:
```
git config --local user.name "你的名字"
git config --local user.email "你的邮箱"
```
不过麻烦的一点是如果是多个项目就需要挨个配置,不过我们一般是pull一个项目就配置一下,也仅仅需要配置一次即可。
注意配置单个Git帐号时,是不进入项目文件夹就可以,不过不是使用--local,而是使用--global就可以全局配置。
配置项目用户和邮箱完成后,我们可以进入项目文件夹下的.git文件夹查看config文件内容,大概内容如下:
```
...
[user]
    name = YanZhenjie
    email = smallajax@foxmail.com
```
此时配置全部结束,请查看下方测试SSH-KEY配置是否成功进行测试。如果配置成功,你就可以clone和commit了。

## 测试SSH-KEY配置是否成功

配置全部结束，我们来测试一下配置是否成功：

如果你是Github：
```
ssh -T git@github.com
```
如果是你Gitlib：
```
ssh -T git@gitlib.com
```
如果你是局域网192.168.1.222：
```
ssh -T git@192.168.1.222
```
其它自行举一反三吧。
此时需要输入刚才生成SSH-KEY时输入的私钥密码，输入后自行观察信息判断是否连接成功。

比如Github的信息是：
```
Hi yanzhenjie! You've successfully authenticated, but GitHub does not provide shell access.
```
比如Gitlib的信息是：
```
Welcome to GitLab, YanZhenjie!
```

添加SSH到SSH-Agent时报错

如果执行ssh-add ...命令提示如下错误：
```
Could not open a connection to your authentication agent.
```
那么请执行eval $(ssh-agent)命令后再重试，如果还不行，请再执行ssh-agent bash命令后重试。 
ref:
[http://blog.csdn.net/yanzhenjie1003/article/details/69487932?locationNum=4&fps=1](http://blog.csdn.net/yanzhenjie1003/article/details/69487932?locationNum=4&fps=1)


## 踩坑:
直接 clone git协议的链接，提示 permission denied..., 网友说不是自己建的库,git clone http: ,自己建的库 git clone git:
至于具体原理 ref: http://blog.csdn.net/liangpz521/article/details/21534849
ran@ranux:~/Documents/xxx_src$ git clone git@git.xxx.com:xxx/xxx-service-wechat.git
Cloning into 'xxx-service-wechat'...
The authenticity of host 'git.xxx.com (61.149.179.190)' can't be established.
RSA key fingerprint is SHA256:dk7bjq40xJ9oEFm4NS7Uo+lDvgVPilONMLheB6suFB0.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added 'git.xxx.com,61.149.179.190' (RSA) to the list of known hosts.
git@git.xxx.com's password: 
Permission denied, please try again.
git@git.xxx.com's password: 
Connection to git.xxx.com closed by remote host.
fatal: Could not read from remote repository.

Please make sure you have the correct access rights
and the repository exists.
ran@ranux:~/Documents/xxx_src$ git clone git@git.xxx.com:xxx/xxx-service-wechat.git
Cloning into 'xxx-service-wechat'...
The authenticity of host 'git.xxx.com (61.149.179.190)' can't be established.
RSA key fingerprint is SHA256:dk7bjq40xJ9oEFm4NS7Uo+lDvgVPilONMLheB6suFB0.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added 'git.xxx.com,61.149.179.190' (RSA) to the list of known hosts.
git@git.xxx.com's password: 
Permission denied, please try again.
git@git.xxx.com's password: 

ran@ranux:~/Documents/xxx_src$ git clone http://git.xxx.com/xxx/xxx-service-wechat.git
Cloning into 'xxx-service-wechat'...
Username for 'http://git.xxx.com': xxx@xxx.com
Password for 'http://xxx@xxx.com@git.xxx.com': 
fatal: Authentication failed for 'http://git.xxx.com/xxx/xxx-service-wechat.git/'
ran@ranux:~/Documents/xxx_src$ git clone http://git.xxx.com/xxx/xxx-service-wechat.git
Cloning into 'xxx-service-wechat'...
Username for 'http://git.xxx.com': xxx
Password for 'http://xxx@git.xxx.com': 
remote: Counting objects: 825, done.
remote: Compressing objects: 100% (330/330), done.
remote: Total 825 (delta 276), reused 739 (delta 256)
Receiving objects: 100% (825/825), 178.90 KiB | 0 bytes/s, done.
Resolving deltas: 100% (276/276), done.
Checking connectivity... done.
