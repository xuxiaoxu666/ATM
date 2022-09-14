# 管理员相关接口

from db.db_handle import *
from lib.commen import get_log, get_users, money_is_correct

logger = get_log('管理员相关日志')


# 添加管理员接口
def add_admin_interface(admin, add_name):
    add_user_dict = user_select(add_name)
    if not add_user_dict:
        return False, '输入的用户名不存在,请重新输入'
    if add_user_dict['is_admin']:
        return False, '输入的用户已是管理员,不用再添加了'
    add_user_dict['is_admin'] = True
    user_save(add_user_dict)
    logger.warning(f'管理员{admin}添加了用户{add_name}为管理员')
    return True, f'{admin}成功添加了了用户{add_name}为管理员'


# 锁定用户接口
def lock_user_interface(admin):
    n_list = get_users()  # ['jack', 'jasper']
    user_list = []
    for i in n_list:
        if i != admin:  # 不用锁自己
            if not user_select(i)['is_lock']:  # 被锁定的用户就不用在锁了
                user_list.append(i)
    if not user_list:
        return False, '当前没有可以锁定的用户'
    for i, v in enumerate(user_list, start=1):
        print(f'用户编号:{i}  --用户名:{v}')
    choice = input('请输入想要锁定的用户编号>>>:').strip()
    if not choice.isdigit():
        return False, '必须输入数字'
    choice = int(choice)
    if choice not in range(1, len(user_list) + 1):
        return False, '输入的编号不存在'
    alter_name = user_list[choice - 1]
    lock_user_dict = user_select(alter_name)
    lock_user_dict['is_lock'] = True
    user_save(lock_user_dict)
    logger.warning(f'用户{alter_name}已被管理员{admin}锁定')
    return True, f'用户{alter_name}已被锁定'


# 解锁接口
def unlock_interface(admin):
    n_list = get_users()  # ['jack', 'jasper']
    user_list = []
    for i in n_list:
        if i != admin:  # 不用解锁锁自己
            if user_select(i)['is_lock']:  # 没被锁定的用户就不用在解锁了
                user_list.append(i)
    if not user_list:
        return False, '当前没有可以解锁的用户'
    for i, v in enumerate(user_list, start=1):
        print(f'用户编号:{i}  --用户名:{v}')
    choice = input('请输入想要解锁的用户编号>>>:').strip()
    if not choice.isdigit():
        return False, '必须输入数字'
    choice = int(choice)
    if choice not in range(1, len(user_list) + 1):
        return False, '输入的编号不存在'
    unlock_name = user_list[choice - 1]
    unlock_user_dict = user_select(unlock_name)
    unlock_user_dict['is_lock'] = False
    user_save(unlock_user_dict)
    logger.warning(f'用户{unlock_name}已被管理员{admin}解锁')
    return True, f'用户{unlock_name}已被解锁'


# 添加商品接口
def add_shop_interface(admin, shop_name, shop_price, shop_kc):
    if not shop_name:
        return False, '商品名不能为空'
    shop_price = money_is_correct(shop_price)
    if not shop_price:
        return False, '输入金额不合法'
    shop_price = float(shop_price)
    if not shop_kc.isdigit():
        return False, '输入库存数不合法'
    shop_kc = int(shop_kc)
    if shop_kc not in range(1, 10000):
        return False, '输入库存数不合法'
    shop_list = shop_select()
    if not shop_list:
        shop_save([[shop_name, shop_price, shop_kc]])
        logger.info(f'管理员{admin}添加商品成功')
        return True, '商品添加成功'
    shop_list.append([shop_name, shop_price, shop_kc])
    shop_save(shop_list)
    logger.info(f'管理员{admin}添加商品成功')
    return True, '商品添加成功'


# 添加库存接口
def add_repertory_interface():
    shop_list = shop_select()
    if not shop_list:
        return False, '商品为空,请先添加商品'
    for i, v in enumerate(shop_list, start=1):
        print(f'商品编号:{i}  商品名:{v[0]}  --商品库存:{v[2]}')
    input_id = input('输入想要操作的商品编号>>>:').strip()
    if not input_id.isdigit():
        return False, '输入不合法'
    input_id = int(input_id)
    if input_id not in range(1, len(shop_list) + 1):
        return False, '输入不合法'
    input_num = input('输入当前库存量>>>:').strip()
    if not input_num.isdigit():
        return False, '输入不合法'
    input_num = int(input_num)
    if input_num not in range(1, 10000):
        return False, '输入不合法'
    shop_list[input_id - 1][2] = input_num
    shop_save(shop_list)
    logger.info('修改库存成功')
    return True, '修改成功'


# 修改商品单价接口
def reset_price_interface():
    shop_list = shop_select()
    if not shop_list:
        return False, '商品为空,请先添加商品'
    for i, v in enumerate(shop_list, start=1):
        print(f'商品编号:{i}  商品名:{v[0]}  --商品单价:{v[1]}')
    input_id = input('输入想要操作的商品编号>>>:').strip()
    if not input_id.isdigit():
        return False, '输入不合法'
    input_id = int(input_id)
    if input_id not in range(1, len(shop_list) + 1):
        return False, '输入不合法'
    input_money = input('请输入修改后的单价>>>:').strip()
    input_money = money_is_correct(input_money)
    if not input_money:
        return False, '输入金额不合法'
    input_money = float(input_money)
    shop_list[input_id - 1][1] = input_money
    shop_save(shop_list)
    logger.info('商品单价修改成功')
    return True, '商品单价修改成功'


# 下架商品
def remove_interface():
    shop_list = shop_select()
    if not shop_list:
        return False, '商品为空,请先添加商品'
    for i, v in enumerate(shop_list, start=1):
        print(f'商品编号:{i}  商品名:{v[0]}')
    input_id = input('输入想要操作的商品编号>>>:').strip()
    if not input_id.isdigit():
        return False, '输入不合法'
    input_id = int(input_id)
    if input_id not in range(1, len(shop_list) + 1):
        return False, '输入不合法'
    shop_list.pop(input_id - 1)
    shop_save(shop_list)
    logger.info('商品下架成功')
    return True, '商品下架成功'


# 查看商品接口
def check_shop_interface():
    return shop_select()
