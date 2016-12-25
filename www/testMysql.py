#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Thejojo'



import orm
from models import User, Blog, Comment
import asyncio
import sys
import logging
# def test():
#     yield from orm.create_pool(user='www-data', password='www-data', database='awesome')
#
#     u = User(name='Test', email='test@example.com', passwd='1234567890', image='about:blank')
#
#     yield from u.save()
#
# for x in test():
#     pass

@asyncio.coroutine
def test(loop):
    yield from orm.create_pool(loop=loop, host='localhost', port=3307, user='www-data', password='www-data', db='awesome')
    u = User(name='testaaa733ss447',email='test7aaa3ss5537@test.com',passwd='test',image='about:blank')
    # yield from u.save()
    print(u)

    # 测试findAll
    users = yield from User.findAll(orderBy='created_at')
    for user in users:
        print(user)

    # 测试update语句
    user = users[1]
    user.email = 'guest@orm.com'
    user.name = 'guest'
    yield from user.update()
    # 测试count rows语句
    # rows = yield from User.findAll(orderBy='created_at')
    # logging.info('rows is %s' % rows)
    #
    # # 测试insert into语句
    # if rows < 3:
    #     for idx in range(5):
    #         u = User(
    #             name='test%s' % idx,
    #             email='test%s@org.com' % idx,
    #             passwd='orm123%s' % idx,
    #             image='about:blank'
    #         )
    #         row = yield from User.countRows(where='email = ?', args=[u.email])
    #         if row == 0:
    #             yield from u.save()
    #         else:
    #             print('the email is already registered...')

    yield from orm.destory_pool()

loop = asyncio.get_event_loop()
loop.run_until_complete(test(loop))
loop.close()
if loop.is_closed():
    sys.exit(0)

