---
title: Java-HashMap-hash
date: 2017-09-22 00:00:00
categories: Java
tags:
    - Java
    - HashMap
---

看HashMap 源码时, 发现 hash 的算法很巧妙, 特记录之

<!-- more -->

为什么要有HashMap的hash()方法，难道不能直接使用KV中K原有的hash值吗？在HashMap的put、get操作时为什么不能直接使用K中原有的hash值
```
    /**
     * Computes key.hashCode() and spreads (XORs) higher bits of hash
     * to lower.  Because the table uses power-of-two masking, sets of
     * hashes that vary only in bits above the current mask will
     * always collide. (Among known examples are sets of Float keys
     * holding consecutive whole numbers in small tables.)  So we
     * apply a transform that spreads the impact of higher bits
     * downward. There is a tradeoff between speed, utility, and
     * quality of bit-spreading. Because many common sets of hashes
     * are already reasonably distributed (so don't benefit from
     * spreading), and because we use trees to handle large sets of
     * collisions in bins, we just XOR some shifted bits in the
     * cheapest possible way to reduce systematic lossage, as well as
     * to incorporate impact of the highest bits that would otherwise
     * never be used in index calculations because of table bounds.
     */
    static final int hash(Object key) {
        int h;
        return (key == null) ? 0 : (h = key.hashCode()) ^ (h >>> 16);
    }
```
从上面的代码可以看到key的hash值的计算方法。key的hash值高16位不变，低16位与高16位异或作为key的最终hash值。（h >>> 16，表示无符号右移16位，高位补0，任何数跟0异或都是其本身，因此key的hash值高16位不变。）

![Snipaste20190703181705.png](Snipaste20190703181705.png)

为什么要这么干呢？ 
这个与HashMap中table下标的计算有关。

```
n = table.length;
index = （n-1） & hash;
```

因为，table的长度都是2的幂，因此index仅与hash值的低n位有关（此n非table.leng，而是2的幂指数），hash值的高位都被与操作置为0了。 
假设table.length=2^4=16

![Snipaste20190703181844.png](Snipaste20190703181844.png)

由上图可以看到，只有hash值的低4位参与了运算。 
这样做很容易产生碰撞。设计者权衡了speed, utility, and quality，将高16位与低16位异或来减少这种影响。设计者考虑到现在的hashCode分布的已经很不错了，而且当发生较大碰撞时也用树形存储降低了冲突。仅仅异或一下，既减少了系统的开销，也不会造成的因为高位没有参与下标的计算(table长度比较小时)，从而引起的碰撞

ref:
https://blog.csdn.net/fan2012huan/article/details/51097331 
