# 公共方法

import hashlib
import os
import time
import re
import random
import logging
import logging.config
from conf.settings import LOGGING_DIC, USER_DB_DIR


# 返回主界面
def exit_now():
    print('3秒后返回主页面...')
    time.sleep(3)


# 获取随机字母验证码
def random_code():
    res = [chr(i) for i in range(65, 91)]
    res1 = [chr(i) for i in range(97, 123)]
    res.extend(res1)
    random_list = random.sample(res, 4)
    return ''.join(random_list)


# 金额正则匹配验证
def money_is_correct(money):
    """
    只能匹配正数和正浮点数
    :return: 符合规定的字符串或者None
    """
    money = re.match('^[0-9](([0-9]*(\.[0-9]{1,3})$)|([0-9]+$))', money)
    return money.group()


# 密码正则匹配验证
def pwd_is_correct(password):
    """
    最短 6 位，最长 16 位 {6,16}
    可以包含小写大母 [a-z] 和大写字母 [A-Z]
    可以包含数字 [0-9]
    :return: 符合规定的字符串或者None
    """
    return re.match('^[\w]{6,16}$', password)


# 密码加密
def encrypt(msg):
    md5 = hashlib.md5()
    md5.update('这是加盐处理'.encode('utf8'))
    md5.update(msg.encode('utf8'))
    return md5.hexdigest()


# 记录日志
def get_log(msg):
    logging.config.dictConfig(LOGGING_DIC)
    return logging.getLogger(msg)


# 登录认证装饰器
def login_auth(user_type):
    def outer(func_name):
        def inner(*args, **kwargs):
            from core.user_src import is_login, is_admin, login
            if is_login:
                if not user_type == 'admin':
                    res = func_name(*args, **kwargs)
                    return res
                if is_admin:
                    res = func_name(*args, **kwargs)
                    return res
                else:
                    print(f'当前用户{is_login}没有管理员权限', end='\n\n')
            else:
                print('未登录,请先登录', end='\n\n')
                login()

        return inner

    return outer


# 获取当前格式化时间
def get_now_ftime():
    return time.strftime('%Y-%m-%d %H-%M-%S')


# 查询当前注册的所有用户 并返回用户名
def get_users():
    res = os.listdir(USER_DB_DIR)
    new_list = []
    for i in res:
        new_list.append(i.split('.')[0])
    return new_list

