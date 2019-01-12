---
title: Java-Strategy-Factory-Reflect-switch
date: 2017-09-22 00:00:00
categories: Java
tags:
    - Java
    - Strategy
    - Factory
---

本文使用策略模式+工厂模式+发射重构 switch 语句

<!-- more -->

## switch 结构代码

```
if(payStrategyParam == "ALIPAY") {
    System.out.println("pay with alipay: " + 12);
}else if(payStrategyParam == "WECHATPAY") {
    System.out.println("pay with wechatpay: " + 12);
}else if(payStrategyParam == "EBANKPAY") {
    System.out.println("pay with ebankpay: " + 12);
}
```

## 重构后的代码

```
/**
 * 付款策略接口
 */
public interface PayStrategy {
    void pay(double total);
}

/**
 * 支付宝付款
 */
public class Alipay implements PayStrategy{
    @Override
    public void pay(double total) {
        System.out.println("pay with alipay: " + total);
    }
}

/**
 * 微信付款
 */
public class WechatPay implements PayStrategy{
    @Override
    public void pay(double total) {
        System.out.println("pay with wechatpay: " + total);
    }
}

/**
 * 银行卡付款
 */
public class EbankPay implements PayStrategy{
    @Override
    public void pay(double total) {
        System.out.println("pay with ebankpay: " + total);
    }
}

/**
 * 付款枚举类
 */
public enum PayEnum {
    ALIPAY("com.pattern.reflect.Alipay"),
    WECHATPAY("com.pattern.reflect.WechatPay"),
    EBANKPAY("com.pattern.reflect.EbankPay");

    PayEnum(String className) {
        this.setClassName(className);
    }

    private String className;
    
    public String getClassName() {
        return className;
    }

    public void setClassName(String className) {
        this.className = className;
    }

}

/**
 * 工厂类
 */
public class StrategyFactory {
    public static PayStrategy getStrategy(String strategyType) throws Exception {
        String className = PayEnum.valueOf(strategyType).getClassName();
        return (PayStrategy) Class.forName(className).newInstance();
    }
}


public class Client {
    public static void main(String[] args) throws Exception {

        String payStrategyParam = "ALIPAY";//Param from front end

        PayStrategy strategy = StrategyFactory.getStrategy(payStrategyParam);
        strategy.pay(12);

        payStrategyParam = "WECHATPAY";//Param from front end

        strategy = StrategyFactory.getStrategy(payStrategyParam);
        strategy.pay(12);

        payStrategyParam = "EBANKPAY";//Param from front end

        strategy = StrategyFactory.getStrategy(payStrategyParam);
        strategy.pay(12);

        /* result:
        pay with alipay: 12.0
        pay with wechatpay: 12.0
        pay with ebankpay: 12.0
         */
    }
}
```

## 总结

if…else if…的缺点
多分支和复杂度高的逻辑会使代码冗长，难以理解和维护。
违反开闭原则，增删分支需要改动if…else if结构，，增大代码出错风险
使用策略模式+工厂模式的优点
对应的分支处理分成不同策略类来实现，使代码易于读懂和维护
扩展性好，增加分支只需要增加对应的策略实现类和枚举。符合开闭原则

ref：https://blog.csdn.net/u012557814/article/details/81671928 

