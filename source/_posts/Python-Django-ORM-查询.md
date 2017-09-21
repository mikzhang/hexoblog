---
title: Python_Django_ORM_查询
date: 2017-08-05 07:33:10
categories: Python
tags:
     - Python
     - Django
---


<!-- more -->

## 模糊查询
```python
def search(request):
    searchtype = request.POST.get("searchtype")
    keyword = request.POST.get("keyword")

    #单个字段模糊查询
    elif searchtype == "author":
        sciencenews = models.Sciencenews.objects.filter(author__icontains=keyword)
    elif searchtype == "title":
        sciencenews = models.Sciencenews.objects.filter(title__icontains=keyword)
    elif searchtype == "content":
        sciencenews = models.Sciencenews.objects.filter(content__icontains=keyword)

    #多个字段模糊查询， 括号中的下划线是双下划线，双下划线前是字段名，双下划线后可以是icontains或contains,区别是是否大小写敏感，竖线是或的意思
    elif searchtype == "all":
        # OR 关系用 | 实现
        sciencenews = models.Sciencenews.objects.filter(Q(title__icontains=keyword)|Q(content__icontains=keyword)|Q(author__icontains=keyword))
    else:
        # AND 关系用 filter链 实现
        sciencenews = models.Sciencenews.objects.filter(author__icontains=keyword).filter(title__icontains=keyword).filter(content__icontains=keyword)

    return render(request,"show/index.html",{"param":sciencenews,"searchtype":searchtype,"key
```

## django使用Q来实现动态可变条件的或查询
```
from django.db.models import Q

# 1.固定条件的或查询
>>> User.objects.filter(Q(is_staff=True) | Q(username='123'))
[<User: staff_a>, <User: 123>, <User: staff_b>]

# 2.对于动态可变条件的或查询
代码示例：
>>> di = {'username': '123', 'is_staff': True} # 条件不固定
>>> q = Q()
>>> for i in di:
... q.add(Q(**{i: di[i]}), Q.OR)
...
<django.db.models.query_utils.Q object at 0x103a84bd0>
<django.db.models.query_utils.Q object at 0x103af1110>
>>> print q
(OR: (AND: ), (AND: ('username', '123')), ('is_staff', True))
>>> User.objects.filter(q)
[<User: staff_a>, <User: 123>, <User: staff_b>]
```

## Django执行(performing)原始的SQL查询：

 Django提供两种方式执行(performing)原始的SQL查询：

- Manager.raw() :执行原始查询并返回模型实例
- Executing custom SQL directly ：直接执行自定义SQL，这种方式可以完全避免数据模型，而是直接执行原始的SQL语句。

### raw()方法

The raw() manager method can be used to perform raw SQL queries that return model instances:
Manager. raw ( raw_query , params=None , translations=None )

#### 用法：
```
>>> for p in Person.objects.raw('SELECT * FROM Person LIMIT 2'):
...     print p
John Smith
Jane Jones
```
注意，原始SQL里的model，如果在 db_table 没有定义，则使用app的名称，后面下划线 后面接模型类的名称,如"Myblog_New";上面的例子，在定义类的时候已经这样处理了：
```
Class New(models.Model):
    ......
    ......
#自定义表名
    class Meta:
        db_table = 'New'
```

#### 查询字段隐射到模型字段（Mapping query fields to model fields）

raw() automatically maps fields in the query to fields on the model.并且是通过名称来匹配，这意味着我们可以使用SQL子句(clause)
```
>>> Person.objects.raw('''SELECT first AS first_name,
...                              last AS last_name,
...                              bd AS birth_date,
...                              pk as id,
...                       FROM some_other_table''')
```
返回一个RawQuerySet对象

#### 索引查找(Index lookups)
```
first_person = Person.objects.raw('SELECT * from myapp_person')[0]
first_person = Person.objects.raw('SELECT * from myapp_person LIMIT 1')[0]
```
然而,索引和切片不是在数据库级别上执行(除LIMIT外)

#### 延迟模型字段（Deferring model fields）

Fields may also be left out（left out：忽视，不考虑；被遗忘），这意味着该字段的查询将会被排除在根据需要时的加载。
```
>>> for p in Person.objects.raw('SELECT id, first_name FROM myapp_person'):
...     print p.first_name, # 这将检索到原始查询
...     print p.last_name # 这将检索需求
...
John Smith
Jane Jones
```
这个例子其实检索了三个字段，一个主键(必需)、一个原始SQL字段、一个需求字段。这里主键字段不能省略，否则会出错

#### 传递参数(Passing parameters into raw() )

如果需要执行参数化查询,您可以使用params参数
```
>>> query = 'SELECT * FROM myapp_person WHERE last_name = %s' % lname
>>> Person.objects.raw(query)
```
注意： 必须使用[参数]，否则出错


### 直接执行自定义SQL

Manager.raw() 远远不能满足日常需求，可直接执行自定义SQL，directly execute UPDATE , INSERT , or DELETE queries.

大致思路:

1. database connection调用 connection.cursor() 得到一个游标(cursor)对象。
2. cursor.execute(sql, [params]) 执行SQL
3. cursor.fetchone() 或者 cursor.fetchall()： 返回结果行
ps:
django.db.connection：代表默认的数据库连接
django.db.transaction ：代表默认数据库事务（transaction）

如果执行修改操作，则调用 transaction.commit_unless_managed()来保证你的更改提交到数据库。
```python
def my_custom_sql():
    from django.db import connection, transaction
    cursor = connection.cursor()

    # 数据修改操作——提交要求
    cursor.execute("UPDATE bar SET foo = 1 WHERE baz = %s", [self.baz])
    transaction.commit_unless_managed()

    # 数据检索操作,不需要提交
    cursor.execute("SELECT foo FROM bar WHERE baz = %s", [self.baz])
    row = cursor.fetchone()

    return row
```

django.db.connections ：针对使用多个数据库
````python
from django.db import connections
cursor = connections['my_db_alias'].cursor()
# Your code here...
transaction.commit_unless_managed(using='my_db_alias')
```
通常我们不需要手动调用 transaction.commit_unless_managed( ),我们可以使用 @commit_on_success：
```python
@commit_on_success
def my_custom_sql_view(request, value):
    from django.db import connection, transaction
    cursor = connection.cursor()

    # Data modifying operation
    cursor.execute("UPDATE bar SET foo = 1 WHERE baz = %s", [value])

    # Since we modified data, mark the transaction as dirty
    transaction.set_dirty()

    # Data retrieval operation. This doesn't dirty the transaction,
    # so no call to set_dirty() is required.
    cursor.execute("SELECT foo FROM bar WHERE baz = %s", [value])
    row = cursor.fetchone()

    return render_to_response('template.html', {'row': row})
```
查看Django ORM执行的SQL语句 ：   connection.queries

ref:
[http://blog.csdn.net/iloveyin/article/details/46380619](http://blog.csdn.net/iloveyin/article/details/46380619)
[https://www.douban.com/note/505215076/](https://www.douban.com/note/505215076/)
[http://blog.csdn.net/liuweiyuxiang/article/details/71104613](http://blog.csdn.net/liuweiyuxiang/article/details/71104613)
