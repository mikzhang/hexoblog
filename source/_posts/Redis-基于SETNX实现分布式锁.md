---
title: Redis-基于SETNX实现分布式锁
date: 2017-09-22 00:00:00
categories: Redis
tags:
    - Redis
---

基于 Redis SETNX 实现分布式锁

<!-- more -->

## 环境与配置

- Redis 任意版本即可
- SpringBoot 任意版本即可，但是需要依赖 spring-boot-starter-data-redis
```
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-redis</artifactId>
</dependency>
```
## Redis 社区对 SETNX 的解释

```
Set key to hold string value if key does not exist. In that case, it is equal to SET. When key already holds a value, no operation is performed. SETNX is short for “SET if Not eXists”.
```

Return value: Integer reply, specifically:

- 1 if the key was set
- 0 if the key was not set

由于当某个 key 不存在的时候，SETNX 才会设置该 key。且由于 Redis 采用单进程单线程模型，所以，不需要担心并发的问题。那么，就可以利用 SETNX 的特性维护一个 key，存在的时候，即锁被某个线程持有；不存在的时候，没有线程持有锁。

## 关于实现的解释

由于只涉及到 Redis 的操作，所以，代码实现比较简单。只对外提供两个接口：获取锁、释放锁。

- IDistributedLock: 操作接口定义
- RedisLock: IDistributedLock 的实现类
- DistributedLockUtil: 分布式锁工具类
- SpringContextUtil: 获取当前 classpath 中的 Bean

SETNX 命令对应到 StringRedisTemplate 的 api 是 setIfAbsent，如下所示

```
/**
 * Set {@code key} to hold the string {@code value} if {@code key} is absent.
 *
 * @param key must not be {@literal null}.
 * @param value
 * @see <a href="http://redis.io/commands/setnx">Redis Documentation: SETNX</a>
 */
Boolean setIfAbsent(K key, V value);
```

## 源码和注释信息

```
/**
 * <h1>分布式锁接口</h1>
 * 只需要两个接口: 获取锁与释放锁
 */
public interface IDistributedLock {
    /**
     * <h2>获取锁</h2>
     * */
    boolean acquire();
    /**
     * <h2>释放锁</h2>
     * */
    void release();
}
```

```
import SpringContextUtil;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.redis.core.StringRedisTemplate;

/**
 * <h1>基于 Redis 实现的分布式锁</h1>
 */
@Slf4j
public class RedisLock implements IDistributedLock {

    /** redis client */
    private static StringRedisTemplate redisTemplate;

    private String lockKey;                 // 锁的键值
    private int expireMsecs = 15 * 1000;    // 锁超时, 防止线程得到锁之后, 不去释放锁
    private int timeoutMsecs = 15 * 1000;   // 锁等待, 防止线程饥饿
    private boolean locked = false;         // 是否已经获取锁

    RedisLock(String lockKey) {
        this.lockKey = lockKey;
    }

    RedisLock(String lockKey, int timeoutMsecs) {
        this.lockKey = lockKey;
        this.timeoutMsecs = timeoutMsecs;
    }

    RedisLock(String lockKey, int expireMsecs, int timeoutMsecs) {
        this.lockKey = lockKey;
        this.expireMsecs = expireMsecs;
        this.timeoutMsecs = timeoutMsecs;
    }

    public String getLockKey() {
        return this.lockKey;
    }

    @Override
    public synchronized boolean acquire() {

        int timeout = timeoutMsecs;

        if (redisTemplate == null) {
            redisTemplate = SpringContextUtil.getBean(StringRedisTemplate.class);
        }

        try {

            while (timeout >= 0) {

                long expires = System.currentTimeMillis() + expireMsecs + 1;
                String expiresStr = String.valueOf(expires); // 锁到期时间

                if (redisTemplate.opsForValue().setIfAbsent(lockKey, expiresStr)) {
                    locked = true;
                    log.info("[1] 成功获取分布式锁!");
                    return true;
                }
                String currentValueStr = redisTemplate.opsForValue().get(lockKey); // redis里的时间

                // 判断是否为空, 不为空的情况下, 如果被其他线程设置了值, 则第二个条件判断是过不去的
                if (currentValueStr != null && Long.parseLong(currentValueStr) < System.currentTimeMillis()) {

                    String oldValueStr = redisTemplate.opsForValue().getAndSet(lockKey, expiresStr);

                    // 获取上一个锁到期时间, 并设置现在的锁到期时间
                    // 只有一个线程才能获取上一个线程的设置时间
                    // 如果这个时候, 多个线程恰好都到了这里, 但是只有一个线程的设置值和当前值相同, 它才有权利获取锁
                    if (oldValueStr != null && oldValueStr.equals(currentValueStr)) {
                        locked = true;
                        log.info("[2] 成功获取分布式锁!");
                        return true;
                    }
                }

                timeout -= 100;
                Thread.sleep(100);
            }
        } catch (Exception e) {
            log.error("获取锁出现异常, 必须释放: {}", e.getMessage());
        }

        return false;
    }

    @Override
    public synchronized void release() {

        if (redisTemplate == null) {
            redisTemplate = SpringContextUtil.getBean(StringRedisTemplate.class);
        }

        try {
            if (locked) {

                String currentValueStr = redisTemplate.opsForValue().get(lockKey); // redis里的时间

                // 校验是否超过有效期, 如果不在有效期内, 那说明当前锁已经失效, 不能进行删除锁操作
                if (currentValueStr != null && Long.parseLong(currentValueStr) > System.currentTimeMillis()) {
                    redisTemplate.delete(lockKey);
                    locked = false;
                    log.info("[3] 成功释放分布式锁!");
                }
            }
        } catch (Exception e) {
            log.error("释放锁出现异常, 必须释放: {}", e.getMessage());
        }
    }
}
```

```
/**
 * <h1>分布式锁工具类</h1>
 */
public class DistributedLockUtil {

    /**
     * 获取分布式锁
     * 默认获取锁15s超时, 锁过期时间15s
     */
    public static IDistributedLock getDistributedLock(String lockKey) {
        lockKey = assembleKey(lockKey);
        return new RedisLock(lockKey);
    }

    /**
     * 获取分布式锁
     */
    public static IDistributedLock getDistributedLock(String lockKey, int timeoutMsecs) {
        lockKey = assembleKey(lockKey);
        return new RedisLock(lockKey, timeoutMsecs);
    }

    /**
     * 获取分布式锁
     */
    public static IDistributedLock getDistributedLock(String lockKey, int timeoutMsecs, int expireMsecs) {
        lockKey = assembleKey(lockKey);
        return new RedisLock(lockKey, expireMsecs, timeoutMsecs);
    }

    /**
     * 对 key 进行拼接
     */
    private static String assembleKey(String lockKey) {
        return String.format("imooc_analyze_%s", lockKey);
    }
}
```

```
import org.springframework.beans.BeansException;
import org.springframework.context.ApplicationContext;
import org.springframework.context.ApplicationContextAware;
import org.springframework.stereotype.Component;

/**
 * <h1>获取当前 classpath 中的 Bean</h1>
 */
@Component
public class SpringContextUtil implements ApplicationContextAware {

    private static ApplicationContext applicationContext;

    @Override
    public void setApplicationContext(ApplicationContext applicationContext) throws BeansException {
        SpringContextUtil.applicationContext = applicationContext;
    }

    public static ApplicationContext getApplicationContext() {
        return applicationContext;
    }

    @SuppressWarnings("unchecked")
    public static <T> T getBean(Class c) throws BeansException {
        return (T) applicationContext.getBean(c);
    }
}
```

ref:
http://www.imooc.com/article/280456
