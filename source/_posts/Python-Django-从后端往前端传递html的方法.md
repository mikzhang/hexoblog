---
title: Python_Django_从后端往前端传递html的方法
date: 2017-08-08 11:38:28
categories: Python
tags:
     - Python
     - Django
---

Python_Django_从后端往前端传递html的方法

<!-- more -->

django从view向template传递HTML字符串的时候，django默认不渲染此HTML，原因是为了防止这段字符串里面有恶意攻击的代码。

如果需要渲染这段字符串，需要在view里这样写：
```python
from django.utils.safestring import mark_safe
```
函数里面这样写：
```python
pageHtml = mark_safe("<a href='{%url equip:listEquipmentCategory 1 %}'>首页</a>")
ret = {"equit_cate_list":list,"count":count,"ecform":ecform,"page":page,"pageHtml":pageHtml}
return render(request, "list_equip_category.html",ret)
```

前端页面直接使用{{pageHtml}}即可。

mark_safe这个函数就是确认这段函数是安全的，不是恶意攻击的。

ref:
[http://www.jianshu.com/p/5b304cb7c397](http://www.jianshu.com/p/5b304cb7c397)

