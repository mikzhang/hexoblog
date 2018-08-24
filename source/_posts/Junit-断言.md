---
title: Junit-断言
date: 2017-09-06 12:52:48
categories: Junit
tags:
    - Junit
---

Assert 类扩展了java.lang.Object类并为它们提供编写测试，以便检测故障。下表中有一种最常用的断言方法的更详细的解释

<!-- more -->

## 常用的断言方法

![常用的断言方法](20180808143938.png)

```
import static org.junit.Assert.*;
import org.junit.Test;

public class AssertionsTest {

	@Test
	public void test() {
		String obj1 = "junit";
		String obj2 = "junit";
		String obj3 = "test";
		String obj4 = "test";
		String obj5 = null;
		int var1 = 1;
		int var2 = 2;
		int[] arithmetic1 = { 1, 2, 3 };
		int[] arithmetic2 = { 1, 2, 3 };

		assertEquals(obj1, obj2);

		assertSame(obj3, obj4);

		assertNotSame(obj2, obj4);

		assertNotNull(obj1);

		assertNull(obj5);

		assertTrue(var1  var2);

		assertArrayEquals(arithmetic1, arithmetic2);
	}
}
```

ref:
[https://www.yiibai.com/junit/junit-assertions.html](https://www.yiibai.com/junit/junit-assertions.html)


