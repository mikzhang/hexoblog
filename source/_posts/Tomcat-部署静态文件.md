---
title: Tomcat-部署静态文件
date: 2017-10-09 00:00:00
categories: Tomcat
tags:
    - Tomcat
---

在 tomcat 部署静态文件

<!-- more -->

可以把文件直接放到webapps下面。当只是运行一个项目的时候,这种方法还好,但是当你涉及到两个以上项目的时候,就麻烦了。设定虚拟目录的方法,下面详细介绍。

配置虚拟目录也有两种方法,直接介绍我现在用的这种,直接在servler.xml里修改,毕竟经过了实践可用的,首先找到Tomcat下的conf文件夹下的server.xml

编辑server.xml,可以看到Host标签,默认就有一个,一个Host代表一个站点,找到Host结束标签,我们在这里配置虚拟路径

在</Host>的上面添加```<Context path="" docBase="" reloadable="" debug="" crossContext=""/>```,这里属性值都没有填写,下面填写属性值。
要填写属性值,我们要知道什么意思,对待知识就得不甚解。所以我这步没有直接填东西,填完你可能就直接似懂非懂的去用了。

Context指上下文,相信当你看到这步的时候,你一定没少接触过这个词。不赘述
path指虚拟目录,与浏览器访问的路径相关,如果直接是path="/",访问就是http://localhost:8080/XX.jsp,如果为空串,也是一样,如果加了项目名,访问路径也要加,如path="/home",访问就是http://localhost:8080/home/XX.jsp
docBase指实际存在路径,一般在硬盘里。如果我们的文件home直接放在了E盘下,那docBase=“E:\home”
reloadable指有文件更新时,是否重新加载,一般设置为true,设置为true后,不需重新启动,就能验证我们的改动,不过修改了java文件后,可以重新编译需要一小会,在IDE下的控制台里可以看见输出,一般没有输出滚动出来的时候,就可以了。这三个一般经常设置。

debug指等级,一般设置为debug=“0”,提供最少的信息。设不设置无大影响。
crossContext指是否可以互相使用上下文环境。这个我也是查了很久,一般不使用。网上搜到一个两个应用共享session的,有兴趣的同学可以看下。

