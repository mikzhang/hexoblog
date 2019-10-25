---
title: Maven-dependencies-dependencyManagement
date: 2017-09-22 00:00:00
categories: Maven
tags:
    - Maven
---

Maven中的dependencyManagement 意义

<!-- more -->

1、在Maven中**dependencyManagement**的作用其实相当于一个对所依赖jar包进行**版本管理**的管理器。

2、pom.xml文件中，jar的版本判断的两种途径

1）如果dependencies里的dependency自己没有声明version元素，那么maven就会到dependencyManagement里面去找有没有对该artifactId和groupId进行过版本声明，如果有，就继承它，如果没有就会报错，告诉你必须为dependency声明一个version。

2）如果dependencies中的dependency声明了version，那么无论dependencyManagement中有无对该jar的version声明，都以dependency里的version为准。

3、
1）dependencies即使在子项目中不写该依赖项，那么子项目仍然会从父项目中继承该依赖项（全部继承）

2）dependencyManagement里只是声明依赖，并不实现引入，因此子项目需要显示的声明需要用的依赖。如果不在子项目中声明依赖，是不会从父项目中继承下来的；只有在子项目中写了该依赖项，并且没有指定具体版本，才会从父项目中继承该项，并且version和scope都读取自父pom;另外如果子项目中指定了版本号，那么会使用子项目中指定的jar版本。

4、如下
```
//只是对版本进行管理，不会实际引入jar 
<dependencyManagement> 
      <dependencies> 
            <dependency> 
                <groupId>org.springframework</groupId> 
                <artifactId>spring-core</artifactId> 
                <version>3.2.7</version> 
            </dependency> 
    </dependencies> 
</dependencyManagement> 
   
//会实际下载jar包 
<dependencies> 
       <dependency> 
                <groupId>org.springframework</groupId> 
                <artifactId>spring-core</artifactId> 
       </dependency> 
</dependencies>
```

ref: https://www.cnblogs.com/zhangmingcheng/p/10984036.html
