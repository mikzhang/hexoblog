---
title: Java-Lombok
date: 2017-09-22 00:00:00
categories: Java
tags:
    - Java
    - Lombok
---

以前的Java项目中，充斥着太多不友好的代码：POJO的getter/setter/toString；异常处理；I/O流的关闭操作等等，这些样板代码既没有技术含量，又影响着代码的美观，Lombok应运而生

<!-- more -->


## 引入相应的maven包

```
<dependency>
    <groupId>org.projectlombok</groupId>
    <artifactId>lombok</artifactId>
    <version>1.16.18</version>
    <scope>provided</scope>
</dependency>
```
Lombok的scope=provided，说明它只在编译阶段生效，不需要打入包中。事实正是如此，Lombok在编译期将带Lombok注解的Java文件正确编译为完整的Class文件。


## 添加IDE工具对Lombok的支持

IDEA中引入Lombok支持如下：
点击File-- Settings设置界面，安装Lombok插件
![snipaste_20190919110013.jpg](snipaste_20190919110013.jpg)

点击File-- Settings设置界面，开启 AnnocationProcessors：
![snipaste_20190919110114.jpg](snipaste_20190919110114.jpg)
开启该项是为了让Lombok注解在编译阶段起到作用


## Lombok实现原理

自从Java 6起，javac就支持“JSR 269 Pluggable Annotation Processing API”规范，只要程序实现了该API，就能在javac运行的时候得到调用。

Lombok就是一个实现了"JSR 269 API"的程序。在使用javac的过程中，它产生作用的具体流程如下：

1. javac对源代码进行分析，生成一棵抽象语法树(AST)
2. javac编译过程中调用实现了JSR 269的Lombok程序
3. 此时Lombok就对第一步骤得到的AST进行处理，找到Lombok注解所在类对应的语法树(AST)，然后修改该语法树(AST)，增加Lombok注解定义的相应树节点
4. javac使用修改后的抽象语法树(AST)生成字节码文件


## Lombok注解的使用


### POJO类常用注解

#### @Getter/@Setter
1. 作用类上，生成所有成员变量的getter/setter方法；
2. 作用于成员变量上，生成该成员变量的getter/setter方法。可以设定访问权限及是否懒加载等。

![snipaste_20190919110628.jpg](snipaste_20190919110628.jpg)

在Structure视图中，可以看到已经生成了getter/setter等方法
![snipaste_20190919110716.jpg](snipaste_20190919110716.jpg)

编译后的代码如下：[这也是传统Java编程需要编写的样板代码]
![Xnip20190919110855.png](Xnip20190919110855.png)

#### @Accessors
作用于类, 使 bean 支持链式风格
```
@Accessors(chain = true)
@Setter
@Getter
public class Student {
    private String name;
    private int age;
}
```
测试代码：
```
Student student = new Student()
        .setAge(24)
        .setName("zs");
```
这样就完成了一个对于 bean 来讲很友好的链式操作

#### @ToString
作用于类，覆盖默认的toString()方法，可以通过of属性限定显示某些字段，通过exclude属性排除某些字段
![snipaste_20190919111020.jpg](snipaste_20190919111020.jpg)

#### @EqualsAndHashCode
作用于类，覆盖默认的equals和hashCode

#### @NonNull
主要作用于成员变量和参数中，标识不能为空，否则抛出空指针异常。

#### @NoArgsConstructor, @RequiredArgsConstructor, @AllArgsConstructor
作用于类上，用于生成构造函数。有staticName、access等属性。

staticName属性一旦设定，将采用静态方法的方式生成实例，access属性可以限定访问权限。

**@NoArgsConstructor**
生成无参构造器；

**@RequiredArgsConstructor**
生成包含final和@NonNull注解的成员变量的构造器；

再回过头来看刚刚的 Student，很多时候，我们去写 Student 这个 bean 的时候，他会有一些必输字段，比如 Student 中的 name 字段，一般处理的方式是将 name 字段包装成一个构造方法，只有传入 name 这样的构造方法，才能创建一个 Student 对象。

接上上边的静态构造方法和必传参数的构造方法，使用 lombok 将更改成如下写法（@RequiredArgsConstructor 和 @NonNull）:
```
@Accessors(chain = true)
@Setter
@Getter
@RequiredArgsConstructor(staticName = "ofName")
public class Student {
    @NonNull private String name;
    private int age;
}
```
测试代码：
```
Student student = Student.ofName("zs");
```
这样构建出的 bean 语义是否要比直接 new 一个含参的构造方法(包含  name 的构造方法)要好很多。
当然他仍然是支持链式调用的：
```
Student student = Student.ofName("zs").setAge(24);
```

**@AllArgsConstructor**
生成全参构造器。

![snipaste_20190919111133.jpg](snipaste_20190919111133.jpg)

编译后结果：
![Xnip20190919111444.png](Xnip20190919111444.png)

#### @Data
作用于类上，是以下注解的集合：
- @ToString
- @EqualsAndHashCode
- @Getter
- @Setter
- @RequiredArgsConstructor

#### @Builder
作用于类上，将类转变为建造者模式

看一下 Student 这个类的原始 builder 状态:
```
@Getter
@Setter
public class Student {
    private String name;
    private int age;

    public static Builder builder(){
            return new Builder();
    }
    public static class Builder{
            private String name;
            private int age;
            public Builder name(String name){
                    this.name = name;
                    return this;
            }

            public Builder age(int age){
                    this.age = age;
                    return this;
            }

            public Student build(){
                    Student student = new Student();
                    student.setAge(age);
                    student.setName(name);
                    return student;
            }
    }
}
```
调用方式：
```
Student student = Student.builder().name("zs").age(24).build();
```
这样的 builder 代码，让我是在恶心难受，于是我打算用 lombok 重构这段代码：
```
@Builder
public class Student {
    private String name;
    private int age;
}
```
调用方式：
```
Student student = Student.builder().name("zs").age(24).build();
```

#### @Log
作用于类上，生成日志变量。针对不同的日志实现产品，有不同的注解：
![snipaste_20190919111720.jpg](snipaste_20190919111720.jpg)


### 其他重要注解

#### @Cleanup
自动关闭资源，针对实现了java.io.Closeable接口的对象有效，如：典型的IO流对象
![snipaste_20190919111821.jpg](snipaste_20190919111821.jpg)
编译后结果如下：
![snipaste_20190919111856.jpg](snipaste_20190919111856.jpg)

#### @SneakyThrows
可以对受检异常进行捕捉并抛出，可以改写上述的main方法如下：
![snipaste_20190919112006.jpg](snipaste_20190919112006.jpg)

#### @Synchronized
作用于方法级别，可以替换synchronize关键字或lock锁，用处不大。


ref:
[IDEA中用好Lombok，撸码效率至少提升5倍](https://mp.weixin.qq.com/s?__biz=MzI3NjU2ODA5Mg==&mid=2247484565&idx=2&sn=6cc229f530f3961f80d9f1208deff427&scene=21#wechat_redirect)

