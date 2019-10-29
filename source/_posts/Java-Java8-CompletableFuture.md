---
title: Java-Java8-CompletableFuture
date: 2017-09-22 00:00:00
categories: Java
tags:
    - Java
---



Future基础知识：[Java并发（6）带返回结果的任务执行](http://www.cnblogs.com/shijiaqi1066/p/3412331.html)
Guava的Future：[Guava Future](http://www.cnblogs.com/shijiaqi1066/p/5745295.html)
Netty的Future：[Netty Future与Promise](http://www.cnblogs.com/shijiaqi1066/p/4804875.html)

**异步编排CompletableFuture**
CompletableFuture是JDK8提供的Future增强类。CompletableFuture异步任务执行线程池，默认是把异步任务都放在ForkJoinPool中执行。

官方文档：
https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/CompletableFuture.html
https://docs.oracle.com/javase/9/docs/api/java/util/concurrent/CompletableFuture.html

CompletableFuture接口提供了非常多的方法用于编排异步任务基本每个方法都有两套方法，Async版本的函数与非Async版本的函数。

若方法不以Async结尾，意味着Action使用相同的线程执行，而Async可能会使用其它的线程去执行(如果使用相同的线程池，也可能会被同一个线程选中执行)。

<!-- more -->

## 创建CompletableFuture

```
public static <U> CompletableFuture<U> completedFuture(U value);

// 执行异步任务
public static <U> CompletableFuture<U> supplyAsync(Supplier<U> supplier);
public static <U> CompletableFuture<U> supplyAsync(Supplier<U> supplier, Executor executor);

// 执行异步任务
public static CompletableFuture<Void> runAsync(Runnable runnable);
public static CompletableFuture<Void> runAsync(Runnable runnable, Executor executor);
```

例：创建一个已经有结果值的CompletableFuture。
```
// 创建
CompletableFuture<String> future = CompletableFuture.completedFuture("a future value");
```

例：异步执行带返回值的异步任务。
```
CompletableFuture<String> future = CompletableFuture.supplyAsync(()->{
    System.out.println("带有返回值的异步任务");
    return "a future value";
});
```

例：异步执行不带返回值的异步任务
```
CompletableFuture<Void> future = CompletableFuture.runAsync(()->{
    System.out.println("不带返回值的异步任务");
});
```

## 获取CompletableFuture的返回值

```
public T get() throws InterruptedException, ExecutionException;
public T get(long timeout, TimeUnit unit) throws InterruptedException, ExecutionException, TimeoutException；
public T getNow(T valueIfAbsent)；
public T join();
```
说明：
get方法：阻塞获取CompletableFuture的结果值，另外可以设置该方法的阻塞时间。
getNow方法：如果结果已经计算完则返回结果或者抛出异常，否则返回给定的valueIfAbsent值。
join方法：返回计算的结果或者抛出一个unchecked异常(CompletionException)。

例：获取Future的结果值。
```
// 使用get
{
    CompletableFuture<String> future = CompletableFuture.completedFuture("a future value");
    String string = future.get();
    System.out.println(string);
}

// 使用join
{
    CompletableFuture<String> future = CompletableFuture.supplyAsync(()->{
        return "haha";
    });
 
    String join = future.join();
    System.out.println(join);
}
``` 

## 连接异步任务

完成完一个任务后继续执行一个异步任务

```
// thenRun 处理 Runnable
public CompletableFuture<Void> thenRun(Runnable action);
public CompletableFuture<Void> thenRunAsync(Runnable action);
public CompletableFuture<Void> thenRunAsync(Runnable action, Executor executor);

// thenAccept 处理 Consumer
public CompletableFuture<Void> thenAccept(Consumer<? super T> action);
public CompletableFuture<Void> thenAcceptAsync(Consumer<? super T> action);
public CompletableFuture<Void> thenAcceptAsync(Consumer<? super T> action, Executor executor);

// thenApply 处理 Function
public <U> CompletableFuture<U> thenApply(Function<? super T,? extends U> fn);
public <U> CompletableFuture<U> thenApplyAsync(Function<? super T,? extends U> fn);
public <U> CompletableFuture<U> thenApplyAsync(Function<? super T,? extends U> fn, Executor executor);

// handle 处理 BiFunction
public <U> CompletableFuture<U> handle(BiFunction<? super T, Throwable, ? extends U> fn);
public <U> CompletableFuture<U> handleAsync(BiFunction<? super T, Throwable, ? extends U> fn);
public <U> CompletableFuture<U> handleAsync(BiFunction<? super T, Throwable, ? extends U> fn, Executor executor);
```

例：thenRun方法。执行异步任务，执行完后再接一个异步任务。
```
CompletableFuture<Void> future = CompletableFuture.runAsync(()->{
    System.out.println("不带返回值的异步任务");
}).thenRun(()->{
    System.out.println("前一个future后，再异步执行任务。");
});
```

例：执行异步任务，并将结果给下一个异步任务，最后再返回结果值。
```
// 转换
CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> {
    return "a future value";
});
CompletableFuture<Integer> future1 = future.thenApplyAsync((str) -> {
    return str.length();
});

// 返回值
Integer join = future1.join();
System.out.println(join);
```

例：执行异步任务，并将结果给下一个异步任务，最后不返回结果值。
```
// 消费
CompletableFuture<String> future0 = CompletableFuture.completedFuture("a future value");
 
CompletableFuture<Void> future1 = future0.thenAcceptAsync((str)->{
    System.out.println("没有返回值。消费了字符串：" + str);
});
 
future1.join();
```


## 组合两个异步任务

### thenCompose方法
接着上一个CompletableFuture的结果执行一个异步任务，最新的异步任务返回一个新的CompletableFuture。

具体方法：
```
public <U> CompletableFuture<U> thenCompose(Function<? super T,? extends CompletionStage<U>> fn);
public <U> CompletableFuture<U> thenComposeAsync(Function<? super T,? extends CompletionStage<U>> fn);
public <U> CompletableFuture<U> thenComposeAsync(Function<? super T,? extends CompletionStage<U>> fn, Executor executor);
```

例：CompletableFuture后跟一个新的一步方法，产生新的CompletableFuture。
```
CompletableFuture<String> future = CompletableFuture
    .completedFuture(10)
    .thenComposeAsync((x)->{
        return CompletableFuture.supplyAsync(()-> x.toString());  // 新的ComplatableFuture
    }
);

// 获取结果
String r = future.join();
System.err.println(r); // 打印：10
```

### thenCombine方法
为两个CompletableFuture的结果值提供一个函数算子，将结果值计算出来。
```
[Task0] ---\
            ==>(fn)-->[Task]
[Task1] ---/
```
具体方法：
```
public <U,V> CompletableFuture<V> thenCombine(CompletionStage<? extends U> other, BiFunction<? super T,? super U,? extends V> fn);
public <U,V> CompletableFuture<V> thenCombineAsync(CompletionStage<? extends U> other, BiFunction<? super T,? super U,? extends V> fn);
public <U,V> CompletableFuture<V> thenCombineAsync(CompletionStage<? extends U> other, BiFunction<? super T,? super U,? extends V> fn, Executor executor);
```

例：定义两个Future组合起来的算子，并计算
```
CompletableFuture<Integer> f0 = CompletableFuture.completedFuture(10000);
CompletableFuture<String> f1 = CompletableFuture.completedFuture("hello");

CompletableFuture<String> future = f0.thenCombine(f1, (i, s)-> (s + i)); // 定义算子

// 获取结果值 
String r = future.join(); System.out.println(r); // 打印：hello10000
```

### Both系列方法
执行两个异步任务，并将两个任务的计算结果获取后，再执行一个异步任务，最后再返回值

thenAcceptBoth方法
将两个future的结果值传给第三个算子
```
public <U> CompletableFuture<Void> thenAcceptBoth(CompletionStage<? extends U> other, BiConsumer<? super T,? super U> action);
public <U> CompletableFuture<Void> thenAcceptBothAsync(CompletionStage<? extends U> other, BiConsumer<? super T,? super U> action);
public <U> CompletableFuture<Void> thenAcceptBothAsync(CompletionStage<? extends U> other, BiConsumer<? super T,? super U> action, Executor executor);
```
例：
```
CompletableFuture<Integer> f0 = CompletableFuture.supplyAsync(()->{
    try {
        Thread.sleep(1000*5);
    } catch (InterruptedException e) {
        e.printStackTrace();
    }
        return 2;
});
 
CompletableFuture<Integer> f1 = CompletableFuture.supplyAsync(()->{
    try {
        Thread.sleep(1000*2);
    } catch (InterruptedException e) {
        e.printStackTrace();
    }
    return 3;
});
 
// 提供一个异步算子。使用future的计算结果。
CompletableFuture<Void> f= f0.thenAcceptBothAsync(f1,(Integer x,Integer y) -> {
    System.out.println("两个future都完成，才计算算子。");
    System.out.println(x*y);
});
 
f.join();
```

runAfterBoth方法
等待之前的两个异步任务都结束，再执行Action。
```
public CompletableFuture<Void> runAfterBoth(CompletionStage<?> other,  Runnable action);
```

例：
```
CompletableFuture<Integer> f0 = CompletableFuture.supplyAsync(()->{
    try {
        Thread.sleep(1000*5);
    } catch (InterruptedException e) {
        e.printStackTrace();
    }
        return 2;
});
 
CompletableFuture<Integer> f1 = CompletableFuture.supplyAsync(()->{
    try {
        Thread.sleep(1000*2);
    } catch (InterruptedException e) {
        e.printStackTrace();
    }
    return 3;
});// 提供一个异步算子。使用future的计算结果。
CompletableFuture<Void> f = f0.runAfterBothAsync(f1, ()->{
    System.out.println("两个future都完成，再执行该任务。");
});

f.join();
```

### Either

runAfterEither方法
两个异步任务，任意一个CompletableFuture获取得到结果值，则执行该方法指定的Runnable 任务
```
public CompletionStage<Void> runAfterEither(CompletionStage<?> other,Runnable action);
public CompletionStage<Void> runAfterEitherAsync(CompletionStage<?> other,Runnable action);
public CompletionStage<Void> runAfterEitherAsync(CompletionStage<?> other,Runnable action,Executor executor);
```

例：
```
CompletableFuture<Integer> f0 = CompletableFuture.supplyAsync(()->{
    try {
        Thread.sleep(1000*5);
    } catch (InterruptedException e) {
        e.printStackTrace();
    }
    return 0;
});
 
CompletableFuture<Integer> f1 = CompletableFuture.supplyAsync(()->{
    try {
        Thread.sleep(1000*2);
    } catch (InterruptedException e) {
        e.printStackTrace();
    }
    return 1;
});
 

CompletableFuture<Void> f = f0.runAfterEither(f1, ()->{
    System.out.println("有一个任务完成了");
});

f.join();
```

applyToEither方法
两个异步任务，任意一个CompletableFuture获取得到结果值，则执行该方法指定的Function任务。
```
public <U> CompletableFuture<U> applyToEither(CompletionStage<? extends T> other, Function<? super T,U> fn);
public <U> CompletableFuture<U> applyToEitherAsync(CompletionStage<? extends T> other, Function<? super T,U> fn);
public <U> CompletableFuture<U> applyToEitherAsync(CompletionStage<? extends T> other, Function<? super T,U> fn, Executor executor);
```

例：
```
CompletableFuture<Integer> f0 = CompletableFuture.supplyAsync(()->{
    try {
        Thread.sleep(1000*5);
    } catch (InterruptedException e) {
        e.printStackTrace();
    }
    return 0;
});
 
CompletableFuture<Integer> f1 = CompletableFuture.supplyAsync(()->{
    try {
        Thread.sleep(1000*2);
    } catch (InterruptedException e) {
        e.printStackTrace();
    }
    return 1;
});

CompletableFuture<String> f = f0.applyToEither(f1, (Integer i)-> "task:" + i);
String r = f.join();
System.out.println(r);  // 打印：task:1
```

acceptEither方法
两个异步任务，任意一个CompletableFuture获取得到结果值，则执行该方法指定的Consumer任务。
```
public CompletableFuture<Void> acceptEither(CompletionStage<? extends T> other, Consumer<? super T> action);
public CompletableFuture<Void> acceptEitherAsync(CompletionStage<? extends T> other, Consumer<? super T> action);
public CompletableFuture<Void> acceptEitherAsync(CompletionStage<? extends T> other, Consumer<? super T> action, Executor executor);
```

例：
```
CompletableFuture<Integer> f0 = CompletableFuture.supplyAsync(()->{
    try {
        Thread.sleep(1000*5);
    } catch (InterruptedException e) {
        e.printStackTrace();
    }
    return 0;
});
 
CompletableFuture<Integer> f1 = CompletableFuture.supplyAsync(()->{
    try {
        Thread.sleep(1000*2);
    } catch (InterruptedException e) {
        e.printStackTrace();
    }
    return 1;
});

CompletableFuture<Void> f = f0.acceptEither(f1, (Integer i)->{
    System.out.println("task:" + i);  // 打印：task:1
});

f.join();
```

## 多个任务的组合

### anyOf方法
将多个CompletableFuture组合为一个CompletableFuture，任意一个CompletableFuture有了结果，则该方法的返回值也会得到结果。
```
public static CompletableFuture<Object> anyOf(CompletableFuture<?>... cfs);
```
例：三个CompletableFuture执行完一个就得到一个新的CompletableFuture
```
CompletableFuture<Integer> f0 = CompletableFuture.supplyAsync(()->{
    try {
        Thread.sleep(1000*1);
    } catch (InterruptedException e) {
        e.printStackTrace();
    }
    return 0;
});
 
CompletableFuture<Integer> f1 = CompletableFuture.supplyAsync(()->{
    try {
        Thread.sleep(1000*2);
    } catch (InterruptedException e) {
        e.printStackTrace();
    }
    return 1;
});

CompletableFuture<Integer> f2 = CompletableFuture.supplyAsync(()->{
    try {
        Thread.sleep(1000*3);
    } catch (InterruptedException e) {
        e.printStackTrace();
    }
    return 2;
});

long t0 = System.currentTimeMillis();

CompletableFuture<Object> f = CompletableFuture.anyOf(f0, f1, f2);
Object r = f.join();
System.out.println(r);   // 打印：0

long t1 = System.currentTimeMillis();
System.out.println((t1-t0)/1000);   // 打印：1
```

### allOf方法
将多个CompletableFuture组合为一个CompletableFuture，所有CompletableFuture有了结果，则该方法的返回值也会得到结果。
```
public static CompletableFuture<Void> allOf(CompletableFuture<?>... cfs);
```
例：三个CompletableFuture都执行完，就得到一个新的CompletableFuture
```
CompletableFuture<Integer> f0 = CompletableFuture.supplyAsync(()->{
    try {
        Thread.sleep(1000*1);
    } catch (InterruptedException e) {
        e.printStackTrace();
    }
    return 0;
});
 
CompletableFuture<Integer> f1 = CompletableFuture.supplyAsync(()->{
    try {
        Thread.sleep(1000*2);
    } catch (InterruptedException e) {
        e.printStackTrace();
    }
    return 1;
});

CompletableFuture<Integer> f2 = CompletableFuture.supplyAsync(()->{
    try {
        Thread.sleep(1000*3);
    } catch (InterruptedException e) {
        e.printStackTrace();
    }
    return 2;
});

long t0 = System.currentTimeMillis();

CompletableFuture<Void> f = CompletableFuture.allOf(f0, f1, f2);
f.join();

long t1 = System.currentTimeMillis();
System.out.println((t1-t0)/1000);   // 打印：3
```

## 完成时执行任务
当一系列的任务计算结果完成或者抛出异常的时候，我们可以执行指定的任务

```
public CompletableFuture<T> whenComplete(BiConsumer<? super T,? super Throwable> action);
public CompletableFuture<T> whenCompleteAsync(BiConsumer<? super T,? super Throwable> action);
public CompletableFuture<T> whenCompleteAsync(BiConsumer<? super T,? super Throwable> action, Executor executor);
```

例：任务完成后，执行最后的任务，并且可以获取最后任务之前的结果值。
```
CompletableFuture<Integer> future = CompletableFuture.supplyAsync(()->{
    try {
        Thread.sleep(5*1000);
    } catch (InterruptedException e) {
        throw new RuntimeException(e);
    }
    return new Random().nextInt(1000);
}).whenComplete((Integer i, Throwable t)->{
    System.out.println("任务结果值：" + i);
});

// 阻塞
future.get();
```

## 异常处理
使用CompletableFuture编排异步任务在处理异常的时候，有几种方式：

1. 在异步任务中使用try...catch...处理异常。
2. 使用whenComplate方法接收异常。
3. 使用exceptionally方法接收异常。

```
public CompletableFuture<T> exceptionally(Function<Throwable,? extends T> fn);
```
例：
```
CompletableFuture<String> f = CompletableFuture.supplyAsync(()->{
    return 100/0;
})
.exceptionally(ex -> {
    ex.printStackTrace();
    return 0;
}).thenApply((Integer i)-> "run:" + i.toString());

String r = f.join();
System.out.println(r);
```

打印：
```
java.util.concurrent.CompletionException: java.lang.ArithmeticException: / by zero
	at java.base/java.util.concurrent.CompletableFuture.encodeThrowable(Unknown Source)
	at java.base/java.util.concurrent.CompletableFuture.completeThrowable(Unknown Source)
	at java.base/java.util.concurrent.CompletableFuture$AsyncSupply.run(Unknown Source)
	at java.base/java.util.concurrent.CompletableFuture$AsyncSupply.exec(Unknown Source)
	at java.base/java.util.concurrent.ForkJoinTask.doExec(Unknown Source)
	at java.base/java.util.concurrent.ForkJoinPool.runWorker(Unknown Source)
	at java.base/java.util.concurrent.ForkJoinWorkerThread.run(Unknown Source)
Caused by: java.lang.ArithmeticException: / by zero
	at test.java/test.TestCompletableFuture.lambda$0(TestCompletableFuture.java:292)
	... 5 more
run:0
```

ref: https://www.cnblogs.com/shijiaqi1066/p/8758206.html
