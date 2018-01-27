---
title: Java-Mockito
date: 2017-09-01 09:38:16
categories: Java
tags:
    - Java
    - Mockito
---

Java Mockito learning experience.

<!-- more -->

## 引入 mockito-core 依赖

### gradle 方式:
```
repositories { jcenter() }
dependencies { testCompile "org.mockito:mockito-core:2.+" }
```

### Maven 方式:
```
<dependency>
    <groupId>org.mockito</groupId>
    <artifactId>mockito-core</artifactId>
    <version>2.13.0</version>
</dependency>
```

### 验证交互

```
import static org.mockito.Mockito.*;

// mock creation
List mockedList = mock(List.class);

// using mock object - it does not throw any "unexpected interaction" exception
mockedList.add("one");
mockedList.clear();

// selective, explicit, highly readable verification
verify(mockedList).add("one");
verify(mockedList).clear();
```

### 存根方法调用

```
// you can mock concrete classes, not only interfaces
LinkedList mockedList = mock(LinkedList.class);

// stubbing appears before the actual execution
when(mockedList.get(0)).thenReturn("first");

// the following prints "first"
System.out.println(mockedList.get(0));

// the following prints "null" because get(999) was not stubbed
System.out.println(mockedList.get(999));
```

ref:
http://site.mockito.org

