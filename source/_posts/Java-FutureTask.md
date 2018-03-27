---
title: Java-FutureTask
date: 2017-10-09 00:00:00
categories: Java
tags:
    - Java
    - FutureTask
---

深入学习 FutureTask

<!-- more -->

## 第一部分:What
在Java中一般通过继承Thread类或者实现Runnable接口这两种方式来创建多线程,但是这两种方式都有个缺陷,就是不能在执行完成后获取执行的结果,因此Java 1.5之后提供了Callable和Future接口,通过它们就可以在任务执行完毕之后得到任务的执行结果。本文会简要的介绍使用方法,然后会从源代码角度分析下具体的实现原理。
本文以Java 1.7的代码进行分析。

## 第二部分:How

### Callable接口

对于需要执行的任务需要实现Callable接口,Callable接口定义如下:
```java
public interface Callable<V> {
    /**
     * Computes a result, or throws an exception if unable to do so.
     *
     * @return computed result
     * @throws Exception if unable to compute a result
     */
    V call() throws Exception;
}
```
可以看到Callable是个泛型接口,泛型V就是要call()方法返回的类型。Callable接口和Runnable接口很像,都可以被另外一个线程执行,但是正如前面所说的,Runnable不会返回数据也不能抛出异常。

### Future接口

Future接口代表异步计算的结果,通过Future接口提供的方法可以查看异步计算是否执行完成,或者等待执行结果并获取执行结果,同时还可以取消执行。Future接口的定义如下:
```java
public interface Future<V> {
    boolean cancel(boolean mayInterruptIfRunning);
    boolean isCancelled();
    boolean isDone();
    V get() throws InterruptedException, ExecutionException;
    V get(long timeout, TimeUnit unit)
        throws InterruptedException, ExecutionException, TimeoutException;
}
```

- cancel():cancel()方法用来取消异步任务的执行。如果异步任务已经完成或者已经被取消,或者由于某些原因不能取消,则会返回false。如果任务还没有被执行,则会返回true并且异步任务不会被执行。如果任务已经开始执行了但是还没有执行完成,若mayInterruptIfRunning为true,则会立即中断执行任务的线程并返回true,若mayInterruptIfRunning为false,则会返回true且不会中断任务执行线程。
- isCanceled():判断任务是否被取消,如果任务在结束(正常执行结束或者执行异常结束)前被取消则返回true,否则返回false。
- isDone():判断任务是否已经完成,如果完成则返回true,否则返回false。需要注意的是:任务执行过程中发生异常、任务被取消也属于任务已完成,也会返回true。
- get():获取任务执行结果,如果任务还没完成则会阻塞等待直到任务执行完成。如果任务被取消则会抛出CancellationException异常,如果任务执行过程发生异常则会抛出ExecutionException异常,如果阻塞等待过程中被中断则会抛出InterruptedException异常。
- get(long timeout,Timeunit unit):带超时时间的get()版本,如果阻塞等待过程中超时则会抛出TimeoutException异常。

### FutureTask

Future只是一个接口,不能直接用来创建对象,FutureTask是Future的实现类,
FutureTask的继承图如下:
{% asset_img 728ad60436305482476012b9ac99c699.png %}
可以看到,FutureTask实现了RunnableFuture接口,则RunnableFuture接口继承了Runnable接口和Future接口,所以FutureTask既能当做一个Runnable直接被Thread执行,也能作为Future用来得到Callable的计算结果。

FutureTask一般配合ExecutorService来使用,也可以直接通过Thread来使用。
```java
package com.beautyboss.slogen.callback;
 
import java.util.concurrent.*;
 
public class CallDemo {
 
    public static void main(String[] args) throws ExecutionException, InterruptedException {
 
        /**
         * 第一种方式:Future + ExecutorService
         * Task task = new Task();
         * ExecutorService service = Executors.newCachedThreadPool();
         * Future<Integer> future = service.submit(task1);
         * service.shutdown();
         */
 
 
        /**
         * 第二种方式: FutureTask + ExecutorService
         * ExecutorService executor = Executors.newCachedThreadPool();
         * Task task = new Task();
         * FutureTask<Integer> futureTask = new FutureTask<Integer>(task);
         * executor.submit(futureTask);
         * executor.shutdown();
         */
 
        /**
         * 第三种方式:FutureTask + Thread
         */
 
        // 2. 新建FutureTask,需要一个实现了Callable接口的类的实例作为构造函数参数
        FutureTask<Integer> futureTask = new FutureTask<Integer>(new Task());
        // 3. 新建Thread对象并启动
        Thread thread = new Thread(futureTask);
        thread.setName("Task thread");
        thread.start();
 
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
 
        System.out.println("Thread [" + Thread.currentThread().getName() + "] is running");
 
        // 4. 调用isDone()判断任务是否结束
        if(!futureTask.isDone()) {
            System.out.println("Task is not done");
            try {
                Thread.sleep(2000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
        int result = 0;
        try {
            // 5. 调用get()方法获取任务结果,如果任务没有执行完成则阻塞等待
            result = futureTask.get();
        } catch (Exception e) {
            e.printStackTrace();
        }
 
        System.out.println("result is " + result);
 
    }
 
    // 1. 继承Callable接口,实现call()方法,泛型参数为要返回的类型
    static class Task  implements Callable<Integer> {
 
        @Override
        public Integer call() throws Exception {
            System.out.println("Thread [" + Thread.currentThread().getName() + "] is running");
            int result = 0;
            for(int i = 0; i < 100;++i) {
                result += i;
            }
 
            Thread.sleep(3000);
            return result;
        }
    }
}
```

## 第三部分:Why

### 构造函数

先从FutureTask的构造函数看起,FutureTask有两个构造函数,其中一个如下:
```java
public FutureTask(Callable<V> callable) {
        if (callable == null)
            throw new NullPointerException();
        this.callable = callable;
        this.state = NEW;       // ensure visibility of callable
}
```
这个构造函数会把传入的Callable变量保存在this.callable字段中,该字段定义为private Callable<V> callable;用来保存底层的调用,在被执行完成以后会指向null,接着会初始化state字段为NEW。state字段用来保存FutureTask内部的任务执行状态,一共有7中状态,每种状态及其对应的值如下:
```java
private volatile int state;
private static final int NEW          = 0;
private static final int COMPLETING   = 1;
private static final int NORMAL       = 2;
private static final int EXCEPTIONAL  = 3;
private static final int CANCELLED    = 4;
private static final int INTERRUPTING = 5;
private static final int INTERRUPTED  = 6;
```

其中需要注意的是state是volatile类型的,也就是说只要有任何一个线程修改了这个变量,那么其他所有的线程都会知道最新的值。

为了后面更好的分析FutureTask的实现,这里有必要解释下各个状态。

- NEW:表示是个新的任务或者还没被执行完的任务。这是初始状态。
- COMPLETING:任务已经执行完成或者执行任务的时候发生异常,但是任务执行结果或者异常原因还没有保存到outcome字段(outcome字段用来保存任务执行结果,如果发生异常,则用来保存异常原因)的时候,状态会从NEW变更到COMPLETING。但是这个状态会时间会比较短,属于中间状态。
- NORMAL:任务已经执行完成并且任务执行结果已经保存到outcome字段,状态会从COMPLETING转换到NORMAL。这是一个最终态。
- EXCEPTIONAL:任务执行发生异常并且异常原因已经保存到outcome字段中后,状态会从COMPLETING转换到EXCEPTIONAL。这是一个最终态。
- CANCELLED:任务还没开始执行或者已经开始执行但是还没有执行完成的时候,用户调用了cancel(false)方法取消任务且不中断任务执行线程,这个时候状态会从NEW转化为CANCELLED状态。这是一个最终态。
- INTERRUPTING: 任务还没开始执行或者已经执行但是还没有执行完成的时候,用户调用了cancel(true)方法取消任务并且要中断任务执行线程但是还没有中断任务执行线程之前,状态会从NEW转化为INTERRUPTING。这是一个中间状态。
- INTERRUPTED:调用interrupt()中断任务执行线程之后状态会从INTERRUPTING转换到INTERRUPTED。这是一个最终态。

有一点需要注意的是,所有值大于COMPLETING的状态都表示任务已经执行完成(任务正常执行完成,任务执行异常或者任务被取消)。

各个状态之间的可能转换关系如下图所示:
{% asset_img 815ce1e16f6e67713e34c51046a91e3f.png %}

另外一个构造函数如下,
```java
public FutureTask(Runnable runnable, V result) {
        this.callable = Executors.callable(runnable, result);
        this.state = NEW;       // ensure visibility of callable
}
```
这个构造函数会把传入的Runnable封装成一个Callable对象保存在callable字段中,同时如果任务执行成功的话就会返回传入的result。这种情况下如果不需要返回值的话可以传入一个null。

顺带看下Executors.callable()这个方法,这个方法的功能是把Runnable转换成Callable,代码如下:
```java
public static <T> Callable<T> callable(Runnable task, T result) {
    if (task == null)
        throw new NullPointerException();
    return new RunnableAdapter<T>(task, result);
}
```
可以看到这里采用的是适配器模式,调用RunnableAdapter<T>(task, result)方法来适配,实现如下:
```java
static final class RunnableAdapter<T> implements Callable<T> {
    final Runnable task;
    final T result;
    RunnableAdapter(Runnable task, T result) {
        this.task = task;
        this.result = result;
    }
    public T call() {
        task.run();
        return result;
    }
}
```
这个适配器很简单,就是简单的实现了Callable接口,在call()实现中调用Runnable.run()方法,然后把传入的result作为任务的结果返回。

在new了一个FutureTask对象之后,接下来就是在另一个线程中执行这个Task,无论是通过直接new一个Thread还是通过线程池,执行的都是run()方法,接下来就看看run()方法的实现。

### run()

run()方法实现如下:
```java
public void run() {
    // 1. 状态如果不是NEW,说明任务或者已经执行过,或者已经被取消,直接返回
    // 2. 状态如果是NEW,则尝试把当前执行线程保存在runner字段中
    // 如果赋值失败则直接返回
    if (state != NEW ||
        !UNSAFE.compareAndSwapObject(this, runnerOffset,
                                     null, Thread.currentThread()))
        return;
    try {
        Callable<V> c = callable;
        if (c != null && state == NEW) {
            V result;
            boolean ran;
            try {
                // 3. 执行任务
                result = c.call();
                ran = true;
            } catch (Throwable ex) {
                result = null;
                ran = false;
                // 4. 任务异常
                setException(ex);
            }
            if (ran)
                // 4. 任务正常执行完毕
                set(result);
        }
    } finally {
        // runner must be non-null until state is settled to
        // prevent concurrent calls to run()
        runner = null;
        // state must be re-read after nulling runner to prevent
        // leaked interrupts
        int s = state;
        // 5. 如果任务被中断,执行中断处理
        if (s >= INTERRUPTING)
            handlePossibleCancellationInterrupt(s);
    }
}
```

run()方法首先会

1. 判断当前任务的state是否等于NEW,如果不为NEW则说明任务或者已经执行过,或者已经被取消,直接返回。
2. 如果状态为NEW则接着会通过unsafe类把任务执行线程引用CAS的保存在runner字段中,如果保存失败,则直接返回。
3. 执行任务。
4. 如果任务执行发生异常,则调用setException()方法保存异常信息。
setException()方法如下:
```java
protected void setException(Throwable t) {
    if (UNSAFE.compareAndSwapInt(this, stateOffset, NEW, COMPLETING)) {
        outcome = t;
        UNSAFE.putOrderedInt(this, stateOffset, EXCEPTIONAL); // final state
        finishCompletion();
    }
}
```
在setException()方法中
- 首先会CAS的把当前的状态从NEW变更为COMPLETING状态。
- 把异常原因保存在outcome字段中,outcome字段用来保存任务执行结果或者异常原因。
- CAS的把当前任务状态从COMPLETING变更为EXCEPTIONAL。这个状态转换对应着上图中的二。
- 调用finishCompletion()。关于这个方法后面在分析。

5. 如果任务成功执行则调用set()方法设置执行结果,该方法实现如下:
```java
protected void set(V v) {
    if (UNSAFE.compareAndSwapInt(this, stateOffset, NEW, COMPLETING)) {
        outcome = v;
        UNSAFE.putOrderedInt(this, stateOffset, NORMAL); // final state
        finishCompletion();
    }
}
```
这个方法跟上面分析的setException()差不多,
- 首先会CAS的把当前的状态从NEW变更为COMPLETING状态。
- 把任务执行结果保存在outcome字段中。
- CAS的把当前任务状态从COMPLETING变更为NORMAL。这个状态转换对应着上图中的一。
- 调用finishCompletion()。

发起任务线程跟执行任务线程通常情况下都不会是同一个线程,在任务执行线程执行任务的时候,任务发起线程可以查看任务执行状态、获取任务执行结果、取消任务等等操作,接下来分析下这些操作。

### get()

任务发起线程可以调用get()方法来获取任务执行结果,如果此时任务已经执行完毕则会直接返回任务结果,如果任务还没执行完毕,则调用方会阻塞直到任务执行结束返回结果为止。get()方法实现如下:
```java
public V get() throws InterruptedException, ExecutionException {
    int s = state;
    if (s <= COMPLETING)
        s = awaitDone(false, 0L);
    return report(s);
}
```
get()方法实现比较简单,会

1. 判断任务当前的state <= COMPLETING是否成立。前面分析过,COMPLETING状态是任务是否执行完成的临界状态。
2. 如果成立,表明任务还没有结束(这里的结束包括任务正常执行完毕,任务执行异常,任务被取消),则会调用awaitDone()进行阻塞等待。
3. 如果不成立表明任务已经结束,调用report()返回结果。

### awaitDone()

当调用get()获取任务结果但是任务还没执行完成的时候,调用线程会调用awaitDone()方法进行阻塞等待,该方法定义如下:
```java
private int awaitDone(boolean timed, long nanos)
        throws InterruptedException {
    // 计算等待截止时间
    final long deadline = timed ? System.nanoTime() + nanos : 0L;
    WaitNode q = null;
    boolean queued = false;
    for (;;) {
        // 1. 判断阻塞线程是否被中断,如果被中断则在等待队
        // 列中删除该节点并抛出InterruptedException异常
        if (Thread.interrupted()) {
            removeWaiter(q);
            throw new InterruptedException();
        }
 
        // 2. 获取当前状态,如果状态大于COMPLETING
        // 说明任务已经结束(要么正常结束,要么异常结束,要么被取消)
        // 则把thread显示置空,并返回结果
        int s = state;
        if (s > COMPLETING) {
            if (q != null)
                q.thread = null;
            return s;
        }
        // 3. 如果状态处于中间状态COMPLETING
        // 表示任务已经结束但是任务执行线程还没来得及给outcome赋值
        // 这个时候让出执行权让其他线程优先执行
        else if (s == COMPLETING) // cannot time out yet
            Thread.yield();
        // 4. 如果等待节点为空,则构造一个等待节点
        else if (q == null)
            q = new WaitNode();
        // 5. 如果还没有入队列,则把当前节点加入waiters首节点并替换原来waiters
        else if (!queued)
            queued = UNSAFE.compareAndSwapObject(this, waitersOffset,
                    q.next = waiters, q);
        else if (timed) {
            // 如果需要等待特定时间,则先计算要等待的时间
            // 如果已经超时,则删除对应节点并返回对应的状态
            nanos = deadline - System.nanoTime();
            if (nanos <= 0L) {
                removeWaiter(q);
                return state;
            }
            // 6. 阻塞等待特定时间
            LockSupport.parkNanos(this, nanos);
        }
        else
            // 6. 阻塞等待直到被其他线程唤醒
            LockSupport.park(this);
    }
}
```
awaitDone()中有个死循环,每一次循环都会

1. 判断调用get()的线程是否被其他线程中断,如果是的话则在等待队列中删除对应节点然后抛出InterruptedException异常。
2. 获取任务当前状态,如果当前任务状态大于COMPLETING则表示任务执行完成,则把thread字段置null并返回结果。
3. 如果任务处于COMPLETING状态,则表示任务已经处理完成(正常执行完成或者执行出现异常),但是执行结果或者异常原因还没有保存到outcome字段中。这个时候调用线程让出执行权让其他线程优先执行。
4. 如果等待节点为空,则构造一个等待节点WaitNode。
5. 如果第四步中新建的节点还没如队列,则CAS的把该节点加入waiters队列的首节点。
6. 阻塞等待。

假设当前state=NEW且waiters为NULL,也就是说还没有任何一个线程调用get()获取执行结果,这个时候有两个线程threadA和threadB先后调用get()来获取执行结果。再假设这两个线程在加入阻塞队列进行阻塞等待之前任务都没有执行完成且threadA和threadB都没有被中断的情况下(因为如果threadA和threadB在进行阻塞等待结果之前任务就执行完成或线程本身被中断的话,awaitDone()就执行结束返回了),执行过程是这样的,以threadA为例:

1. 第一轮for循环,执行的逻辑是q == null,所以这时候会新建一个节点q。第一轮循环结束。
2. 第二轮for循环,执行的逻辑是!queue,这个时候会把第一轮循环中生成的节点的netx指针指向waiters,然后CAS的把节点q替换waiters。也就是把新生成的节点添加到waiters链表的首节点。如果替换成功,queued=true。第二轮循环结束。
3. 第三轮for循环,进行阻塞等待。要么阻塞特定时间,要么一直阻塞知道被其他线程唤醒。

在threadA和threadB都阻塞等待之后的waiters结果如图
{% asset_img 92f6bbb0d4800bc528b2dacc1116e0d4.png %}

### cancel(boolean)

用户可以调用cancel(boolean)方法取消任务的执行,cancel()实现如下:
```java
public boolean cancel(boolean mayInterruptIfRunning) {
    // 1. 如果任务已经结束,则直接返回false
    if (state != NEW)
        return false;
    // 2. 如果需要中断任务执行线程
    if (mayInterruptIfRunning) {
        // 2.1. 把任务状态从NEW转化到INTERRUPTING
        if (!UNSAFE.compareAndSwapInt(this, stateOffset, NEW, INTERRUPTING))
            return false;
        Thread t = runner;
        // 2.2. 中断任务执行线程
        if (t != null)
            t.interrupt();
        // 2.3. 修改状态为INTERRUPTED
        UNSAFE.putOrderedInt(this, stateOffset, INTERRUPTED); // final state
    }
    // 3. 如果不需要中断任务执行线程,则直接把状态从NEW转化为CANCELLED
    else if (!UNSAFE.compareAndSwapInt(this, stateOffset, NEW, CANCELLED))
        return false;
    // 4. 
    finishCompletion();
    return true;
}
```

cancel()方法会做下面几件事:

1. 判断任务当前执行状态,如果任务状态不为NEW,则说明任务或者已经执行完成,或者执行异常,不能被取消,直接返回false表示执行失败。
2. 判断需要中断任务执行线程,则

- 把任务状态从NEW转化到INTERRUPTING。这是个中间状态。
- 中断任务执行线程。
- 修改任务状态为INTERRUPTED。这个转换过程对应上图中的四。

3. 如果不需要中断任务执行线程,直接把任务状态从NEW转化为CANCELLED。如果转化失败则返回false表示取消失败。这个转换过程对应上图中的四。
4. 调用finishCompletion()。

### finishCompletion()

根据前面的分析,不管是任务执行异常还是任务正常执行完毕,或者取消任务,最后都会调用finishCompletion()方法,该方法实现如下:
```java
private void finishCompletion() {
    // assert state > COMPLETING;
    for (WaitNode q; (q = waiters) != null;) {
        if (UNSAFE.compareAndSwapObject(this, waitersOffset, q, null)) {
            for (;;) {
                Thread t = q.thread;
                if (t != null) {
                    q.thread = null;
                    LockSupport.unpark(t);
                }
                WaitNode next = q.next;
                if (next == null)
                    break;
                q.next = null; // unlink to help gc
                q = next;
            }
            break;
        }
    }
 
    done();
 
    callable = null;        // to reduce footprint
}
```
这个方法的实现比较简单,依次遍历waiters链表,唤醒节点中的线程,然后把callable置空。
被唤醒的线程会各自从awaitDone()方法中的LockSupport.park()阻塞中返回,然后会进行新一轮的循环。在新一轮的循环中会返回执行结果(或者更确切的说是返回任务的状态)。

### report()

report()方法用在get()方法中,作用是把不同的任务状态映射成任务执行结果。实现如下:
```java
private V report(int s) throws ExecutionException {
    Object x = outcome;
    // 1. 任务正常执行完成,返回任务执行结果
    if (s == NORMAL)
        return (V)x;
    // 2. 任务被取消,抛出CancellationException异常
    if (s >= CANCELLED)
        throw new CancellationException();
    // 3. 其他状态,抛出执行异常ExecutionException
    throw new ExecutionException((Throwable)x);
}
```
映射关系如下图所示:
{% asset_img 137a6979a224d067b7b401ec072ca00f.png %}
如果任务处于NEW、COMPLETING和INTERRUPTING这三种状态的时候是执行不到report()方法的,所以没必要对这三种状态进行转换。

### get(long,TimeUnit)

带超时等待的获取任务结果,实现如下:
```java
public V get(long timeout, TimeUnit unit)
        throws InterruptedException, ExecutionException, TimeoutException {
    if (unit == null)
        throw new NullPointerException();
    int s = state;
    if (s <= COMPLETING &&
        // 如果awaitDone()超时返回之后任务还没结束,则抛出异常
        (s = awaitDone(true, unit.toNanos(timeout))) <= COMPLETING)
        throw new TimeoutException();
    return report(s);
}
```
跟get()不同点在于get(long,TimeUnit)会在awaitDone()超时返回之后抛出TimeoutException异常。

### isCancelled()和isDone()

这两个方法分别用来判断任务是否被取消和任务是否执行完成,实现都比较简单,代码如下:
```java
public boolean isCancelled() {
    return state >= CANCELLED;
}

public boolean isDone() {
    return state != NEW;
}
```

总结下,其实FutureTask的实现还是比较简单的,当用户实现Callable()接口定义好任务之后,把任务交给其他线程进行执行。FutureTask内部维护一个任务状态,任何操作都是围绕着这个状态进行,并随时更新任务状态。任务发起者调用get()获取执行结果的时候,如果任务还没有执行完毕,则会把自己放入阻塞队列中然后进行阻塞等待。当任务执行完成之后,任务执行线程会依次唤醒阻塞等待的线程。调用cancel()取消任务的时候也只是简单的修改任务状态,如果需要中断任务执行线程的话则调用Thread.interrupt()中断任务执行线程。

## 第四部分:Other

有个值得关注的问题就是当任务还在执行的时候用户调用cancel(true)方法能否真正让任务停止执行呢？
在前面的分析中我们直到,当调用cancel(true)方法的时候,实际执行还是Thread.interrupt()方法,而interrupt()方法只是设置中断标志位,如果被中断的线程处于sleep()、wait()或者join()逻辑中则会抛出InterruptedException异常。

因此结论是:cancel(true)并不一定能够停止正在执行的异步任务。

ref: [http://www.importnew.com/25286.html](http://www.importnew.com/25286.html)
