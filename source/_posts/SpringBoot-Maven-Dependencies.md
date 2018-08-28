---
title: SpringBoot-Maven-Dependencies
date: 2017-01-07 12:52:48
categories: SpringBoot
tags:
    - SpringBoot
---

SpringBoot 下 Maven 依赖关系

<!-- more -->

## 环境
- SpringBoot 2.0
- 项目 gs-rest-service (download from spring.io)

## 查看 SpringBoot 的依赖
借助 Maven Helper 插件, 查看步骤如下：
核心依赖 spring-boot-starter-web
![20180828170931](20180828170931.png)
查看依赖关系
![20180828171116](20180828171116.png)
![springboot_mvn_dependency](springboot_mvn_dependency.png)
![springboot_mvn_dependency_test](springboot_mvn_dependency_test.png)

或者使用 mvn:dependency:tree > tree.txt
```
[INFO] org.springframework:gs-rest-service:jar:0.1.0
[INFO] +- org.springframework.boot:spring-boot-starter-web:jar:2.0.3.RELEASE:compile
[INFO] |  +- org.springframework.boot:spring-boot-starter:jar:2.0.3.RELEASE:compile
[INFO] |  |  +- org.springframework.boot:spring-boot:jar:2.0.3.RELEASE:compile
[INFO] |  |  +- org.springframework.boot:spring-boot-autoconfigure:jar:2.0.3.RELEASE:compile
[INFO] |  |  +- org.springframework.boot:spring-boot-starter-logging:jar:2.0.3.RELEASE:compile
[INFO] |  |  |  +- ch.qos.logback:logback-classic:jar:1.2.3:compile
[INFO] |  |  |  |  \- ch.qos.logback:logback-core:jar:1.2.3:compile
[INFO] |  |  |  +- org.apache.logging.log4j:log4j-to-slf4j:jar:2.10.0:compile
[INFO] |  |  |  |  \- org.apache.logging.log4j:log4j-api:jar:2.10.0:compile
[INFO] |  |  |  \- org.slf4j:jul-to-slf4j:jar:1.7.25:compile
[INFO] |  |  +- javax.annotation:javax.annotation-api:jar:1.3.2:compile
[INFO] |  |  \- org.yaml:snakeyaml:jar:1.19:runtime
[INFO] |  +- org.springframework.boot:spring-boot-starter-json:jar:2.0.3.RELEASE:compile
[INFO] |  |  +- com.fasterxml.jackson.core:jackson-databind:jar:2.9.6:compile
[INFO] |  |  |  +- com.fasterxml.jackson.core:jackson-annotations:jar:2.9.0:compile
[INFO] |  |  |  \- com.fasterxml.jackson.core:jackson-core:jar:2.9.6:compile
[INFO] |  |  +- com.fasterxml.jackson.datatype:jackson-datatype-jdk8:jar:2.9.6:compile
[INFO] |  |  +- com.fasterxml.jackson.datatype:jackson-datatype-jsr310:jar:2.9.6:compile
[INFO] |  |  \- com.fasterxml.jackson.module:jackson-module-parameter-names:jar:2.9.6:compile
[INFO] |  +- org.springframework.boot:spring-boot-starter-tomcat:jar:2.0.3.RELEASE:compile
[INFO] |  |  +- org.apache.tomcat.embed:tomcat-embed-core:jar:8.5.31:compile
[INFO] |  |  +- org.apache.tomcat.embed:tomcat-embed-el:jar:8.5.31:compile
[INFO] |  |  \- org.apache.tomcat.embed:tomcat-embed-websocket:jar:8.5.31:compile
[INFO] |  +- org.hibernate.validator:hibernate-validator:jar:6.0.10.Final:compile
[INFO] |  |  +- javax.validation:validation-api:jar:2.0.1.Final:compile
[INFO] |  |  +- org.jboss.logging:jboss-logging:jar:3.3.2.Final:compile
[INFO] |  |  \- com.fasterxml:classmate:jar:1.3.4:compile
[INFO] |  +- org.springframework:spring-web:jar:5.0.7.RELEASE:compile
[INFO] |  |  \- org.springframework:spring-beans:jar:5.0.7.RELEASE:compile
[INFO] |  \- org.springframework:spring-webmvc:jar:5.0.7.RELEASE:compile
[INFO] |     +- org.springframework:spring-aop:jar:5.0.7.RELEASE:compile
[INFO] |     +- org.springframework:spring-context:jar:5.0.7.RELEASE:compile
[INFO] |     \- org.springframework:spring-expression:jar:5.0.7.RELEASE:compile
...
```
