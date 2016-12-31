# liaoxuefengPython

[TOC]

# Day 1 - 准备工作
git，mysql，pip安装第三方

# Day 2 - 编写web框架


# Day 3 - 编写ORM

其实我完全看不懂。
ORM由几个部分组成。

创建连接池。 create_pool

select语句。 select

excute 用来做inset，update，delete的。

字段。Field，子类做stringfield，等等

Model，metaclass

Model 下面添加save，find，等等方法。

# Day 4 - 编写Model

在编写ORM时，给一个Field增加一个default参数可以让ORM自己填入缺省值，非常方便。并且，缺省值可以作为函数对象传入，在调用save()时自动计算。

例如，主键id的缺省值是函数next_id，创建时间created_at的缺省值是函数time.time，可以自动设置当前日期和时间。

日期和时间用float类型存储在数据库中，而不是datetime类型，这么做的好处是不必关心数据库的时区以及时区转换问题，排序非常简单，显示的时候，只需要做一个float到str的转换，也非常容易。
写完model，然后就因该在mysql数据库里生成表了。

可以手写创建表的sql脚本。
在pycharm里，右边有个database
那里先连接localhost。open console
运行sql脚本。
然后选择moreshema。就能看到了。awesome表。

源代码有个坑。
event loop closed。
这个问题最主要的原因就是：执行完SQL语句，没有释放与数据库的连接。

只需要在 orm.py的execute方法中，加上对连接的释放即可：

```
@asyncio.coroutine
def execute(sql, args):
    log(sql)
    with (yield from __pool) as conn:
        try:
            cur = yield from conn.cursor()
            yield from cur.execute(sql.replace('?', '%s'), args)
            affected = cur.rowcount
            yield from cur.close()
        except BaseException as e:
            raise
        finally:
            conn.close()
        return affected
```

还是不行，所以加上了destory方法。在test最后写上。

# Day 5 - 编写Web框架

首先是coroweb文件
首先定义get和post
函数经过该函数后，即加入__method__、__route__属性
例如，处理带参数的URL/blog/{id}可以这么写：

@get('/blog/{id}')
def get_blog(id):
    pass

类似还有一个post。

第二个部分是好几个函数，判断函数值关键字

第三个是RequestHandler
URL处理函数不一定是一个coroutine，因此我们用RequestHandler()来封装一个URL处理函数。

RequestHandler是一个类，由于定义了__call__()方法，因此可以将其实例视为函数。

RequestHandler目的就是从URL函数中分析其需要接收的参数，从request中获取必要的参数，
调用URL函数，然后把结果转换为web.Response对象，这样，
就完全符合aiohttp框架的要求：

第四个是addroute模块

然后是app.py文件

# Day 6 - 编写配置文件

config_default 和config_override，config 这3个文件

default用来保存默认设置。override用来覆盖数据库host等等。
优先从override来读取。配置读取文件放在统一的config里

前两个很简单。最后一个复杂一点。

这个toDict的主要功能是添加一种取值方式a_dict.key，相当于a_dict['key']

# Day 7 - 编写MVC

调试成功。不知道为什么原来的app.py文件有错误。无法连接mysql。
修改之后就好了。

# Day 8 - 构建前端

uikit 这个css框架，打包放倒static文件夹里

jinja2模板

```
“继承”模板的方式是通过编写一个“父模板”，在父模板中定义一些可替换的block（块）。然后，编写多个“子模板”，每个子模板都可以只替换父模板定义的block。比如，定义一个最简单的父模板：

<!-- base.html -->
<html>
    <head>
        <title>{% block title%} 这里定义了一个名为title的block {% endblock %}</title>
    </head>
    <body>
        {% block content %} 这里定义了一个名为content的block {% endblock %}
    </body>
</html>

对于子模板a.html，只需要把父模板的title和content替换掉：

{% extends 'base.html' %}

{% block title %} A {% endblock %}

{% block content %}
    <h1>Chapter A</h1>
    <p>blablabla...</p>
{% endblock %}

```

开始写base界面了。但是新的uikit已经改变了很多。有些功能无法实现。
如果想一模一样，还是把廖雪峰的sattic文件给复制下来。
html界面一共有head 和body部分。
head界定了三个块。meta title beforehead

用于子页面定义一些meta，例如rss feed：
```
  {% block meta %} ... {% endblock %}

覆盖页面的标题：

  {% block title %} ... {% endblock %}

子页面可以在<head>标签关闭前插入JavaScript代码：

  {% block beforehead %} ... {% endblock %}
```

body 部分：
第一个部分是导航条，第二个部分是内容。第三个部分是最底下的声明之类的。

base写完之后，写blogs界面

然后处理url的函数更新一下。在handlers里

先改写index函数，然后教程里没写出来，但是要从models里import Blogs等等。



