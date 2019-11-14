---
title: Guava-ListenableFuture
date: 2017-09-22 00:00:00
categories: Java
tags:
    - Guava
---

Guava-ListenableFuture

<!-- more -->

jdk原生的 Future 已经提供了异步操作，但是不能直接回调。Guava 对 Future 进行了增强，核心接口就是ListenableFuture。如果已经开始使用了jdk8，可以直接学习使用原生的CompletableFuture

Guava 对jdk的异步增强可以通过看 MoreExecutor 和 Futures 两个类的源码入手，写的并不复杂，没有一层一层的调用，逻辑很清晰，建议读完本文通过这两个类由点到面的理解 Guava 到底做了什么

## ListenableFuture 

ListenableFuture 继承了 Future，额外新增了一个方法，listener 是任务结束后的回调方法，executor 是执行回调方法的执行器(通常是线程池)。Guava 中对 Future 的增强就是在 addListener 这个方法上进行了各种各样的封装，所以 addListener 是核心方法
```
void addListener(Runnable listener, Executor executor);
```

## ListenableFutureTask

jdk 原生 FutureTask 类是对 Future 接口的实现，Guava中 ListenableFutureTask 继承了 FutureTask 并实现了 ListenableFuture，Guava 异步回调最简单的使用：

```
//ListenableFutureTask通过静态create方法返回实例，还有一个重载方法，不太常用
ListenableFutureTask<String> task = ListenableFutureTask.create(new Callable<String>() {
    @Override
    public String call() throws Exception {
        return "";
    }
});
//启动任务
new Thread(task).start();
//增加回调方法，MoreExecutors.directExecutor()返回guava默认的Executor，执行回调方法不会新开线程，所有回调方法都在当前线程做(可能是主线程或者执行ListenableFutureTask的线程，具体可以看最后面的代码)。
//guava异步模块中参数有Executor的方法，一般还会有一个没有Executor参数的重载方法，使用的就是MoreExecutors.directExecutor()
task.addListener(new Runnable() {
    @Override
    public void run() {
        System.out.println("done");
    }
}, MoreExecutors.directExecutor());
//MoreExecutors.directExecutor()源码，execute方法就是直接运行，没有新开线程
public static Executor directExecutor() {
    return DirectExecutor.INSTANCE;
}

private enum DirectExecutor implements Executor {
    INSTANCE;

    @Override
    public void execute(Runnable command) {
        command.run();
    }

    @Override
    public String toString() {
        return "MoreExecutors.directExecutor()";
    }
}
```
一般使用异步模式的时候，都会用一个线程池来提交任务，不会像上面那样简单的开一个线程去做，那样效率太低下了，所以需要说说guava对jdk原生线程池的封装。guava对原生线程池的增强都在MoreExecutor类中，guava对ExecutorService和ScheduledExecutorService的增强类似，这里只介绍ExecutorService的增强

```
//真正干活的线程池
ThreadPoolExecutor poolExecutor = new ThreadPoolExecutor(
        5,
        5,
        0,
        TimeUnit.SECONDS,
        new ArrayBlockingQueue<>(100),
        new CustomizableThreadFactory("demo"),
        new ThreadPoolExecutor.DiscardPolicy());
//guava的接口ListeningExecutorService继承了jdk原生ExecutorService接口，重写了submit方法，修改返回值类型为ListenableFuture
ListeningExecutorService listeningExecutor = MoreExecutors.listeningDecorator(poolExecutor);

//获得一个随着jvm关闭而关闭的线程池，通过Runtime.getRuntime().addShutdownHook(hook)实现
//修改ThreadFactory为创建守护线程，默认jvm关闭时最多等待120秒关闭线程池，重载方法可以设置时间
ExecutorService newPoolExecutor = MoreExecutors.getExitingExecutorService(poolExecutor);

//只增加关闭线程池的钩子，不改变ThreadFactory
MoreExecutors.addDelayedShutdownHook(poolExecutor, 120, TimeUnit.SECONDS);
```
有了上面的学习，就可以真正使用guava的异步回调了
```
//像线程池提交任务，并得到ListenableFuture
ListenableFuture<String> listenableFuture = listeningExecutor.submit(new Callable<String>() {
    @Override
    public String call() throws Exception {
        return "";
    }
});
//可以通过addListener对listenableFuture注册回调，但是通常使用Futures中的工具方法
Futures.addCallback(listenableFuture, new FutureCallback<String>() {
    @Override
    public void onSuccess(String result) {

    }

    @Override
    public void onFailure(Throwable t) {

    }
});

/**
 * Futures.addCallback源码，其实就是包装了一层addListener，可以不加executor参数，使用上文说的DirectExecutor
 * 需要说明的是不加Executor的情况，只适用于轻型的回调方法，如果回调方法很耗时占资源，会造成线程阻塞
 * 因为DirectExecutor有可能在主线程中执行回调
 */
public static <V> void addCallback(final ListenableFuture<V> future, final FutureCallback<? super V> callback, Executor executor) {
    Preconditions.checkNotNull(callback);
    Runnable callbackListener =
            new Runnable() {
                @Override
                public void run() {
                    final V value;
                    try {
                        value = getDone(future);
                    } catch (ExecutionException e) {
                        callback.onFailure(e.getCause());
                        return;
                    } catch (RuntimeException e) {
                        callback.onFailure(e);
                        return;
                    } catch (Error e) {
                        callback.onFailure(e);
                        return;
                    }
                    callback.onSuccess(value);
                }
            };
    future.addListener(callbackListener, executor);
}
```
guava还提供了多个异步任务的链式执行方法，如果使用addListener实现大概是这样，会一层一层不断地套下去

```
ListenableFutureTask<String> task1 = ListenableFutureTask.create(new Callable<String>() {
    @Override
    public String call() throws Exception {
        return "";
    }
});
new Thread(task1).start();
task1.addListener(new Runnable() {
    @Override
    public void run() {
        ListenableFutureTask<String> task2 = ListenableFutureTask.create(new Callable<String>() {
            @Override
            public String call() throws Exception {
                return "";
            }
        });
        task2.addListener(new Runnable() {
            @Override
            public void run() {
                ...
            }
        }, MoreExecutors.directExecutor());
        new Thread(task2).start();
    }
}, MoreExecutors.directExecutor());
```
使用guava的异步链式执行
```
//当task1执行完毕会回调执行Function的apply方法，如果有task1有异常抛出，则task2也抛出相同异常，不执行apply
ListenableFuture<String> task2 = Futures.transform(task1, new Function<String, String>() {
    @Override
    public String apply(String input) {
        return "";
    }
});
ListenableFuture<String> task3 = Futures.transform(task2, new Function<String, String>() {
    @Override
    public String apply(String input) {
        return "";
    }
});
//处理最终的异步任务
Futures.addCallback(task3, new FutureCallback<String>() {
    @Override
    public void onSuccess(String result) {
        
    }

    @Override
    public void onFailure(Throwable t) {

    }
});
```

Futures.transform()和Futures.addCallback()都是对addListener做了封装，进行回调的设置，但是transform更适合用在链式处理的中间过程，addCallback更适合用在处理最终的结果上

## Futures.transform

Futures.transform()和Futures.transformAsync()的区别在于一个参数为Function，一个是AsyncFuntion，AsyncFuntion的apply方法返回值类型也是ListenableFuture，也就是回调方法也是异步的
transform和transformAsync不传入executor的方法已经被废弃准备删去了，不传入Executor时是哪个线程注意到任务结束了就在哪个线程执行回调方法，既可能是主线程，也可能是执行前一个任务的线程，这样会造成混乱。可以看下面代码

```
ListenableFutureTask<String> task1 = ListenableFutureTask.create(new Callable<String>() {
    @Override
    public String call() throws Exception {
        TimeUnit.SECONDS.sleep(5);
        System.out.println("task1 over" + new Date());
        return "";
    }
});
new Thread(task1).start();
//放开注释的话，上面的线程已经结束，所以是主线程执行回调方法，因此主线程会阻塞5s
//TimeUnit.SECONDS.sleep(6);
ListenableFuture<String> transform = Futures.transform(task1, new Function<String, String>() {
    @Override
    public String apply(String input) {
        try {
            TimeUnit.SECONDS.sleep(5);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        System.out.println("trans over" + new Date());
        //显示的是执行task1的线程
        System.out.println("trans over" + Thread.currentThread());
        return "";
    }
});
while (true) {
    TimeUnit.MILLISECONDS.sleep(200);
    System.out.println(new Date().toString() + Thread.currentThread());
}
```

ref:
[guava异步增强——ListenableFuture](https://www.jianshu.com/p/9c57aa5e34af)

