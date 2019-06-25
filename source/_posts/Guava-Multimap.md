---
title: Guava-Multimap
date: 2017-09-22 00:00:00
categories: Java
tags:
    - Guava
    - Multimap
---

```
每个有经验的Java程序员都在某处实现过Map<K, List<V>>或Map<K, Set<V>>，并且要忍受这个结构的笨拙。
```

<!-- more -->

假如目前有个需求是给两个年级添加5个学生，并且统计出一年级学生的信息：

```
public class MultimapTest {
    class Student {
        String name;
        int age;
    }

    private static final String CLASS_NAME_1 = "一年级";
    private static final String CLASS_NAME_2 = "二年级";
    
    Map<String, List<Student>> StudentsMap = new HashMap<String, List<Student>>();

    public void testStudent() {
        
        for (int i = 0; i < 5; i++) {
            Student student = new Student();
            student.name = "Tom" + i;
            student.age = 6;
            addStudent(CLASS_NAME_1, student);
        }
        for (int i = 0; i < 5; i++) {
            Student student = new Student();
            student.name = "Jary" + i;
            student.age = 7;
            addStudent(CLASS_NAME_2, student);
        }
        List<Student> class1StudentList = StudentsMap.get(CLASS_NAME_1);
        
        for (Student stu : class1StudentList) {
            System.out.println("一年级学生 name:" + stu.name + " age:" + stu.age);
        }
    }
    
    public void addStudent(String className, Student student) {
        List<Student> students = StudentsMap.get(className);
        if (students == null) {
            students = new ArrayList<Student>();
            StudentsMap.put(className, students);
        }
        students.add(student);
    }

    public static void main(String[] args) {
        MultimapTest multimapTest = new MultimapTest();
        multimapTest.testStudent();

    }
}
```

可以看到我们实现起来特别麻烦，需要检查key是否存在，不存在时则创建一个，存在时在List后面添加上一个。这个过程是比较痛苦的，如果希望检查List中的对象是否存在，删除一个对象，或者遍历整个数据结构，那么则需要更多的代码来实现。

## Multimap 简介

Multimap 提供了一个方便地把一个键对应到多个值的数据结构。

我们可以这样理解Multimap:”键-单个值映射”的集合(例如：a -> 1 a -> 2 a ->4 b -> 3 c -> 5)

特点：不会有任何键映射到空集合：一个键要么至少到一个值，要么根本就不在Multimap中。

主要方法介绍：

- put(K, V)：添加键到单个值的映射
- putAll(K, Iterable<V>)：依次添加键到多个值的映射
- remove(K, V)：移除键到值的映射；如果有这样的键值并成功移除，返回true
- removeAll(K)：清除键对应的所有值，返回的集合包含所有之前映射到K的值，但修改这个集合就不会影响Multimap了
- replaceValues(K, Iterable<V>)：清除键对应的所有值，并重新把key关联到Iterable中的每个元素。返回的集合包含所有之前映射到K的值

## Multimap的视图
 

Multimap还支持若干强大的视图：

- asMap为Multimap<K, V>提供Map<K,Collection<V>>形式的视图。返回的Map支持remove操作，并且会反映到底层的 Multimap，但它不支持put或putAll操作。更重要的是，如果你想为Multimap中没有的键返回null，而不是一个新的、可写的空集 合，你就可以使用asMap().get(key)。（你可以并且应当把asMap.get(key)返回的结果转化为适当的集合类型——如 SetMultimap.asMap.get(key)的结果转为Set，ListMultimap.asMap.get(key)的结果转为List ——Java类型系统不允许ListMultimap直接为asMap.get(key)返回List——译者注：也可以用Multimaps中的asMap静态方法帮你完成类型转换）
- entries用Collection<Map.Entry<K, V>>返回Multimap中所有”键-单个值映射”——包括重复键。（对SetMultimap，返回的是Set）
- keySet用Set表示Multimap中所有不同的键。
- keys用Multiset表示Multimap中的所有键，每个键重复出现的次数等于它映射的值的个数。可以从这个Multiset中移除元素，但不能做添加操作；移除操作会反映到底层的Multimap。
- values()用 一个”扁平”的Collection<V>包含Multimap中的所有值。这有一点类似于 Iterables.concat(multimap.asMap().values())，但它直接返回了单个Collection，而不像 multimap.asMap().values()那样是按键区分开的Collection。

## Multimap不是Map

Multimap<K, V>不是Map<K,Collection<V>>，虽然某些Multimap实现中可能使用了map。它们之间的显著区别包括：

- Multimap.get(key)总是返回非null、但是可能空的集合。这并不意味着Multimap为相应的键花费内存创建了集合，而只是提供一个集合视图方便你为键增加映射值——译者注：如果有这样的键，返回的集合只是包装了Multimap中已有的集合；如果没有这样的键，返回的空集合也只是持有Multimap引用的栈对象，让你可以用来操作底层的Multimap。因此，返回的集合不会占据太多内存，数据实际上还是存放在Multimap中。
- 如果你更喜欢像Map那样，为Multimap中没有的键返回null，请使用asMap()视图获取一个Map<K, Collection<V>>。（或者用静态方法Multimaps.asMap()为ListMultimap返回一个Map<K, List<V>>。对于SetMultimap和SortedSetMultimap，也有类似的静态方法存在）
- 当且仅当有值映射到键时，Multimap.containsKey(key)才会返回true。尤其需要注意的是，如果键k之前映射过一个或多个值，但它们都被移除后，Multimap.containsKey(key)会返回false。
- Multimap.entries()返回Multimap中所有”键-单个值映射”——包括重复键。如果你想要得到所有”键-值集合映射”，请使用asMap().entrySet()。
Multimap.size()返回所有”键-单个值映射”的个数，而非不同键的个数。要得到不同键的个数，请改用Multimap.keySet().size()。

```
import com.google.common.collect.ArrayListMultimap;
import com.google.common.collect.Multimap;

public class MultimapTest {
    class Student {
        String name;
        int age;
    }

    private static final String CLASS_NAME_1 = "一年级";
    private static final String CLASS_NAME_2 = "二年级";
    
    Multimap<String, Student> multimap = ArrayListMultimap.create();

    public void testStudent() {
        
        for (int i = 0; i < 5; i++) {
            Student student = new Student();
            student.name = "Tom" + i;
            student.age = 6;
            multimap.put(CLASS_NAME_1, student);
        }
        for (int i = 0; i < 5; i++) {
            Student student = new Student();
            student.name = "Jary" + i;
            student.age = 7;
            multimap.put(CLASS_NAME_2, student);
        }
        
        for (Student stu : multimap.get(CLASS_NAME_1)) {
            System.out.println("一年级学生 name:" + stu.name + " age:" + stu.age);
        }
        //判断键是否存在
        if(multimap.containsKey(CLASS_NAME_1)){
            System.out.println("键值包含："+CLASS_NAME_1);
        }
        //”键-单个值映射”的个数
        System.out.println(multimap.size());
        //不同键的个数
        System.out.print(multimap.keySet().size());
    }
    
    public static void main(String[] args) {
        MultimapTest multimapTest = new MultimapTest();
        multimapTest.testStudent();
    }
}
```

//TODO
demo code 补充完整

ref:
https://www.cnblogs.com/parryyang/p/5776654.html
https://blog.csdn.net/xiangliqu/article/details/68953059
