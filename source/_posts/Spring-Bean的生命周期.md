---
title: Spring-Bean的生命周期
date: 2017-09-22 00:00:00
categories: Spring
tags:
    - Spring
---

Spring Bean的生命周期

<!-- more -->

![1528637-20181105211348802-396856434.png](1528637-20181105211348802-396856434.png)

详解：

1. instantiate bean对象实例化
2. populate properties 封装属性
3. 如果Bean实现BeanNameAware执行setBeanName
4. 如果Bean实现BeanFactoryAwar或ApplicationContextAwar设置工厂setBeanFactory或上下文对象setApplicationContext
5. 如果存在类实现BeanPostProcessor(后处理Bean),执行postProcessBeforeInitialization
6. 如果Bean实现InitializingBean执行afterPropertiesSet
7. 调用自定义的init-method方法
8. 如果存在类实现BeanPostProcessor(处理Bean),执行postProcessAfterInitialization
9. 执行业务处理
10. 如果Bean实现DisposableBean执行destroy
11. 调用自定义的destroy-method

第一步就是对实例化bean，调用构造函数来创建实例，第二步是根据配置，进行相应属性的设置，依赖注入就是在这一步完成的。

第三步和第四步是让spring去了解咱们的spring容器，第五步和第八步可以针对指定的Bean进行功能增强，这时一般是采用的动态代理，（两种动态代理方式：jdk动态代理和cglib动态代理）。第六步和第十步是通过实现指定的接口来完成init（初始化）和destory（销毁）操作。但是我们在通常情况下不会使用这两步，因为我们可以通过第七步和第十一步，在配置文件中设置相应的初始化和销毁方法。

比如：
![1528637-20181105212114593-1948447418.png](1528637-20181105212114593-1948447418.png)


总结：

对于springbean的生命周期，我们需要关注的主要有两个方法：
1.增强bean的功能可以使用后处理Bean，BeanPostProcessor
2.如果需要初始化或销毁操作，我们可以使用init-method方法和destory-method方法。

同时还需要注意一点：destory-method方法是只针对于scope=singleton的时候才有效果！

ref:
https://www.cnblogs.com/wgl-gdyuan/p/9911653.html
[Spring 了解Bean的一生(生命周期)](https://blog.csdn.net/w_linux/article/details/80086950) //TODO
[实践出真知：理解Spring Bean生命周期](https://blog.csdn.net/programmer_at/article/details/82533396) //TODO
[深入理解spring生命周期与BeanPostProcessor的实现原理](https://blog.51cto.com/4247649/2118349) //TODO
[三分钟了解spring-bean生命周期之初始化和销毁的三种方式](https://mp.weixin.qq.com/s?__biz=MzAxMjY1NTIxNA==&mid=2454441970&idx=1&sn=55a4491608d6f05a5a406b73024bbc6d&chksm=8c11e0f3bb6669e54a1499a2aad09d38ceb68d40a88dfd89bd53de0fbe84238fa45caf768037&scene=21#wechat_redirect) //TODO


