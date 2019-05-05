---
title: Java-concurrency-ReentrantLock
date: 2017-09-22 00:00:00
categories: Java
tags:
    - Java
    - concurrency
---

可重入锁ReentrantLock的实现原理以及源码分析。

<!-- more -->

## 什么是重入锁

可重入锁 ReentrantLock ，顾名思义，支持重新进入的锁，其表示该锁能支持一个线程对资源的重复加锁。

Java API 描述

```
一个可重入的互斥锁 Lock，它具有与使用 synchronized 方法和语句所访问的隐式监视器锁相同的一些基本行为和语义，但功能更强大。
ReentrantLock 将由最近成功获得锁，并且还没有释放该锁的线程所拥有。当锁没有被另一个线程所拥有时，调用 lock 的线程将成功获取该锁并返回。如果当前线程已经拥有该锁，此方法将立即返回。可以使用 isHeldByCurrentThread() 和 getHoldCount() 方法来检查此情况是否发生。
```

ReentrantLock还提供了公平锁和非公平锁的选择， 其构造方法接受一个公平参数（默认是非公平方式），当传入ture时表示公平锁， 否则为非公平锁。其两者的主要区别在于公平锁获取锁是有顺序的。但是其效率往往没有非公平锁的效率高，在多线程的访问时往往表现很低的吞吐量（即速度慢，常常急慢）。

![2121654773-5cc2624fcb3c3_articlex.jpeg}(2121654773-5cc2624fcb3c3_articlex.jpeg)

## 源码分析

我们先来看一段代码

```
ReentrantLock lock = new ReentrantLock();
try {
    lock.lock();
    // 业务代码
} finally {
    lock.unlock();
}
```

这一段代码相信学过Java的同学都非常熟悉了，今天我们就以此为入口一步一步的带你深入其底层世界。

共享状态的获取（锁的获取）
lock()方法

```
// ReentrantLock --> lokc() 实现Lock 接口的方法
public void lock() {
    // 调用内部类sync 的lock方法, 这里有两种实现，公平锁（FairSync）非公平锁（NonfairSync）这里我们来主要说 NonfairSync
    sync.lock();
}
```

ReentrantLock 的lock 方法， sync 为ReentrantLock的一个内部类，其继承了AbstractQueuedSynchronizer（AQS）, 他有两个子类公平锁FairSync 和非公平锁NonfairSync

ReentrantLock 中其中大部分的功能的实现都是委托给内部类Sync实现的，在Sync 中定义了abstract void lock() 留给子类去实现， 默认实现了final boolean nonfairTryAcquire(int acquires) 方法，可以看出其为非公平锁默认实现方式，下面我讲下给看下非公平锁lock方法。

NonfairSync.lock()

```
// ReentrantLock$NonfairSync
final void lock() {
    if (compareAndSetState(0, 1))
        // 非公平原则， 上来就插队来尝试下获取共享状态，如果成功则设置当前持有锁线程为自己，获取锁成功。
        setExclusiveOwnerThread(Thread.currentThread());
    else
        //如果失败则调用AQS中的acquire方法
        acquire(1);
}
```

首先就尝试获取同步状态（体现非公平锁上来就插队）如果成功则将持有锁线程设置为自己，失败则走AQS中的acquire方法。

AQS.acquire(int arg)

```
// AQS中的acquire方法，在AQS中已经讲过，首先会调用tryAcquire(arg)方法，tryAcquire(arg)方法会有具体由子类去实现。
public final void acquire(int arg) {
    if (!tryAcquire(arg) &&
        acquireQueued(addWaiter(Node.EXCLUSIVE), arg))
        selfInterrupt();
}
```

这里AQS中的源码我就不再过多的讲解了（无非就是尝试获取同步状态成功直接返回，失败加入同步队列等待被唤醒），主要来将留给子类实现的tryAcquire(arg)方法。
如有对AQS不明白的请看文章头中列出的几篇文章过一下或者锁搜引擎中锁搜下。

Nonfairync.tryAcquire(int acquires)

```
protected final boolean tryAcquire(int acquires) {
    // 非公平锁的tryAcquire(arg)实现，委托给Sync.nonfairTryAcquire(int acquires)具体处理
    return nonfairTryAcquire(acquires);
}
```

ReentrantLock中非公平锁tryAcquire(int acquires)的实现，具体调用其父类Sync中默认实现的（上面已经提过）。

Sync.nonfairTryAcquire(int acquires)

```
final boolean nonfairTryAcquire(int acquires) {
    final Thread current = Thread.currentThread();
    // 获取共享状态
    int c = getState();
    if (c == 0) {
        // 如果共享状态为0，说明锁空闲，利用CAS来获取锁（将共享状态值改为1）
        if (compareAndSetState(0, acquires)) {
            // 如果设置成功，则表明获取锁成功，将持有锁线程设置为自己
            setExclusiveOwnerThread(current);
            return true;
        }
    }
    // 如果c != 0 则说明锁已经被线程持有，判断持有锁的线程是不是自己（这里就是可重入锁的具体体现）
    else if (current == getExclusiveOwnerThread()) {
        // 如果当前持有锁的线程是自己，说明可重入，将共享状态值加1，返回ture
        int nextc = c + acquires;
        if (nextc < 0) // overflow
            throw new Error("Maximum lock count exceeded");
        setState(nextc);
        return true;
    }
    return false;
}
```

主要逻辑：

- 首先判断同步状态 state == 0 ?，
- 如果state == 0 则说明该锁处于空闲状态，直接通过CAS设置同步状态,成功将持有锁线程设置为自己返回ture，
- 如果state !=0 判断锁的持有者是否是自己，是则说明可重入将state 值加1 返回ture,
- 否则返回false.

来张图加深下理解

![2076618888-5cc261d0a1730_articlex.jpeg](2076618888-5cc261d0a1730_articlex.jpeg)

注：此图只是体现了RenntrantLock中的状态，其中涉及到AQS中的状态流转没有在这体现。

锁的释放
锁的释放逻辑就比较简单

ReentrantLock.unlock()

```
public void unlock() {
        sync.release(1);
    }
```

同样在ReentrantLock.unlock()方法中将具体释放逻辑委托给了内部类Sync来实现, 在这Sync 同样没有去实现release(1)而是使用其父类AQS的默认实现。

AQS.release(1)

```
// 调用AQS中的release 方法
public final boolean release(int arg) {
    if (tryRelease(arg)) {
        Node h = head;
        if (h != null && h.waitStatus != 0)
            unparkSuccessor(h);
        return true;
    }
    return false;
}
```

AQS释放锁的逻辑比较简单，同样就不解释了(无非就是释放锁，唤醒后继节点)具体来看下需要自类实现的tryRelease(arg) 释放共享状态的方法。

Sync.tryRelease(int releases)

```
protected final boolean tryRelease(int releases) {
    // 共享状态值减去releases
    int c = getState() - releases;
    // 如果持有锁的线程线程不是自己，则抛出异常（很好理解不能把别人的锁释放了）
    if (Thread.currentThread() != getExclusiveOwnerThread())
        throw new IllegalMonitorStateException();
    boolean free = false;
    // 共享状态 state = 0 则表明释放锁成功
    if (c == 0) {
        free = true;
        setExclusiveOwnerThread(null);
    }
    setState(c);
    return free;
}
```

释放共享状态（锁）的逻辑比较简单，主要是将共享状态的值减去releases，减后共享状态值为0表示释放锁成功将持有锁线程设置为null 返回 ture。

![3209737936-5cc261e70a714_articlex.jpeg](3209737936-5cc261e70a714_articlex.jpeg)

## 四、总结
最后我们来对ReentrantLock加锁和释放锁做个简单总结，ReentrantLock 是一个可重入锁提供了两种实现方式公平锁和非公平锁。
非公平锁获取锁流程：
1: 首先不管三七二一就来个 CAS 尝试获取锁。
2: 成功则皆大欢喜。
3: 失败，再次获取下共享状态（万一这会有人释放了尼）判断是否为0
4: 如果为0 则说明锁空闲，再次CAS获取锁成功将持有锁线程设置为自己并返回ture
5:不为0，判断持有者是否是自己、是自己表明可重入state + 1 返回ture 否则返回false（就去同步队列中排队去）。

非公平锁释放锁流程
很简单state - 1 = 0 则释放成功否则失败。

ref:
https://segmentfault.com/a/1190000018993293

这篇文章也不错：
https://segmentfault.com/a/119000001476995
