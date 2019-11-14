---
title: Guava-DirectExecutor
date: 2017-09-22 00:00:00
categories: Guava
tags:
    - Guava
---

DirectExecutor

<!-- more -->

源码
```
package com.google.common.util.concurrent;

import com.google.common.annotations.GwtCompatible;
import java.util.concurrent.Executor;

/**
 * An {@link Executor} that runs each task in the thread that invokes {@link Executor#execute
 * execute}.
 */
@GwtCompatible
enum DirectExecutor implements Executor {
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

文档的大意: DirectExecutor 是哪样一种Executor? 在调用execute的线程中执行每个任务, 并不会开启新线程。下面验证下。
```
import com.google.common.util.concurrent.MoreExecutors;
import java.util.concurrent.Executor;

public class DirectExecutorTest {

    public static void main(String[] args) {
        System.out.println("main thread: " + Thread.currentThread().getName());
        Executor executor = MoreExecutors.directExecutor();
        executor.execute(new Runnable() {
            @Override
            public void run() {
                System.out.println("current thread: "+Thread.currentThread().getName());
            }
        });
    }

    /* output:
    main thread: main
    current thread: main
     */
}
```

一般使用异步模式的时候，都会用一个线程池来提交任务，不会像上面那样简单的开一个线程去做，那样效率太低下了,故, Guava在很多场景并不推荐使用该executor
