---
title: Junit-运行参数化测试
date: 2017-09-06 12:52:48
categories: Junit
tags:
    - Junit
---

Parameterized 的测试运行器允许使用不同的参数多次运行同一个测试。

<!-- more -->

## 类
```
public class Calculator {
    public double add(double a, double b){
        return a + b;
    }
}
```

## 测试类
```
@RunWith(value = Parameterized.class)
public class CalculatorTest {

    private double expected;
    private double valueOne;
    private double valueTwo;

    @Parameters
    public static Collection<Integer[]> getTestParameters(){
        return Arrays.asList(
            new Integer[][]{
                {2, 1, 1}, //expected, valueOne, valueTwo
                {3, 2, 1},
                {4, 3, 1},
            }
        );
    }

    public CalculatorTest(double expected, double valueOne, double valueTwo){
        this.expected = expected;
        this.valueOne = valueOne;
        this.valueTwo = valueTwo;
    }

    @Test
    public void add() throws Exception {
        Calculator cal = new Calculator();
        assertEquals(expected, cal.add(valueOne, valueTwo), 0);
    }
}
```

## 说明
![20180803161601](20180803161601.png)
![sdfiosajfsdf](sdfiosajfsdf.png)


ref:
Junit 实战第二版


