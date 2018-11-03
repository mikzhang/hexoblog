---
title: Java-Java8-Lambda
date: 2018-09-21 21:31:57
categories: Java
tags:
    - Java
    - Java*8
    - Lambda
---

Java 8 lambda表达式示例

<!-- more -->

## 用lambda表达式实现Runnable

毫无疑问，lambda表达式用得最多的场合就是替代匿名内部类，而实现Runnable接口是匿名内部类的经典例子。lambda表达式的功能相当强大，用()->就可以代替整个匿名内部类！请看代码：

如果使用匿名内部类：
```
// Java 8之前：
new Thread(new Runnable() {
    @Override
    public void run() {
    System.out.println("Before Java8, too much code for too little to do");
    }
}).start();

//Java 8方式：
new Thread( () -> System.out.println("In Java8, Lambda expression rocks !!") ).start();
```
这个例子向我们展示了Java 8 lambda表达式的语法。你可以使用lambda写出如下代码：
```
(params) -> expression
(params) -> statement
(params) -> { statements }
```
例如，如果你的方法不对参数进行修改、重写，只是在控制台打印点东西的话，那么可以这样写：
```
() -> System.out.println("Hello Lambda Expressions");
```
如果你的方法接收两个参数，那么可以写成如下这样：
```
(int even, int odd) -> even + odd
```
顺便提一句，通常都会把lambda表达式内部变量的名字起得短一些。这样能使代码更简短，放在同一行。所以，在上述代码中，变量名选用a、b或者x、y会比even、odd要好。

## 使用Java 8 lambda表达式进行事件处理
如果你用过Swing API编程，你就会记得怎样写事件监听代码。这又是一个旧版本简单匿名类的经典用例，但现在可以不这样了。你可以用lambda表达式写出更好的事件监听代码，如下所示：
```
// Java 8之前：
JButton show =  new JButton("Show");
show.addActionListener(new ActionListener() {
    @Override
    public void actionPerformed(ActionEvent e) {
    System.out.println("Event handling without lambda expression is boring");
    }
});

// Java 8方式：
show.addActionListener((e) -> {
    System.out.println("Light, Camera, Action !! Lambda expressions Rocks");
});
```
Java开发者经常使用匿名类的另一个地方是为 Collections.sort() 定制 Comparator。在Java 8中，你可以用更可读的lambda表达式换掉丑陋的匿名类。我把这个留做练习，应该不难，可以按照我在使用lambda表达式实现 Runnable 和 ActionListener 的过程中的套路来做。

## 使用lambda表达式对集合进行迭代
请看对比：
```
//before java8
List<String> languages = Arrays.asList("java","scala","python");
for(String each:languages) {
    System.out.println(each);
}
//after java8
languages.forEach(x -> System.out.println(x));
// 使用Java 8的方法引用更方便，方法引用由::双冒号操作符标示，
// 看起来像C++的作用域解析运算符
languages.forEach(System.out::println);
```

## Java 8中使用lambda表达式的Map和Reduce示例
本例介绍最广为人知的函数式编程概念map。它允许你将对象进行转换。例如在本例中，我们将 costBeforeTax 列表的每个元素转换成为税后的值。我们将 x -> x*x lambda表达式传到 map() 方法，后者将其应用到流中的每一个元素。然后用 forEach() 将列表元素打印出来。使用流API的收集器类，可以得到所有含税的开销。有 toList() 这样的方法将 map 或任何其他操作的结果合并起来。由于收集器在流上做终端操作，因此之后便不能重用流了。你甚至可以用流API的 reduce() 方法将所有数字合成一个，下一个例子将会讲到。

```
// 不使用lambda表达式为每个订单加上12%的税
List costBeforeTax = Arrays.asList(100, 200, 300, 400, 500);
for (Integer cost : costBeforeTax) {
    double price = cost + .12*cost;
    System.out.println(price);
}
 
// 使用lambda表达式
List costBeforeTax = Arrays.asList(100, 200, 300, 400, 500);
costBeforeTax.stream().map((cost) -> cost + .12*cost).forEach(System.out::println);
```
结果:
```
112.0
224.0
336.0
448.0
560.0

112.0
224.0
336.0
448.0
560.0

```

在上个例子中，可以看到map将集合类（例如列表）元素进行转换的。还有一个 reduce() 函数可以将所有值合并成一个。Map和Reduce操作是函数式编程的核心操作，因为其功能，reduce 又被称为折叠操作。另外，reduce 并不是一个新的操作，你有可能已经在使用它。SQL中类似 sum()、avg() 或者 count() 的聚集函数，实际上就是 reduce 操作，因为它们接收多个值并返回一个值。流API定义的 reduceh() 函数可以接受lambda表达式，并对所有值进行合并。IntStream这样的类有类似 average()、count()、sum() 的内建方法来做 reduce 操作，也有mapToLong()、mapToDouble() 方法来做转换。这并不会限制你，你可以用内建方法，也可以自己定义。在这个Java 8的Map Reduce示例里，我们首先对所有价格应用 12% 的VAT，然后用 reduce() 方法计算总和。

既然提到了map，又怎能不提到reduce。reduce与map一样，也是函数式编程里最重要的几个方法之一。。。map的作用是将一个对象变为另外一个，而reduce实现的则是将所有值合并为一个，请看：
```
// 为每个订单加上12%的税
// 老方法：
List costBeforeTax = Arrays.asList(100, 200, 300, 400, 500);
double total = 0;
for (Integer cost : costBeforeTax) {
    double price = cost + .12*cost;
    total = total + price;
}
System.out.println("Total : " + total);
 
// 新方法：
List costBeforeTax = Arrays.asList(100, 200, 300, 400, 500);
double bill = costBeforeTax.stream().map((cost) -> cost + .12*cost).reduce((sum, cost) -> sum + cost).get();
System.out.println("Total : " + bill);
```
结果:
```
Total : 1680.0
Total : 1680.0
```

## filter操作
filter也是我们经常使用的一个操作。在操作集合的时候，经常需要从原始的集合中过滤掉一部分元素。
```
List<Double> cost = Arrays.asList(10.0, 20.0, 30.0, 40.0);
List<Double> filteredCost = cost.stream().filter(x -> x > 25.0).collect(Collectors.toList());
filteredCost.forEach(x -> System.out.println(x));
```
最后的结果：
```
30.0
40.0
```

## 使用lambda表达式和函数式接口Predicate
除了在语言层面支持函数式编程风格，Java 8也添加了一个包，叫做 java.util.function。它包含了很多类，用来支持Java的函数式编程。其中一个便是Predicate，使用 java.util.function.Predicate 函数式接口以及lambda表达式，可以向API方法添加逻辑，用更少的代码支持更多的动态行为。Predicate接口非常适用于做过滤。
```
    public static void filter(List<String> languages, Predicate<String> condition) {
        languages.stream().filter(x -> condition.test(x)).forEach(x -> System.out.println(x + " "));
    }

    public static void main(String[] args) {
        List<String> languages = Arrays.asList("Java","Python","scala","Shell","R");
        System.out.println("Language starts with J: ");
        filter(languages,x -> x.startsWith("J"));
        System.out.println("\nLanguage ends with a: ");
        filter(languages,x -> x.endsWith("a"));
        System.out.println("\nAll languages: ");
        filter(languages,x -> true);
        System.out.println("\nNo languages: ");
        filter(languages,x -> false);
        System.out.println("\nLanguage length bigger three: ");
        filter(languages,x -> x.length() > 4);
    }
```
可以看到，Stream API的过滤方法也接受一个Predicate，这意味着可以将我们定制的 filter() 方法替换成写在里面的内联代码，这就是lambda表达式的魔力。另外，Predicate接口也允许进行多重条件的测试，下个例子将要讲到。

## 如何在lambda表达式中加入Predicate
上个例子说到，java.util.function.Predicate 允许将两个或更多的 Predicate 合成一个。它提供类似于逻辑操作符AND和OR的方法，名字叫做and()、or()和xor()，用于将传入 filter() 方法的条件合并起来。例如，要得到所有以J开始，长度为四个字母的语言，可以定义两个独立的 Predicate 示例分别表示每一个条件，然后用 Predicate.and() 方法将它们合并起来，如下所示：
```
// 甚至可以用and()、or()和xor()逻辑函数来合并Predicate，
// 例如要找到所有以J开始，长度为四个字母的名字，你可以合并两个Predicate并传入
Predicate<String> startsWithJ = (n) -> n.startsWith("J");
Predicate<String> fourLetterLong = (n) -> n.length() == 4;
names.stream()
    .filter(startsWithJ.and(fourLetterLong))
    .forEach((n) -> System.out.print("nName, which starts with 'J' and four letter long is : " + n));
```
类似地，也可以使用 or() 和 xor() 方法。本例着重介绍了如下要点：可按需要将 Predicate 作为单独条件然后将其合并起来使用。简而言之，你可以以传统Java命令方式使用 Predicate 接口，也可以充分利用lambda表达式达到事半功倍的效果。


## 对列表的每个元素应用函数
我们通常需要对列表的每个元素使用某个函数，例如逐一乘以某个数、除以某个数或者做其它操作。这些操作都很适合用 map() 方法，可以将转换逻辑以lambda表达式的形式放在 map() 方法里，就可以对集合的各个元素进行转换了，如下所示。
```
// 将字符串换成大写并用逗号链接起来
List<String> G7 = Arrays.asList("USA", "Japan", "France", "Germany", "Italy", "U.K.","Canada");
String G7Countries = G7.stream().map(x -> x.toUpperCase()).collect(Collectors.joining(", "));
System.out.println(G7Countries);
```

## 计算集合元素的最大值、最小值、总和以及平均值
IntStream、LongStream 和 DoubleStream 等流的类中，有个非常有用的方法叫做 summaryStatistics() 。可以返回 IntSummaryStatistics、LongSummaryStatistics 或者 DoubleSummaryStatistic s，描述流中元素的各种摘要数据。在本例中，我们用这个方法来计算列表的最大值和最小值。它也有 getSum() 和 getAverage() 方法来获得列表的所有元素的总和及平均值。
```
//获取数字的个数、最小值、最大值、总和以及平均值
List<Integer> primes = Arrays.asList(2, 3, 5, 7, 11, 13, 17, 19, 23, 29);
IntSummaryStatistics stats = primes.stream().mapToInt((x) -> x).summaryStatistics();
System.out.println("Highest prime number in List : " + stats.getMax());
System.out.println("Lowest prime number in List : " + stats.getMin());
System.out.println("Sum of all prime numbers : " + stats.getSum());
System.out.println("Average of all prime numbers : " + stats.getAverage());
```

## Lambda表达式 vs 匿名类
既然lambda表达式即将正式取代Java代码中的匿名内部类，那么有必要对二者做一个比较分析。一个关键的不同点就是关键字 this。匿名类的 this 关键字指向匿名类，而lambda表达式的 this 关键字指向包围lambda表达式的类。另一个不同点是二者的编译方式。Java编译器将lambda表达式编译成类的私有方法。使用了Java 7的 invokedynamic 字节码指令来动态绑定这个方法。

## Java 8 Lambda表达式要点
1）lambda表达式仅能放入如下代码：预定义使用了 @Functional 注释的函数式接口，自带一个抽象函数的方法，或者SAM（Single Abstract Method 单个抽象方法）类型。这些称为lambda表达式的目标类型，可以用作返回类型，或lambda目标代码的参数。例如，若一个方法接收Runnable、Comparable或者 Callable 接口，都有单个抽象方法，可以传入lambda表达式。类似的，如果一个方法接受声明于 java.util.function 包内的接口，例如 Predicate、Function、Consumer 或 Supplier，那么可以向其传lambda表达式。

2）lambda表达式内可以使用方法引用，仅当该方法不修改lambda表达式提供的参数。本例中的lambda表达式可以换为方法引用，因为这仅是一个参数相同的简单方法调用。
```
list.forEach(n -> System.out.println(n)); 
list.forEach(System.out::println);  // 使用方法引用
```
然而，若对参数有任何修改，则不能使用方法引用，而需键入完整地lambda表达式，如下所示：
```
list.forEach((String s) -> System.out.println("*" + s + "*"));
```
事实上，可以省略这里的lambda参数的类型声明，编译器可以从列表的类属性推测出来。

3）lambda内部可以使用静态、非静态和局部变量，这称为lambda内的变量捕获。

4）Lambda表达式在Java中又称为闭包或匿名函数，所以如果有同事把它叫闭包的时候，不用惊讶。

5）Lambda方法在编译器内部被翻译成私有方法，并派发 invokedynamic 字节码指令来进行调用。可以使用JDK中的 javap 工具来反编译class文件。使用 javap -p 或 javap -c -v 命令来看一看lambda表达式生成的字节码。大致应该长这样：
```
private static java.lang.Object lambda$0(java.lang.String);
```
6）lambda表达式有个限制，那就是只能引用 final 或 final 局部变量，这就是说不能在lambda内部修改定义在域外的变量。
```
List<Integer> primes = Arrays.asList(new Integer[]{2, 3,5,7});
int factor = 2;
primes.forEach(element -> { factor++; });
```
Compile time error : "local variables referenced from a lambda expression must be final or effectively final"
另外，只是访问它而不作修改是可以的，如下所示：
```
List<Integer> primes = Arrays.asList(new Integer[]{2, 3,5,7});
int factor = 2;
primes.forEach(element -> { System.out.println(factor*element); });
```
输出：
```
4
6
10
14
```
因此，它看起来更像不可变闭包，类似于Python。

以上就是Java 8的lambda表达式的全部10个例子。此次修改将成为Java史上最大的一次，将深远影响未来Java开发者使用集合框架的方式。我想规模最相似的一次修改就是Java 5的发布了，它带来了很多优点，提升了代码质量，例如：泛型、枚举、自动装箱（Autoboxing）、静态导入、并发API和变量参数。上述特性使得Java代码更加清晰，我想lambda表达式也将进一步改进它。我在期待着开发并行第三方库，这可以使高性能应用变得更容易写。

ref:
[Java8 lambda表达式10个示例](http://www.importnew.com/16436.html)
