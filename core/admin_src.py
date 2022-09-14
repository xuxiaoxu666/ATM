# 管理员视图
from lib.commen import *
from interface import admin_interface
from core.user_src import is_login


def add_admin():
    while True:
        add_name = input('输入想要添加的管理员名>>>:').strip()
        cond, msg = admin_interface.add_admin_interface(is_login, add_name)
        if cond:
            print(msg, end='\n\n')
            exit_now()
            break
        else:
            print(msg, end='\n\n')


def lock_user():
    cond, msg = admin_interface.lock_user_interface(is_login)
    print(msg, end='\n\n')


def unlock_user():
    cond, msg = admin_interface.unlock_interface(is_login)
    print(msg, end='\n\n')


# 添加商品
def add_shop():
    shop_name = input('输入商品名>>>:').strip()
    shop_price = input('输入商品单价>>>:').strip()
    shop_kc = input('输入商品库存量>>>:').strip()
    cond, msg = admin_interface.add_shop_interface(is_login, shop_name, shop_price, shop_kc)
    print(msg, end='\n\n')


# 添加库存
def add_repertory():
    cond, msg = admin_interface.add_repertory_interface()
    print(msg, end='\n\n')


# 修改商品价格
def reset_price():
    cond, msg = admin_interface.reset_price_interface()
    print(msg, end='\n\n')


# 下架商品
def remove_shop():
    cond, msg = admin_interface.remove_interface()
    print(msg, end='\n\n')


def check_shop():
    shop_list = admin_interface.check_shop_interface()
    if not shop_list:
        print('商品为空, 请先添加商品!', end='\n\n')
    else:
        for i, v in enumerate(shop_list, start=1):
            print(f'{i}. 商品名:{v[0]}  --商品单价:{v[1]}  --商品库存:{v[2]}')


func_dict = {
    '1': add_admin,
    '2': lock_user,
    '3': unlock_user,
    '4': add_shop,
    '5': add_repertory,
    '6': reset_price,
    '7': remove_shop,
    '8': check_shop
}


def run():
    while True:
        print("""
        ====== Welcome to Admin view ======
        +           -1. 添加管理员          +
        +           -2. 锁定用户            +
        +           -3. 解锁用户            +
        +           -4. 添加商品            +
        +           -5. 添加库存            +
        +           -6. 修改商品价格         +
        +           -7. 移除商品            +
        +           -8. 查看商品            +
        +           -q. 退出管理员视图       +
        ================= end ================
        """)
        choice = input('请输入功能编号>>>:').strip()
        if choice == 'q':
            exit_now()
            break
        if choice in func_dict:
            func_dict.get(choice)()
        else:
            print('输入的功能编号不存在')
