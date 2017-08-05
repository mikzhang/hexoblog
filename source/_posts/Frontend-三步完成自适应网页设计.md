---
title: Frontend_三步完成自适应网页设计
date: 2017-08-03 07:33:10
categories: Frontend
tags:
     - Frontend
---

自适应网页设计近来很流行，如果你接触比较少请参见 [responsive sites](http://webdesignerwall.com/trends/inspiration-fluid-responsive-design)。当然，对一个新手来说可能听起来有点复杂，其实它比你想象的简单多了。这里是一个快速教程，通过学习你会自适应网页和media queries的基本原理（前提你有css基础）。
[demo](http://webdesignerwall.com/demo/responsive-design/index.html)

## Step 1：Meta 标签

为了适应屏幕，不少移动浏览器都会把HTML页面置于较大视口宽度（一般会大于屏幕宽度），你可以使用viewport meta标签来设定。以下viewport meta标签告诉浏览器视口宽度等于设备屏幕宽度，且不进行初始缩放：
```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```
IE8及其更低版本不支持media query，可以使用media-queries.js或respond.js脚本实现支持。
```html
<!--[if lt IE 9]><script src="http://css3-mediaqueries-js.googlecode.com/svn/trunk/css3-mediaqueries.js"></script> <![endif]-->
```
## Step 2. HTML结构

在这个例子中，页面布局包括 header，content，sidebar和
footer。header固定高度为180px，content宽600px，sidebar宽300px。
{% asset_img page-structure.png %}

## Step 3. Media Queries

[CSS3 media query](http://webdesignerwall.com/tutorials/css3-media-queries)是自适应网页设计的关键，他就像高级语言里的if条件语句，告诉浏览器根据不同的视口宽度（这里等于浏览器宽度）来渲染网页。

如果视口宽度小于等于980px，下面规则生效。

这里将容器绝对宽度改用百分比显示，让页面排版更加灵活。

```
/* for 980px or less */
@media screen and (max-width: 980px) {

    #pagewrap{
        width: 94%;
    }
    #content{
        width: 65%;
    }
    #sidebar{
        width: 30%;
    }

}
```
如果视口宽度小于等于700px， 将#content和#sidebar宽度设为自动(auto)，并移除它的浮动属性(float)，这样它会变成满版显示。

```
/* for 700px or less */
@media screen and (max-width:700px) {

    #content {
        width: auto;
        float: none;
    }
    #sidebar {
        width: auto;
        float: none;
    }

}
```
当视口宽度小于等于480px时（如手机屏幕），将#header高度设为自动，h1的字体大小设定为24px，并隐藏#sidebar。

```
/* for 480px or less */
@media screen and (max-width:480px) {

    #header {
        height: auto;
    }
    h1 {
        font-size: 24px;
    }
    #sidebar {
        display: none;
    }

}
```
根据你的喜好，可以定义更多的media queriey条件

## 小结
这里只是一个快速教程，更多可以参见[使用CSS3 Media Queries实现网页自适应](http://xinyo.org/archives/62104/)
ref:
[http://xinyo.org/archives/64557/](http://xinyo.org/archives/64557/)
