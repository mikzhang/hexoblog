---
title: Mysql-锁机制-InnoDB
date: 2017-11-20 00:00:00
categories: Mysql
tags:
    - Mysql
---

锁是计算机协调多个进程或线程并发访问某一资源的机制，不同的数据库的锁机制大同小异。由于数据库资源是一种供许多用户共享的资源，所以如何保证数据并发访问的一致性、有效性是所有数据库必须解决的一个问题，锁冲突也是影响数据库并发访问性能的一个重要因素。了解锁机制不仅可以使我们更有效的开发利用数据库资源，也使我们能够更好地维护数据库，从而提高数据库的性能。

<!-- more -->

MySQL的锁机制比较简单，其最显著的特点是不同的存储引擎支持不同的锁机制。
例如，MyISAM和MEMORY存储引擎采用的是表级锁（table-level-locking）；BDB存储引擎采用的是页面锁（page-level-locking），同时也支持表级锁；InnoDB存储引擎既支持行级锁，也支持表级锁，默认情况下是采用行级锁。

上述三种锁的特性可大致归纳如下：

1. 表级锁：开销小，加锁快；不会出现死锁；锁定粒度大，发生锁冲突的概率最高，并发度最低。
2. 行级锁：开销大，加锁慢；会出现死锁；锁定粒度最小，发生锁冲突的概率最低，并发度也最高。
3. 页面锁：开销和加锁时间界于表锁和行锁之间；会出现死锁；锁定粒度界于表锁和行锁之间，并发度一般。

MyISAM表的读和写是串行的，即在进行读操作时不能进行写操作，反之也是一样。但在一定条件下MyISAM表也支持查询和插入的操作的并发进行，其机制是通过控制一个系统变量（concurrent_insert）来进行的，当其值设置为0时，不允许并发插入；当其值设置为1 时，如果MyISAM表中没有空洞（即表中没有被删除的行），MyISAM允许在一个进程读表的同时，另一个进程从表尾插入记录；当其值设置为2时，无论MyISAM表中有没有空洞，都允许在表尾并发插入记录。

MyISAM锁调度是如何实现的呢，这也是一个很关键的问题。例如，当一个进程请求某个MyISAM表的读锁，同时另一个进程也请求同一表的写锁，此时MySQL将会如优先处理进程呢？通过研究表明，写进程将先获得锁（即使读请求先到锁等待队列）。但这也造成一个很大的缺陷，即大量的写操作会造成查询操作很难获得读锁，从而可能造成永远阻塞。所幸我们可以通过一些设置来调节MyISAM的调度行为。我们可通过指定参数low-priority-updates，使MyISAM默认引擎给予读请求以优先的权利，设置其值为1（set low_priority_updates=1),使优先级降低。

InnoDB锁与MyISAM锁的最大不同在于：一是支持事务（TRANCSACTION），二是采用了行级锁。我们知道事务是由一组SQL语句组成的逻辑处理单元，其有四个属性（简称ACID属性），分别为：

- 原子性（Atomicity）：事务是一个原子操作单元，其对数据的修改，要么全部执行，要么全都不执行；
- 一致性（Consistent）：在事务开始和完成时，数据都必须保持一致状态；
- 隔离性（Isolation）：数据库系统提供一定的隔离机制，保证事务在不受外部并发操作影响的“独立”环境执行；
- 持久性（Durable）：事务完成之后，它对于数据的修改是永久性的，即使出现系统故障也能够保持。

## InnoDB锁模式
 
InnoDB实现了两种类型的行锁。

- 共享锁（S）:允许一个事务去读一行，阻止其他事务获得相同的数据集的排他锁。
- 排他锁（X）:允许获得排他锁的事务更新数据，但是组织其他事务获得相同数据集的共享锁和排他锁。

可以这么理解:
共享锁就是我读的时候，你可以读，但是不能写。排他锁就是我写的时候，你不能读也不能写。其实就是MyISAM的读锁和写锁，但是针对的对象不同了而已。

为了允许行锁和表锁共存，实现多粒度锁机制；同时还有两种内部使用的意向锁（都是表锁），分别为意向共享锁和意向排他锁

- 意向共享锁（IS）:表示事务准备给数据行加入共享锁，也就是说一个数据行加共享锁前必须先取得该表的IS锁
- 意向排他锁（IX）:类似上面，表示事务准备给数据行加入排他锁，说明事务在一个数据行加排他锁前必须先取得该表的IX锁。

InnoDB行锁模式兼容列表:
{% asset_img 20150810092332320.png %}

注意:
当一个事务请求的锁模式与当前的锁兼容，InnoDB就将请求的锁授予该事务；反之如果请求不兼容，则该事务就等待锁释放。
**意向锁是InnoDB自动加的，不需要用户干预。**

对于insert、update、delete，InnoDB会自动给涉及的数据加排他锁（X）；对于一般的Select语句，InnoDB不会加任何锁，事务可以通过以下语句给显示加共享锁或排他锁。

共享锁:select * from table_name where .....lock in share mode
排他锁:select * from table_name where .....for update

加入共享锁的例子:
{% asset_img 20150810092332321.png %}

利用select ....for update加入排他锁
{% asset_img 20150810092333322.png %}

## 锁的实现方式

InnoDB行锁是通过给索引项加锁实现的，如果没有索引，InnoDB会通过隐藏的聚簇索引来对记录加锁。
也就是说:如果不通过索引条件检索数据，那么InnoDB将对表中所有数据加锁，实际效果跟表锁一样。

行锁分为三种情形:

- Record lock :对索引项加锁，即锁定一条记录。
- Gap lock:对索引项之间的‘间隙’、对第一条记录前的间隙或最后一条记录后的间隙加锁，即锁定一个范围的记录，不包含记录本身
- Next-key Lock:锁定一个范围的记录并包含记录本身（上面两者的结合）。

注意:InnoDB默认级别是repeatable-read级别，所以下面说的都是在RR级别中的。

Next-Key Lock是行锁与间隙锁的组合，这样，当InnoDB扫描索引记录的时候，会首先对选中的索引记录加上行锁（Record Lock），再对索引记录两边的间隙加上间隙锁（Gap Lock）。如果一个间隙被事务T1加了锁，其它事务是不能在这个间隙插入记录的。

干巴巴的说没意思，我们来看看具体实例:

假设我们有一张表:
```
+----+------+
| id | age |
+----+------+
| 1 | 3 |
| 2 | 6 |
| 3 | 9 |
+----+------+
```
表结构如下:
```
CREATE TABLE `test` (
`id` int(11) NOT NULL AUTO_INCREMENT,
`age` int(11) DEFAULT NULL,
PRIMARY KEY (`id`),
KEY `keyname` (`age`)
) ENGINE=InnoDB AUTO_INCREMENT=302 DEFAULT CHARSET=gbk ;
```
这样我们age段的索引就分为
```
(negative infinity, 3],
(3,6],
(6,9],
(9,positive infinity)；
```

我们来看一下几种情况:
1、当事务A执行以下语句:
```
mysql> select * from fenye where age=6 for update ;
```
不仅使用行锁锁住了相应的数据行，同时也在两边的区间，（3,6]和（6，9] 都加入了gap锁。
这样事务B就无法在这个两个区间insert进新数据,但是事务B可以在两个区间外的区间插入数据。

2、当事务A执行
```
select * from fenye where age=7 for update ;
```
那么就会给(6,9]这个区间加锁，别的事务无法在此区间插入或更新数据。

3、如果查询的数据不再范围内，
比如事务A执行 
```
select * from fenye where age=100 for update ;
```
那么加锁区间就是(9,positive infinity)。

小结:
行锁防止别的事务修改或删除，GAP锁防止别的事务新增，行锁和GAP锁结合形成的的Next-Key锁共同解决了RR级别在写数据时的幻读问题。

## 何时在InnoDB中使用表锁

InnoDB在绝大部分情况会使用行级锁，因为事务和行锁往往是我们选择InnoDB的原因，但是有些情况我们也考虑使用表级锁。

1. 当事务需要更新大部分数据时，表又比较大，如果使用默认的行锁，不仅效率低，而且还容易造成其他事务长时间等待和锁冲突。
2. 事务比较复杂，很可能引起死锁导致回滚。

## InnoDB 锁表与锁行实例

由于InnoDB预设是Row-Level Lock，所以只有「明确」的指定主键，MySQL才会执行Row lock (只锁住被选取的资料例) ，否则MySQL将会执行Table Lock (将整个资料表单给锁住)。
举个例子: 假设有个表单products ，里面有id跟name二个栏位，id是主键。
例1: (明确指定主键，并且有此笔资料，row lock)
```
SELECT * FROM products WHERE id='3' FOR UPDATE;
SELECT * FROM products WHERE id='3' and type=1 FOR UPDATE;
```
例2: (明确指定主键，若查无此笔资料，无lock)
```
SELECT * FROM products WHERE id='-1' FOR UPDATE;
```
例3: (无主键，table lock)
```
SELECT * FROM products WHERE name='Mouse' FOR UPDATE;
```
例4: (主键不明确，table lock)
```
SELECT * FROM products WHERE id<>'3' FOR UPDATE;
```
例5: (主键不明确，table lock)
```
SELECT * FROM products WHERE id LIKE '3' FOR UPDATE;
```
注1: FOR UPDATE仅适用于InnoDB，且必须在交易区块(BEGIN/COMMIT)中才能生效。
注2: 要测试锁定的状况，可以利用MySQL的Command Mode ，开二个视窗来做测试。

## 死锁

我们说过MyISAM中是不会产生死锁的，因为MyISAM总是一次性获得所需的全部锁，要么全部满足，要么全部等待。而在InnoDB中，锁是逐步获得的，就造成了死锁的可能。

在上面的例子中我们可以看到，当两个事务都需要获得对方持有的锁才能够继续完成事务，导致双方都在等待，产生死锁。
发生死锁后，InnoDB一般都可以检测到，并使一个事务释放锁回退，另一个获取锁完成事务。

避免死锁:
有多种方法可以避免死锁，这里只介绍常见的三种:

1. 如果不同程序会并发存取多个表，尽量约定以相同的顺序访问表，可以大大降低死锁机会。
2. 在同一个事务中，尽可能做到一次锁定所需要的所有资源，减少死锁产生概率；
3. 对于非常容易产生死锁的业务部分，可以尝试使用升级锁定颗粒度，通过表级锁定来减少死锁产生的概率；

ref:
[https://www.2cto.com/database/201508/429967.html](https://www.2cto.com/database/201508/429967.html)
[http://www.jb51.net/article/50047.htm](http://www.jb51.net/article/50047.htm)
[https://www.cnblogs.com/chenqionghe/p/4845693.html](https://www.cnblogs.com/chenqionghe/p/4845693.html)
