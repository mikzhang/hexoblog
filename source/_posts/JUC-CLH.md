---
title: JUC-CLH
date: 2017-09-22 00:00:00
categories: JUC
tags:
    - CLH
    - Java
    - Thread
---

这篇我们来给大家聊聊AQS中核心同步队列（CLH）。

<!-- more -->

## 什么是同步队列（CLH）

### 同步队列

一个FIFO双向队列，队列中每个节点等待前驱节点释放共享状态（锁）被唤醒就可以了。

### AQS如何使用它？

AQS依赖它来完成同步状态的管理，当前线程如果获取同步状态失败时，AQS则会将当前线程已经等待状态等信息构造成一个节点（Node）并将其加入到CLH同步队列，同时会阻塞当前线程，当同步状态释放时，会把首节点唤醒（公平锁），使其再次尝试获取同步状态。

### Node节点面貌？

```
static final class Node {
        // 节点分为两种模式： 共享式和独占式
        /** 共享式 */
        static final Node SHARED = new Node();
        /** 独占式 */
        static final Node EXCLUSIVE = null;

        /** 等待线程超时或者被中断、需要从同步队列中取消等待（也就是放弃资源的竞争），此状态不会在改变 */
        static final int CANCELLED =  1;
        /** 后继节点会处于等待状态，当前节点线程如果释放同步状态或者被取消则会通知后继节点线程，使后继节点线程的得以运行 */
        static final int SIGNAL    = -1;
        /** 节点在等待队列中，线程在等待在Condition 上，其他线程对Condition调用singnal()方法后，该节点加入到同步队列中。 */
        static final int CONDITION = -2;
        /**
         * 表示下一次共享式获取同步状态的时会被无条件的传播下去。
         */
        static final int PROPAGATE = -3;

        /**等待状态*/
        volatile int waitStatus;

        /**前驱节点 */
        volatile Node prev;

        /**后继节点*/
        volatile Node next;

        /**获取同步状态的线程 */
        volatile Thread thread;

        /**链接下一个等待状态 */
        Node nextWaiter;
        
        // 下面一些方法就不贴了
    }
```

CLH同步队列的结构图
![253619634-5cbd6a30badb8_articlex.jpeg](253619634-5cbd6a30badb8_articlex.jpeg)
这里是基于CAS（保证线程的安全）来设置尾节点的。

## 入列操作
如上图了解了同步队列的结构， 我们在分析其入列操作在简单不过。无非就是将tail（使用CAS保证原子操作）指向新节点，新节点的prev指向队列中最后一节点（旧的tail节点），原队列中最后一节点的next节点指向新节点以此来建立联系，来张图帮助大家理解。

![1817013129-5cbd6a7a93674_articlex.jpeg](1817013129-5cbd6a7a93674_articlex.jpeg)

### 源码
源码我们可以通过AQS中的以下两个方法来了解下 

#### addWaiter方法

```
private Node addWaiter(Node mode) {
// 以给定的模式来构建节点， mode有两种模式 
//  共享式SHARED， 独占式EXCLUSIVE;
  Node node = new Node(Thread.currentThread(), mode);
    // 尝试快速将该节点加入到队列的尾部
    Node pred = tail;
     if (pred != null) {
        node.prev = pred;
            if (compareAndSetTail(pred, node)) {
                pred.next = node;
                return node;
            }
        }
        // 如果快速加入失败，则通过 anq方式入列
        enq(node);
        return node;
    }
```

先通过addWaiter(Node node)方法尝试快速将该节点设置尾成尾节点，设置失败走enq(final Node node)方法

#### enq
```
private Node enq(final Node node) {
// CAS自旋，直到加入队尾成功        
for (;;) {
    Node t = tail;
        if (t == null) { // 如果队列为空，则必须先初始化CLH队列，新建一个空节点标识作为Hader节点,并将tail 指向它
            if (compareAndSetHead(new Node()))
                tail = head;
            } else {// 正常流程，加入队列尾部
                node.prev = t;
                    if (compareAndSetTail(t, node)) {
                        t.next = node;
                        return t;
                }
            }
        }
    }

```
通过“自旋”也就是死循环的方式来保证该节点能顺利的加入到队列尾部，只有加入成功才会退出循环，否则会一直循序直到成功。

上述两个方法都是通过compareAndSetHead(new Node())方法来设置尾节点，以保证节点的添加的原子性（保证节点的添加的线程安全。）

## 出列操作
同步队列（CLH）遵循FIFO，首节点是获取同步状态的节点，首节点的线程释放同步状态后，将会唤醒它的后继节点（next），而后继节点将会在获取同步状态成功时将自己设置为首节点，这个过程非常简单。如下图

![2751180000-5cbd6b431be55_articlex.jpeg](2751180000-5cbd6b431be55_articlex.jpeg)
设置首节点是通过获取同步状态成功的线程来完成的（获取同步状态是通过CAS来完成），只能有一个线程能够获取到同步状态，因此设置头节点的操作并不需要CAS来保证，只需要将首节点设置为其原首节点的后继节点并断开原首节点的next（等待GC回收）应用即可。

## 总结
聊完后我们来总一下，同步队列就是一个FIFO双向对队列，其每个节点包含获取同步状态失败的线程应用、等待状态、前驱节点、后继节点、节点的属性类型以及名称描述。

其入列操作也就是利用CAS(保证线程安全)来设置尾节点，出列就很简单了直接将head指向新头节点并断开老头节点联系就可以了。

ref: 
https://segmentfault.com/a/1190000018948010
