---
title: Python-self
date: 2017-09-28 14:30:38
categories: Python
tags:
    - Python
---

首先明确的是self只有在类的方法中才会有，独立的函数或方法是不必带有self的。self在定义类的方法时是必须有的，虽然在调用时不必传入相应的参数。

<!-- more -->

## self代表类的实例,而非类

```python
class Test:
    def prt(self):
        print(self)
        print(self.__class__)
 
t = Test()
t.prt()
```
执行结果如下
```
<__main__.Test object at 0x000000000284E080>
<class '__main__.Test'>
```
从上面的例子中可以很明显的看出,self代表的是类的实例。而self.class则指向类。

再举个栗子
```python
class Person:
     def _init_(self,name):
          self.name=name
     def sayhello(self):
          print 'My name is:',self.name
p=Person('Bill')
p1=Person('Tom')
print p
print p1
```
在上述例子中，self指向Person的实例p。 为什么不是指向类本身呢，如果self指向类本身，那么当有多个实例对象时，self指向哪一个呢

## self不必非写成self

有很多童鞋是先学习别的语言然后学习Python的,所以总觉得self怪怪的,想写成this,可以吗？
当然可以,还是把上面的代码改写一下。

```python
class Test:
    def prt(this):
        print(this)
        print(this.__class__)
 
t = Test()
t.prt()
```
改成this后,运行结果完全一样。
当然,最好还是尊重约定俗成的习惯,使用self。

## self可以不写吗

在Python的解释器内部,当我们调用t.prt()时,实际上Python解释成Test.prt(t),也就是说把self替换成类的实例。
有兴趣的童鞋可以把上面的t.prt()一行改写一下,运行后的实际结果完全相同。
实际上已经部分说明了self在定义时不可以省略,如果非要试一下,那么请看下面:
```python
class Test:
    def prt():
        print(self)
 
t = Test()
t.prt()
```
运行时提醒错误如下:prt在定义时没有参数,但是我们运行时强行传了一个参数。

由于上面解释过了t.prt()等同于Test.prt(t),所以程序提醒我们多传了一个参数t。
```
Traceback (most recent call last):
  File "h.py", line 6, in <module>
    t.prt()
TypeError: prt() takes 0 positional arguments but 1 was given
```

当然,如果我们的定义和调用时均不传类实例是可以的,这就是类方法。
```python
class Test:
    def prt():
        print(__class__)
Test.prt()
```
运行结果如下
```
<class '__main__.Test'>
```

## 在继承时,传入的是哪个实例,就是那个传入的实例,而不是指定义了self的类的实例

```python
class Parent:
    def pprt(self):
        print(self)
 
class Child(Parent):
    def cprt(self):
        print(self)
c = Child()
c.cprt()
c.pprt()
p = Parent()
p.pprt()
```
运行结果如下
```
<__main__.Child object at 0x0000000002A47080>
<__main__.Child object at 0x0000000002A47080>
<__main__.Parent object at 0x0000000002A47240>
```
解释:
运行c.cprt()时应该没有理解问题,指的是Child类的实例。
但是在运行c.pprt()时,等同于Child.pprt(c),所以self指的依然是Child类的实例,由于self中没有定义pprt()方法,所以沿着继承树往上找,发现在父类Parent中定义了pprt()方法,所以就会成功调用。

## 在描述符类中,self指的是描述符类的实例

```python
class Desc:
    def __get__(self, ins, cls):
        print('self in Desc: %s ' % self )
        print(self, ins, cls)
class Test:
    x = Desc()
    def prt(self):
        print('self in Test: %s' % self)
t = Test()
t.prt()
t.x
```
运行结果如下:
```
self in Test: <__main__.Test object at 0x0000000002A570B8>
self in Desc: <__main__.Desc object at 0x000000000283E208>
<__main__.Desc object at 0x000000000283E208> <__main__.Test object at 0x0000000002A570B8> <class '__main__.Test'>
```
大部分童鞋开始有疑问了,为什么在Desc类中定义的self不是应该是调用它的实例t吗？怎么变成了Desc类的实例了呢？
注意:此处需要睁大眼睛看清楚了,这里调用的是t.x,也就是说是Test类的实例t的属性x,由于实例t中并没有定义属性x,所以找到了类属性x,而该属性是描述符属性,为Desc类的实例而已,所以此处并没有顶用Test的任何方法。

那么我们如果直接通过类来调用属性x也可以得到相同的结果。
下面是把t.x改为Test.x运行的结果。
```
self in Test: <__main__.Test object at 0x00000000022570B8>
self in Desc: <__main__.Desc object at 0x000000000223E208>
<__main__.Desc object at 0x000000000223E208> None <class '__main__.Test'>
```
题外话:由于在很多时候描述符类中仍然需要知道调用该描述符的实例是谁,所以在描述符类中存在第二个参数ins,用来表示调用它的类实例,所以t.x时可以看到第三行中的运行结果中第二项为<main.Test object at 0x0000000002A570B8>。而采用Test.x进行调用时,由于没有实例,所以返回None。

## 从OO的本质理解python中的self

举个栗子，假设我要对用户的数据进行操作，用户的数据包含name和age。如果用面向过程的话，实现出来是下面这样子的。
```pyhon
def user_init(user,name,age): 
  user['name'] = name 
  user['age'] = age 
  
def set_user_name(user, x): 
  user['name'] = x 
  
def set_user_age(user, x): 
  user['age'] = x 
  
def get_user_name(user): 
  return user['name'] 
  
def get_user_age(user): 
  return user['age'] 
  
myself = {} 
user_init(myself,'kzc',17) 
print get_user_age(myself) 
set_user_age(myself,20) 
print get_user_age(myself) 
```
可以看到，对用户的各种操作，都要传user参数进去。
如果用面向对象的话，就不用每次把user参数传来传去，把相关的数据和操作绑定在一个地方，在这个类的各个地方，可以方便的获取数据。
之所以可以在类中的各个地方访问数据，本质就是绑定了self这个东西，它方法的第一个参数，当然可以不叫self，叫其它名字，self只不过是个约定。
下面是面向对象的实现，可以看到，结构化多了，清晰可读。
```python
class User(object): 
  def __init__(self,name,age): 
    self.name = name 
    self.age = age 
  
  def SetName(self,name): 
    self.name = name 
  
  def SetAge(self,age): 
    self.age = age 
  
  def GetName(self): 
    return self.name 
  
  def GetAge(self): 
    return self.age 
  
u = User('kzc',17) 
print u.GetName() 
print u.GetAge() 
```

## 总结

- self在定义时需要定义,但是在调用时会自动传入。
- self的名字并不是规定死的,但是最好还是按照约定是用self
- self总是指调用时的类的实例。

ref:
[http://python.jobbole.com/81921/](http://python.jobbole.com/81921/)
[http://www.jb51.net/article/85871.htm](http://www.jb51.net/article/85871.htm)

