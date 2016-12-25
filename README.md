# liaoxuefengPython

[TOC]

# Day1 准备工作
git，mysql，pip安装第三方

# Day2 编写web框架


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

