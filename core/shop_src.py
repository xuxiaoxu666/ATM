# 购物视图层

from lib.commen import exit_now
from interface import shop_interface
from core.user_src import is_login


def add_shop_car():
    cond, msg = shop_interface.add_car_interface(is_login)
    print(msg, end='\n\n')


def edit_car():
    con, msg = shop_interface.edit_car_interface(is_login)
    print(msg, end='\n\n')


def check_car():
    shop_car = shop_interface.check_car_interface(is_login)
    if not shop_car:
        print('购物车是空的,请先添加购物车')
        return
    money = 0
    for i, v in shop_car.items():
        money += v[0] * v[1]
        print(f'商品名:{i}  --商品数量:{v[0]}  --商品单价:{v[1]}')
    print(f'                                          总计{money}元')
    exit_now()


def pay_car():
    cond, msg = shop_interface.pay_car_interface(is_login)
    if cond:
        print(msg)
        exit_now()
    else:
        print(msg)


func_dict = {
    '1': add_shop_car,
    '2': edit_car,
    '3': check_car,
    '4': pay_car,
}


def run():
    while True:
        print("""
        ======== Welcome come to shop =======
        +           -1. 添加购物车            +
        +           -2. 编辑购物车            +
        +           -3. 查看购物车            +
        +           -4. 清空购物车            +
        +           -q. 返回主页面            +
        ================= end ================
        """)
        choice = input('请输入要执行的功能编号>>>:').strip()
        if choice == 'q':
            exit_now()
            return
        if choice in func_dict:
            func_dict.get(choice)()
        else:
            print('输入的功能编号不存在,请重新输入', end='\n\n')
