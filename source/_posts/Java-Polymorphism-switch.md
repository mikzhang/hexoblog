---
title: Java-Polymorphism-switch
date: 2017-09-22 00:00:00
categories: Java
tags:
    - Java
    - Polymorphism
---

本文使用多态思想重构 switch 语句

<!-- more -->

## switch 结构代码

```
public class Base0 {
    private int arg;

    public Base0(int arg) {
        this.arg = arg;
    }

    public void show() {
        switch(arg){
            case 1:
                System.out.println("this is 1");
                break;
            case 2:
                System.out.println("this is 2");
                break;
            case 3:
                System.out.println("this is 3");
                break;
        }
    }
}
```

## 重构后的代码

```
public abstract class Base {
    private int arg;

    public Base(int arg) {
        this.arg = arg;
    }

    public abstract void show();
}

public class Ext1 extends Base {

    public Ext1(int arg) {
        super(arg);
    }

    @Override
    public void show() {
        System.out.println("this is 1");
    }

}

// Ext2, Ext3 代码同理 ...

public class Client {

    public static void main(String[] args) {
        Base0 base01 = new Base0(1);
        Base0 base02 = new Base0(2);
        Base0 base03 = new Base0(3);
        base01.show();
        base02.show();
        base03.show();

        Base base1 = new Ext1(1);
        Base base2 = new Ext2(2);
        Base base3 = new Ext3(3);
        base1.show();
        base2.show();
        base3.show();

        /* result:
        this is 1
        this is 2
        this is 3
         */
    }
}
```

上述完全是一个面向过程到面向对象的转变：将每个case分支都作为一个子对象，然后用java语言的多态性去动态绑定。这样做确实是带来了性能上的损失，但是在当今的CPU计算能力而言，这是可以忽略的，而它带来的好处却很有用：

- 分支的增减只要继续派生即可；
- 子类代表了一个case，比必须用type去硬编码的case语句更加具有可读性；
- 代码的可读性增强，使得分支的维护性增加；
- 面向对象的思想更加符合人看世界的方式；
- 避免了漏写break语句造成的隐蔽错误；
 
ref：https://blog.csdn.net/hzh2007/article/details/8042711 
