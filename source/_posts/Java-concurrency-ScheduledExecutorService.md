---
title: Java-concurrency-ScheduledExecutorService
date: 2017-09-22 00:00:00
categories: Java
tags:
    - Java
    - concurrency
---

ScheduledExecutorService 是一个支持周期调度的线程池

<!-- more -->

ScheduledExecutorService 有3个方法执行定时任务：

- schedule(runnable, delay, unit)   单次延时任务
- scheduleAtFixedRate(runnable, initialDelay, period, unit)     循环任务, 按照上一次任务的发起时间作为开始时间计算下一次任务的开始时间
- scheduleWithFixedDelay(runnable, initialDelay, delay, unit)   循环任务, 是以上一次任务的结束时间作为开始时间计算下一次任务的开始时间

code:
```
ScheduledExecutorService mService = Executors.newScheduledThreadPool(5);
mService.schedule(new Runnable() {
    @Override
    public void run() {
        System.out.println("-------单次任务执行--------");
    }
}, 5, TimeUnit.SECONDS);

//1秒后执行线程，以后每隔5秒执行一次线程(线程开始时间开始计时）
mService.scheduleAtFixedRate(new Runnable() {
    @Override
    public void run() {
        System.out.println("-------定期任务执行--------");
    }
}, 1, 5, TimeUnit.SECONDS);

//1秒后执行线程，以后每隔6秒执行一次线程（线程结束时间开始计时）
mService.scheduleWithFixedDelay(new Runnable() {
    @Override
    public void run() {
        try {
            System.out.println("-------定期任务执行--------");
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}, 1, 5, TimeUnit.SECONDS);
```

总结:
- scheduleWithFixedDelay(runnable, initialDelay, delay, unit）第一次执行时间是initialDelay时间后，以后每次执行间隔是runnable任务执行完的时间加上delay的时间；
- scheduleAtFixedRate(runnable, initialDelay, period, unit)第一次执行时间是initialDelay时间后，以后每次执行间隔就是delay的时间，但这里有一种特殊情况，当period间隔的时间比runnable执行时间还要短的时候，period时间到了并不会立即执行，而是等runnable结束之后才立即执行下一次任务(可参考: https://www.jianshu.com/p/8c4c160ebdf7)


