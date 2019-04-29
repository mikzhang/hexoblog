---
title: Java-regularExpression
date: 2017-10-01 10:03:37
categories: Java
tags:
    - Java
    - regularExpression
---

Java 正则表达

<!-- more -->

## 概述

正则表达式通常用于两种功能：验证和搜索/替换。用于验证时，通常需要在前后分别加上^和$，以匹配整个待验证字符串。
java正则表达式通过java.util.regex包下的Pattern类与Matcher类实现。

- java.util.regex.Pattern 模式类：用来表示一个编译过的正则表达式
- java.util.regex.Matcher 匹配类：用模式匹配一个字符串所得到的结果

字符串的正则表达式必须首先被编译为Pattern的实例。然后，可将得到的模式用于创建 Matcher 对象

```
String str = "abc123";
String regex = "^[a-z]+[0-9]*";
Pattern p = Pattern.compile(regex);
Matcher matcher = p.matcher(str);
```

## Pattern类
pattern 对象是一个正则表达式的编译表示，要创建一个 Pattern 对象，你必须首先调用其公共静态编译方法，它返回一个 Pattern 对象。
public static Pattern compile(String regex, int flags);静态方法可以指定pattern对象的编译模式，常见模式：

- CASE_INSENSITIVE：大小写不敏感
_- MULTILINE：多行模式
_ LITERAL：模式字面值分析

## Matcher类
Matcher类提供如下三个匹配操作方法,三个方法均返回boolean类型,当匹配到时返回true,没匹配到则返回false

- matches 方法尝试将整个输入序列与该模式匹配
- lookingAt 尝试将输入序列从头开始与该模式匹配
- find 方法扫描输入序列以查找与该模式匹配的下一个子序列。

下面分别用示例分别解释每种方法：

### matcher.matches()方法
对整个字符串进行匹配,只有整个字符串都匹配了才返回true

```
Pattern p=Pattern.compile("\\d+");
Matcher m=p.matcher("22bb23");
m.matches();//返回false,因为bb不能被\d+匹配, 导致整个字符串匹配未成功. 
```

### matcher.lookingAt()方法
对前面的字符串进行匹配,只有匹配到的字符串在最前面才返回true

```
Pattern p=Pattern.compile("\\d+");
Matcher m=p.matcher("22bb23");
m.lookingAt();//返回true,因为\d+匹配到了前面的22Matcher
m2=p.matcher("aa2223");
m2.lookingAt();//返回false,因为\d+不能匹配前面的aa
```

##*# matcher.find()方法
对字符串进行匹配,匹配到的字符串可以在任何位置，另外find可以传入参数i表示匹配的起始位置

```
Pattern p=Pattern.compile("\\d+");
Matcher m=p.matcher("22bb23");
m.find();//返回true 
Matcher m2=p.matcher("aa2223");
m2.find();//返回true 
Matcher m4=p.matcher("aabb");
m4.find();//返回false 
```
在使用完上述三个方法以后，就可以使用.Mathcer.start()/ Matcher.end()/ Matcher.group()方法获取更详细的信息。

start()返回匹配到的子字符串在字符串中的索引位置
end()返回匹配到的子字符串的最后一个字符在字符串中的索引位置，最后一个字符的下标加1
group()返回匹配到的子字符串 （带参数表示第几组）

```
Pattern p=Pattern.compile("\\d+");
Matcher m2= p.matcher("aa2223ddd");
m2.find();//使用之后才能使用后面几个方法
m2.start();//2  匹配到“2223”
m2.end();//6
m2.group();//"2223"
```

## 组的概念
组是用括号划分的正则表达式，可以通过编号来引用组。组号从0开始，有几对小括号就表示有几个组，并且组可以嵌套。

```
A((B)C)(D)E正则式中有四组：组0是ABCDE，组1是BC，组2是B；组3是C，组4是D。（顺序从最左边括号开始计算,第0组默认是全部字符串）
```

start(),end(),group()均有一个重载方法它们是start(int i),end(int i),group(int i)专用于分组操作,Mathcer类还有一个groupCount()用于返回有多少组.
注意，只有使用了前面三个检测方法返回true后才可以使用上述三个详细方法，否则会引发一个IllegalStateException。


## 替换操作
常用替换方法如下：

- replaceFirst(String replacement)将字符串里，第一个与模式相匹配的子串替换成replacement
- replaceAll(String replacement)，将输入字符串里所有与模式相匹配的子串全部替换成replacement。
- appendReplacement(StringBuffer sb, String replacement) 将当前匹配子串替换为指定字符串，并且将替换后的子串以及其之前到上次匹配子串之后的字符串段添加到一个 StringBuffer 对象里
- appendTail(StringBuffer sb) 方法则将最后一次匹配工作后剩余的字符串添加到一个 StringBuffer 对象里。

### 使用技巧

```
String regex = "\\w(\\d\\d)(\\w+)";
String candidate = "x99SuperJava x98SuperJava";
while(m.find){
    int gc = matcher.groupCount();
    for (int i = 0; i <= gc; i++) {    
        System.out.println("group: " + i + ": " + matcher.group(i));
    }
    //从当前位置开始匹配，找到一个匹配的子串，将移动下次匹配的位置。

    //或者以下方式, 个人觉得方便, 如果不需要知道具体 group 的话
    System.out.println(matcher.group());
    
}
```
注意调用matches、lookAt、find进行匹配以后，无论成功失败，第二次匹配的位置都会改变，matcher.reset()可以重置会起始位置。

## \在正则特殊性
```
根据 Java Language Specification 的要求，Java 源代码的字符串中的反斜线被解释为 Unicode 转义或其他字符转义。因此必须在字符串字面值中使用两个反斜线，表示正则表达式受到保护，不被 Java 字节码编译器解释。
```
在正则表达式中有两类在java中使用需要\ \ 进行特殊保护处理（两个\ \目的就是消除其在字面值中的转义作用，转换为普通的\）

_- 一类是如\w(括下划线的任何单词字符)、\s（匹配任何空白字符）本身规定中含有\，其在java中写法就是“\ \w”
- 第二类自身是正则表达式的特殊字符比如？. * () 这类特殊字符如果想用其本身代表的含义需要用\ 进行转义（正则表达式中的规定和java字符串中字母值中转义重叠，所以为了消除字面量中的转义用两个\ \将其转换为普通的\），其在java中使用“\ ?”如果没有转义\则会当做特殊字符处理（java编译期间会校验\后面是否可以字面值转义）
- 最后最特殊的\本身也是特殊字符，在java正则里面需要”\ \ \ \”才能展示

ref:
https://www.jianshu.com/p/07375050ae93

java正则表达式语法参考
http://docs.oracle.com/javase/6/docs/api/java/util/regex/Pattern.html
http://josh-persistence.iteye.com/blog/1881270
http://blog.jobbole.com/63398/
参考博客
http://a52071453.iteye.com/blog/1693040
http://josh-persistence.iteye.com/blog/1881270
http://www.voidcn.com/blog/zhoumingsong123/article/p-4417764.html
