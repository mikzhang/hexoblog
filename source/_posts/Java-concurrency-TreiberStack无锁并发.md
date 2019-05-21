---
title: Java-TreiberStack无锁并发
date: 2017-09-22 00:00:00
categories: Java
tags:
    - Java
    - TreiberStack
    - concurrency
---

并发访问的安全性通常有Lock（同步）或者CAS方式实现，其中CAS是无锁（lock-free）并发的基础理念；本文主要简述一下通过Treiber Stack（1986，R.Kent Treiber）实现一个无锁并发栈，其主要思想就是使用CAS原子性的操作栈顶（或者栈底，单端队列），根据其思想，我们可以创造出更多有意义的实现。

<!-- more -->

其中在JAVA中，FutureTask.WaitNode是典型的Treiber Stack实现；此外，Fork/Join框架中WorkQueue的实现中借鉴了此思想。

我们展示一下，Treiber Stack的典型示例：

```
import java.util.concurrent.atomic.AtomicReference;  
  
/** 
 * 一个基于CAS实现的无锁（lock-free）并发栈 
 **/  
public class TreiberStack <E> {  
    private AtomicReference<Node<E>> top = new AtomicReference<Node<E>>();  
  
    /** 
     * 添加到栈顶 
     * @param item 
     */  
    public void push(E item) {  
        Node<E> header = new Node<E>(item);  
        Node<E> currentHead;  
        do {  
            currentHead = top.get();  
            header.next = currentHead;  
        } while (!top.compareAndSet(currentHead, header));  
    }  
  
    /** 
     * 弹出栈顶 
     * @return 
     */  
    public E pop() {  
        Node<E> currentHead;  
        Node<E> header;  
        do {  
            currentHead = top.get();  
            if (currentHead == null)  
                return null;  
            header = currentHead.next;  
        } while (!top.compareAndSet(currentHead, header));  
        return currentHead.item;  
    }  
  
    private static class Node <E> {  
        public final E item;  
        public Node<E> next;  
  
        public Node(E item) {  
            this.item = item;  
        }  
    }  
}  
```

谈到CAS，我们绕不开ABA的问题，如果你能够预测ABA发生的概率较低或者ABA发生时并不会对数据结果产生错误，我们可以认为ABA是无害的。其实面对ABA问题时，如果考虑性能开销，我们也没有特别有效的解决办法

ref:
https://shift-alt-ctrl.iteye.com/blog/2432169
