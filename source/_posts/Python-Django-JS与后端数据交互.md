---
title: Python_Django_JS与后端数据交互
date: 2017-08-11 19:33:10
categories: Python
tags:
     - Python
     - Django
---


## 应用一： Js与后端数据交互，以供数据可视化
有时候我们想把一个 list 或者 dict 传递给 javascript，处理后显示到网页上，比如要用 js 进行可视化的数据。

请注意：如果是不处理，直接显示在网页上，用Django模板就可以了。

这里讲述两种方法：

1. 页面加载完成后，在页面上操作，在页面上通过 ajax 方法得到新的数据（再向服务器发送一次请求）并显示在网页上，这种情况适用于页面不刷新的情况下，动态加载一些内容。比如用户输入一个值或者点击某个地方，动态地把相应内容显示在网页上。
这种请问详见 Django Ajax 一节的内容。

2. 直接在视图函数（views.py中的函数）中渲染一个 list 或 dict 的内容，和网页其它部分一起显示到网页上（一次性地渲染，还是同一次请求）。
需要注意两点：1、views.py中返回的函数中的值要用 json.dumps()处理   2、在网页上要加一个 safe 过滤器
view.py
```python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.shortcuts import render
import json

def home(request):
    List = ['自强学堂', '渲染Json到模板']
    Dict = {'site': '自强学堂', 'author': '涂伟忠'}
    return render(request, 'home.html', {
            'List': json.dumps(List),
            'Dict': json.dumps(Dict)
        })
```

home.html
```
<script type="text/javascript">
    //列表
    var List = {{ List|safe }};

    //下面的代码把List的每一部分放到头部和尾部
    $('#list').prepend(List[0]);
    $('#list').append(List[1]);

    console.log('--- 遍历 List 方法 1 ---')
    for(i in List){
        console.log(i);// i为索引
    }

    console.log('--- 遍历 List 方法 2 ---')
    for (var i = List.length - 1; i >= 0; i--) {
        console.log(List[i]);
    };

    console.log('--- 同时遍历索引和内容，使用 jQuery.each() 方法 ---')
    $.each(List, function(index, item){
        console.log(index);
        console.log(item);
    });


    // 字典
    var Dict = {{ Dict|safe }};
    console.log("--- 两种字典的取值方式  ---")
    console.log(Dict['site']);
    console.log(Dict.author);

    console.log("---  遍历字典  ---");
    for(i in Dict) {
        console.log(i + Dict[i]);//注意，此处 i 为键值
    }
</script>
```


## 应用二：不刷新网页的情况下，加载一些内容

view.py
```python
#coding:utf-8
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse

def get(request):
    return render(request, 'oneapp/get.html')

def add(request):
    a = request.GET.get('a', 0)
    b = request.GET.get('b', 0)
    c = int(a) + int(b)
    return HttpResponse(str(c))
```

get.html
```
<script>
    $(document).ready(function(){
      $("#sum").click(function(){
        var a = $("#a").val();
        var b = $("#b").val();

        $.get("/oneapp/add/",{'a':a,'b':b}, function(ret){
            $('#result').html(ret)
        })
      });
    });
</script>
...
<form action="/oneapp/add/" method="get">
    a: <input type="text" id="a" name="a"> <br>
    b: <input type="text" id="b" name="b"> <br>
    <p>result: <span id='result'></span></p>
    <button type="button" id='sum'>提交</button>
</form>
```


## 应用三：传递数字或者字典到网页，由JS处理，再显示出来

views.py
```python
#coding:utf-8
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json


def ajax_list(request):
    a = range(100)
    #return HttpResponse(json.dump(a), content_type='application/json')
    return JsonResponse(a, safe=False)

def ajax_dict(request):
    name_dict = {'a': 1, 'b': 2}
    #return HttpResponse(json.dump(name_dict), content_type='application/json')
    return JsonResponse(name_dict)
```

index.html
```
<script>
    $(document).ready(function(){
      // 求和 a + b
      $("#sum").click(function(){
        var a = $("#a").val();
        var b = $("#b").val();

        $.get("{% url 'add' %}",{'a':a,'b':b}, function(ret){
            $('#result').html(ret);
        })
      });

      // 列表 list
      $('#list').click(function(){
          $.getJSON("{% url 'ajax_list' %}",function(ret){
            //返回值 ret 在这里是一个列表
            for (var i = ret.length - 1; i >= 0; i--) {
              // 把 ret 的每一项显示在网页上
              $('#list_result').append(' ' + ret[i])
            };
          })
      })

      // 字典 dict
      $('#dict').click(function(){
          $.getJSON("{% url 'ajax_dict' %}",function(ret){
              //返回值 ret 在这里是一个字典
              $('#dict_result').append(ret.a + '<br>');
              // 也可以用 ret['twz']
          })
      })
    });
</script>
...
<form action="/add/" method="get">
    a: <input type="text" id="a" name="a"> <br>
    b: <input type="text" id="b" name="b"> <br>
    <p>result: <span id='result'></span></p>
    <button type="button" id='sum'>提交</button>
</form>

<div id="dict">Ajax 加载字典</div>
<p id="dict_result"></p>

<div id="list">Ajax 加载列表</div>
<p id="list_result"></p>
```

如果是一个复杂的字典或者列表，如：
```
person_info_dict = [
    {"name":"xiaoming", "age":20},
    {"name":"tuweizhong", "age":24},
    {"name":"xiaoli", "age":33},
]
```
这样我们遍历列表的时候，每次遍历得到一个字典，再用字典的方法去处理，当然有更简单的遍历方法：
用 $.each() 方法代替 for 循环
```
$.getJSON('ajax_url_to_json', function(ret) {
    $.each(ret, function(i,item){
        // i 为索引，item为遍历值
    });
});
```

补充：如果 ret 是一个字典，$.each 的参数有所不同，详见：[http://api.jquery.com/jquery.each/](http://api.jquery.com/jquery.each/)
```
$.getJSON('ajax-get-a-dict', function(ret) {
    $.each(ret, function(key, value){
        // key 为字典的 key，value 为对应的值
    });
});
```

## 应用四：使用Django的表单
未完待续

ref:
[http://blog.csdn.net/u011138533/article/details/72629728](http://blog.csdn.net/u011138533/article/details/72629728)

