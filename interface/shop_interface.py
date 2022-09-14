# 购物相关接口

from db.db_handle import *
from lib.commen import get_log, get_now_ftime

logger = get_log('购物相关日志')


# 添加购物车接口
def add_car_interface(username):
    # 获取商品信息
    shop_list = shop_select()  # [['小米', 2999, 10], ['华为', 4999, 10]] 第三个参数是库存
    if not shop_list:
        return False, '没有商品信息,请联系管理员添加!'
    for i, v in enumerate(shop_list, start=1):
        print(f'商品编号:{i}  --商品名:{v[0]}  --商品单价:{v[1]}')
    tamp_dict = {}
    while True:
        input_id = input('请选择要添加的商品编号(q退出)>>>:').strip()
        if input_id == 'q':
            if not tamp_dict:
                return False, '已退出'
            user_dict = user_select(username)
            shop_car = user_dict['shop_car']
            for i in tamp_dict:
                if i in shop_car:  # 如果在 数量相加
                    shop_car[i][0] += tamp_dict[i][0]
                else:  # 如果不在 新增
                    shop_car[i] = tamp_dict[i]
            user_save(user_dict)
            return True, '购物车已添加成功~~~'
        if not input_id.isdigit():
            print('商品编号必须是数字,请重新选择!', end='\n\n')
            continue
        input_id = int(input_id)
        if input_id not in range(1, len(shop_list) + 1):
            print('输入的商品编号不存在,请重新输入!', end='\n\n')
            continue
        input_num = input('请输入要添加的数量>>>:').strip()
        if not input_num.isdigit():
            print('添加数量必须是数字,请重新选择!', end='\n\n')
            continue
        input_num = int(input_num)
        if input_num < 1:
            print('添加商品数量必须大于0,请重新选择!', end='\n\n')
            continue
        shop_name = shop_list[input_id - 1][0]
        price = shop_list[input_id - 1][1]
        if shop_name in tamp_dict:  # 在临时字典 则数量相加
            tamp_dict[shop_name][0] += input_num
            print('添加成功，退出当前页面自动保存', end='\n\n')
        else:  # 不在 则新增
            tamp_dict[shop_name] = [input_num, price]
            print('添加成功，退出当前页面自动保存', end='\n\n')


# 编辑购物车接口
# 移除或者修改
def edit_car_interface(username):
    user_dict = user_select(username)
    shop_car = user_dict['shop_car']  # {"小米": [30, 2999], "华为": [10, 4999]}
    list_shop_car = list(enumerate(shop_car, start=1))  # [(1, '小米'), (2, '华为')]
    if not shop_car:
        return False, '购物车是空的,请先添加购物车'
    while True:
        for i, v in enumerate(shop_car, start=1):
            number = shop_car[v][0]
            print(f'商品编号:{i}  --商品名:{v}  --商品数量:{number}')
        input_id = input('请输入要编辑的商品编号(q退出)>>>:').strip()
        if input_id == 'q':
            user_save(user_dict)
            return True, '购物车修改成功'
        if not input_id.isdigit():
            print('商品编号必须是数字,请重新选择!', end='\n\n')
            continue
        input_id = int(input_id)
        if input_id not in range(1, len(list_shop_car) + 1):
            print('输入的商品编号不存在,请重新输入!', end='\n\n')
            continue
        mode = input('请选择移除还是修改(r移除, a修改)>>>:').strip()
        shop_name = list_shop_car[input_id - 1][1]
        if mode == 'r':
            shop_car.pop(shop_name)
            user_save(user_dict)
            return True, f'商品{shop_name}移除成功'
        elif mode == 'a':
            while True:
                add_or_down = input('+ or - (q退出)>>>:').strip()
                if add_or_down == 'q':
                    print('返回编辑购物车页面自动保存数据', end='\n\n')
                    break
                if add_or_down == '+':
                    shop_car[shop_name][0] += 1
                    print(f'宝贝数量已+1,当前数量是:{shop_car[shop_name][0]}', end='\n\n')
                elif add_or_down == '-':
                    if shop_car[shop_name][0] == 1:
                        print('宝贝数量不能再-了', end='\n\n')
                        continue
                    shop_car[shop_name][0] -= 1
                    print(f'宝贝数量已-1,当前数量是:{shop_car[shop_name][0]}', end='\n\n')
                else:
                    print('请输入正确的指令', end='\n\n')
        else:
            print('请输入正确的指令', end='\n\n')


# 查看购物车接口
def check_car_interface(username):
    user_dict = user_select(username)
    return user_dict['shop_car']


# 清空购物车接口
def pay_car_interface(username):
    shop_list = shop_select()  # [["小米", 2999, 10], ["华为", 4999, 10]]
    user_dict = user_select(username)
    shop_car = user_dict['shop_car']  # {"小米": [30, 2999], "华为": [10, 4999]}
    if not shop_car:
        return False, '购物车是空的,请先添加购物车'
    money = 0
    for x, y in shop_car.items():
        for i in shop_list:
            if x in i:
                if y[0] > i[2]:
                    return False, f'商品{i[0]}库存不足,请先联系管理员补货或修改商品数量'
                money += y[0] * y[1]
                i[2] -= y[0]
                shop_save(shop_list)
    if user_dict['balance'] < money:
        return False, '账户余额不足'
    user_dict['balance'] -= money
    user_dict['shop_car'] = {}
    user_dict['flow'].append(f"{username}在{get_now_ftime()}清空了购物车,消费了{money}元")
    user_save(user_dict)
    logger.info(f"用户{username}清空了购物车,消费了{money}元")
    return True, f'清空购物车成功,本次消费{money}元'
