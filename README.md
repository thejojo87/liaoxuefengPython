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

# Day 9 - 编写API
RestAPI了

就是一个get 在handle里。
但是原文里写的乱七八糟。
看代码就很简单了。
apierror跳过去了先。

下一章节继续

# Day 10 - 用户注册和登录
首先要完成的是用户注册，这个比较简单。

需要的是一个api，指向注册页面。还有template

template我发现他用了vue这个框架。
要学会用这个前端先？

在static里的js文件夹下面添加了一些jquery和vue等js。
然后修改basetemplat引用，增加了vue。
写了registe界面。register界面使用了submit给/api/users里

下一步是postregister信息
在post api/users里处理函数

下半部分是用户登录界面。
这里比较复杂，因为涉及到cookie，加密问题。

先写一个signin界面

然后在handle处理问题。

这里留下了一个问题，就是登陆成功后在上面并没有显示状态，下面评论有答案，
不过等14天完成吧。

# Day 11 - 编写日志创建页

写后端代码，第一部就是post 的函数。Rest API
比如新建日志。

@post('/api/blogs')

比较难的事情是编写前段页面，因为前端混合html，css和javascript。
而且前端页面是动态页面，由后端代码生成的。

模板方式会让后端和javascript很紧密，所以需要mvvm模式

再这里，app.py文件里，必定是哪里错了，才导致request没有user属性。
就是app里初始化init的第二行，middlewares里，少了auth_factory。

# Day 12 - 编写日志列表页

现在apis文件里定义一个page类，储存分页信息。
就只有init函数和str函数。
item_count是博客总数
page_index是页码，page_size是一个页面显示最多博客的数目。
还有两个boor函数。has_next has_previous

然后是handlers.py
添加get api/blogs 这个是动作，并不是直接访问的，需要和template配合
首先在template里，使用javascript，使用api/blogs获取blog数组。




添加 get /manage/blogs页面,template写一个-导入api/blogs页面里。
写完，可以看到总页面了。
但是比如删除，比如进入blog页面都是没有的。要自己写。

所以一共需要3个部分。
一个api/blogs  一个manage/blogs 最后一个是模板 template

# Day 13 - 提升开发效率
主要是这个框架，修改了代码，并不会反映到网站里，必须得重启。
很麻烦。
要添加这个功能。在这里。
Django自动有这个模式。
一种思路是检测www目录下的代码改动，一旦有改动，就自动重启服务器。

按照这个思路，我们可以编写一个辅助程序pymonitor.py，
让它启动wsgiapp.py，并时刻监控www目录下的代码改动，有改动时，
先把当前wsgiapp.py进程杀掉，再重启，就完成了服务器进程的自动重启。

要监控目录文件的变化，我们也无需自己手动定时扫描，
Python的第三方库watchdog可以利用操作系统的API来监控目录文件的变化，并发送通知。

wsgiapp文件是2.7的版本教程里的启动文件。
3的教程里没必要。

先新建一个pymonitor.py

有点不明白，

C:\Users\chn_t\AppData\Local\Programs\Python\Python35\python.exe C:/Users/chn_t/Desktop/coding/python-liaoxuefeng/liaoxuefengPython/www/pymonitor.py -m www.app


遇到一个问题，在app.py里 no module named orm
其实就是orm环境变量没有加在sys里。

解决办法是添加这两行：
http://www.itdadao.com/articles/c15a211947p0.html

```python
# current_working_directory = "C:\Users\username\PycharmProjects\projectName"
# sys.path.append(current_working_directory)

```
不过windows里，\这个符号需要是\\才可以。
http://stackoverflow.com/questions/18084554/why-do-i-get-a-syntaxerror-for-a-unicode-escape-in-my-file-path

最后再遇到这个问题：

```python

OSError: [Errno 10048] error while attempting to bind on address ('127.0.0.1', 9000): 通常每个套接字地址(协议/网络地址/端口)只允许使用一次。
Exception ignored in: <bound method Connection.__del of <aiomysql.connection.Connection object at 0x000000000390C4E0>>
Traceback (most recent call last):
  File "C:\Python34\lib\site-packages\aiomysql\connection.py", line 694, in __del File "C:\Python34\lib\site-packages\aiomysql\connection.py", line 260, in close File "C:\Python34\lib\asyncio\selector_events.py", line 568, in close File "C:\Python34\lib\asyncio\base_events.py", line 427, in call_soon File "C:\Python34\lib\asyncio\base_events.py", line 436, in _call_soon File "C:\Python34\lib\asyncio\base_events.py", line 265, in _check_closed RuntimeError: Event loop is closed
```

这个问题是因为我一个ip开了好几个服务。
需要把app关掉就可以了。




使用gunicorn可以一步搞定。
看aiohttp的官方文档支持gunicorn。

pip3 install gunicorn
gunicorn -b 127.0.0.1:8800 -k aiohttp.worker.GunicornWebWorker -w 1 -t 60 --reload app:app

注意加上 --reload

# Day 14 - 完成Web App

剩下的都是体力活


后端API包括：

    获取日志：GET /api/blogs

    创建日志：POST /api/blogs

    修改日志：POST /api/blogs/:blog_id

    删除日志：POST /api/blogs/:blog_id/delete

    获取评论：GET /api/comments

    创建评论：POST /api/blogs/:blog_id/comments

    删除评论：POST /api/comments/:comment_id/delete

    创建新用户：POST /api/users

    获取用户：GET /api/users

管理页面包括：

    评论列表页：GET /manage/comments

    日志列表页：GET /manage/blogs

    创建日志页：GET /manage/blogs/create

    修改日志页：GET /manage/blogs/edit

    用户列表页：GET /manage/users

用户浏览页面包括：

    注册页：GET /register

    登录页：GET /signin

    注销页：GET /signout

    首页：GET /

    日志详情页：GET /blog/:blog_id

把所有的功能实现，我们第一个Web App就宣告完成！

### 用户浏览页面里
，注册页面，登陆页面，注销页面有了。
第一个要做的是首页改成文章列表

@get('/')修改主页
这里需要注意一下。用户名的问题。
原来是在模板里，用request属性返回的。
但是在这里，改成了app.py里 response_factory里加了一句。

```python
r['__user__'] = request.__user__
```

当然base template也需要改掉。

这里不明白
1. 貌似page改成任何数字都无所谓？如果文章的查询num为0，才会使用page=1的默认设定
2. page_index貌似没用到？
3. 为什么查询是count(id)? 貌似是固定的，就按照id查询数目，如果没有就报错

先从数据库查询文章数，然后传过去page模型，计算页码等数字。
然后再查询数据库里文章，按照计算好的数字提取。


```python
# 对于首页的get请求的处理
@get('/')
def index(*, page="1"):
    page_index = get_page_index(page)
    num = yield from Blog.findNumber("count(id)")
    page = Page(num)
    if num == 0:
        blogs = []
    else:
        blogs = yield from Blog.findAll(orderBy="created_at desc", limit=(page.offset,page.limit))
    return {
        '__template__': 'blogs.html',
        'page': page,
        'blogs': blogs,
    }
```

下一个是日志详情页：GET /blog/:blog_id

```python

# 日志详情页面
@get('/blog/{id}')
def get_blog(id):
    blog = yield from Blog.find(id)  # 通过id从数据库拉取博客信息
    # 从数据库拉取指定blog的全部评论,按时间降序排序,即最新的排在最前
    comments = yield from Comment.findAll('blog_id=?', [id], orderBy='created_at desc')
    # 将每条评论都转化为html格式(根据text2html代码可知,实际为html的<p>)
    for c in comments:
        c.html_content = text2html(c.content)
    blog.html_content = markdown2.markdown(blog.content)  # blog是markdown格式,将其转换为html格式
    return {
        # 返回的参数将在jinja2模板中被解析
        "__template__": "blog.html",
        "blog": blog,
        "comments": comments
    }
```

然后还需要新的blog模板。
其实要是简单的从blogs页面复制过来也不是不可以。
不过还是添加了如果是用户登录，那么就可以评论。
有一个增加评论的功能。post的地址是哪里呢？
貌似是最上面的script里规定的
var comment_url = '/api/blogs/{{ blog.id }}/comments';

刷新还有重定向都是用javascript解决的。
refresh return

用户浏览页面是做完了。
下一部分是

### 管理页面
这里日志列表页，创建日志有了。
需要新建评论列表页面，用户列表页面。
修改日志页面，
####  评论列表页面
新建了一个get /manage/comments 导向一个template
新建了一个get /api/comments 用来给模板提供数据。和blogsqpi一模一样
新建了manage_comments.html

#### 用户列表页面

新建了一个get /manage/users 导向一个template
新建了一个get /api/users 和上面评论一样。
新建一个manage_users.html

#### 修改日志页面
GET /manage/blogs/edit
修改是在文章列表里。
又一个修改的图标。

所以新建一个get /manage/blogs/edit
然后是manage_blog_edit模板,模板之前就有过。

### 后端app页面

获取日志有了。

#### 创建日志-跳转
创建日志有了。但是创建日志之后，保存后跳转有错误。
创建日志用的事edit的template。保存确实是post api/blogs。但是redirect
在location.assign .出错的原因是，添加了id。

#### 修改日志-跳转
首先从manage/blogs里编辑图标链接导向edit模板。
传递id，给 get manage/blogs/edit。
edit模板里有 script postjson
现在就是缺少 post blog id

```python
# 修改日志api
# API: 修改博客
@post("/api/blogs/{id}")
def api_update_blog(id, request, *, name, summary, content):
    check_admin(request) # 检查用户权限
    # 验证博客信息的合法性
    if not name or not name.strip():
        raise APIValueError("name", "name cannot be empty")
    if not summary or not summary.strip():
        raise APIValueError("summary", "summary cannot be empty")
    if not content or not content.strip():
        raise APIValueError("content", "content cannot be empty")
    blog = yield from Blog.find(id)  # 获取修改前的博客
    blog.name = name.strip()
    blog.summary = summary.strip()
    blog.content = content.strip()
    yield from blog.update() # 更新博客
    return blog # 返回博客信息
```

#### 删除日志

只添加一个post api/blogs/{id}/delete
就可以了。
不过我对return dict 最后一句还不是很明白。

#### 创建评论

文章详情里面有个add comment按钮。
只需要加一个post，然后刷新不就好了么。
果然如此简单。


#### 删除评论
原来貌似没有删除评论按钮。

如果在评论管理页面直接删除，只需要一个api post就可以了。
但是不能在文章页面有删除，还是很麻烦呢。



