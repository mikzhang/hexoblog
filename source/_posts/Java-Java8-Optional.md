---
title: Java-Java8-Optional
date: 2018-09-21 21:31:57
categories: Java
tags:
    - Java
    - Java8
    - Optional
---

Optional是Java8提供的为了解决null安全问题的一个API。善用Optional可以使我们代码中很多繁琐、丑陋的设计变得十分优雅。

<!-- more -->

使用Optional，我们就可以把下面这样的代码进行改写。
```
public static String getName(User u) {
    if (u == null)
        return "Unknown";
    return u.name;
}
```
不过，千万不要改写成这副样子。
```
public static String getName(User u) {
    Optional<User> user = Optional.ofNullable(u);
    if (!user.isPresent())
        return "Unknown";
    return user.get().name;
}
```
这样改写非但不简洁，而且其操作还是和第一段代码一样。无非就是用isPresent方法来替代u==null。这样的改写并不是Optional正确的用法，我们再来改写一次。
```
public static String getName(User u) {
    return Optional.ofNullable(u)
                    .map(user->user.name)
                    .orElse("Unknown");
}
```

这样才是正确使用Optional的姿势。那么按照这种思路，我们可以安心的进行链式调用，而不是一层层判断了。看一段代码：
```
public static String getChampionName(Competition comp) throws IllegalArgumentException {
    if (comp != null) {
        CompResult result = comp.getResult();
        if (result != null) {
            User champion = result.getChampion();
            if (champion != null) {
                return champion.getName();
            }
        }
    }
    throw new IllegalArgumentException("The value of param comp isn't available.");
}
```
由于种种原因（比如：比赛还没有产生冠军、方法的非正常调用、某个方法的实现里埋藏的大礼包等等），我们并不能开心的一路comp.getResult().getChampion().getName()到底。而其他语言比如kotlin，就提供了在语法层面的操作符加持：comp?.getResult()?.getChampion()?.getName()。所以讲道理在Java里我们怎么办！

让我们看看经过Optional加持过后，这些代码会变成什么样子。
```
public static String getChampionName(Competition comp) throws IllegalArgumentException {
    return Optional.ofNullable(comp)
            .map(c->c.getResult())
            .map(r->r.getChampion())
            .map(u->u.getName())
            .orElseThrow(()->new IllegalArgumentException("The value of param comp isn't available."));
}
```
这就很舒服了。Optional给了我们一个真正优雅的Java风格的方法来解决null安全问题。虽然没有直接提供一个操作符写起来短，但是代码看起来依然很爽很舒服。更何况?.这样的语法好不好看还见仁见智呢。

解决这种结构的深层嵌套路径是有点麻烦的。我们必须编写一堆 null 检查来确保不会导致一个 NullPointerException：
```
Outer outer = new Outer();
if (outer != null && outer.nested != null && outer.nested.inner != null) {
    System.out.println(outer.nested.inner.foo);
}
```
我们可以通过利用 Java 8 的 Optional 类型来摆脱所有这些 null 检查。map 方法接收一个 Function 类型的 lambda 表达式，并自动将每个 function 的结果包装成一个 Optional 对象。这使我们能够在一行中进行多个 map 操作。Null 检查是在底层自动处理的。
```
Optional.of(new Outer())
    .map(Outer::getNested)
    .map(Nested::getInner)
    .map(Inner::getFoo)
    .ifPresent(System.out::println);
```
请记住，这种解决方案可能没有传统 null 检查那么高的性能。不过在大多数情况下不会有太大问题。

Optional的魅力还不止于此，Optional还有一些神奇的用法，比如Optional可以用来检验参数的合法性。
```
public void setName(String name) throws IllegalArgumentException {
    this.name = Optional.ofNullable(name).filter(User::isNameValid)
                        .orElseThrow(()->new IllegalArgumentException("Invalid username."));
}
```

存在即返回, 无则提供默认值
```
return user.orElse(null);  //而不是 return user.isPresent() ? user.get() : null;
return user.orElse(UNKNOWN_USER);
```
存在即返回, 无则由函数来产生
```
return user.orElseGet(() -> fetchAUserFromDatabase()); //而不要 return user.isPresent() ? user: fetchAUserFromDatabase();
```
存在才对它做点什么
```
user.ifPresent(System.out::println);
```

ref:
[Java8 如何正确使用 Optional](http://www.importnew.com/26066.html)
