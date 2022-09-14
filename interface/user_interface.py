# 用户相关接口
from db.db_handle import user_select, user_save
from lib.commen import encrypt, pwd_is_correct, get_log

logger = get_log('用户相关日志')


# 注册接口
def register_interface(username, password):
    res = pwd_is_correct(password)
    if not res:
        return False, '密码必须是6-16位字母数字或下划线'
    user_dict = user_select(username)
    if user_dict:
        return False, '当前输入用户名已存在，请重新输入!'
    password = encrypt(password)
    user_dict = {
        'username': username,
        'password': password,
        'balance': 15000,
        'shop_car': {},
        'flow': [],
        'is_lock': False,
        'is_admin': False
    }
    user_save(user_dict)
    logger.info(f'用户{username}注册成功')
    return True, f'用户:{username}注册成功'


# 登录接口
def login_interface(username, password):
    user_dict = user_select(username)
    if not user_dict:
        return False, '用户名不存在或密码错误'
    if user_dict['is_lock']:
        return False, '您已被锁定，请尽快联系管理员解锁!'
    password = encrypt(password)
    if password != user_dict['password']:
        return False, '用户名不存在或密码错误'
    logger.info(f'用户{username}登录成功')
    return (username, user_dict['is_admin']), '登录成功'
