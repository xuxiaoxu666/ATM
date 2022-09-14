from interface import user_interface, bank_interface
from lib.commen import *

is_login = ''
is_admin = None


# 主视图层
def register():
    while True:
        username = input('输入注册用户名>>>:').strip()
        if username == 'q':
            exit_now()
            return
        password = input('输入密码>>>:').strip()
        if password == 'q':
            exit_now()
            return
        re_password = input('确认密码>>>:').strip()
        code = random_code()
        print(f'随机验证码:{code}(不区分大小写)')
        input_code = input('请输入随机验证码>>>:').strip()
        if code == 'q':
            exit_now()
            return
        if password != re_password:
            print('两次输入密码不一致,请重新输入!')
            continue
        if not input_code.upper() == code.upper():
            print('随机验证码错误，请重新输入!')
            continue
        cond, msg = user_interface.register_interface(username, password)
        if cond:
            print(msg, end='\n\n')
            break
        else:
            print(msg, end='\n\n')


def login():
    count = 0
    while count < 5:
        username = input('请输入登录用户名>>>:').strip()
        if username == 'q':
            return
        password = input('请输入登录密码>>>:').strip()
        cond, msg = user_interface.login_interface(username, password)
        if cond:
            global is_login, is_admin
            is_login = cond[0]
            is_admin = cond[1]
            print(msg, end='\n\n')
            exit_now()
            return
        else:
            print(msg, end='\n\n')
        count += 1
        if 2 < count < 5:
            # 当输入错误三次 必须校验验证码才可以继续输入
            while True:
                code = random_code()
                print(f'随机验证码:{code}(不区分大小写)')
                input_code = input('请输入随机验证码>>>:').strip()
                if input_code.upper() != code.upper():
                    print('验证码错误', end='\n\n')
                else:
                    print('验证成功,请继续输入(五次自动退出登录界面)!', end='\n\n')
                    break
        if count == 5:
            print('输错次数已达上限，请稍后再来尝试!!!', end='\n\n')
            exit_now()


@login_auth('user')
def check_balance():
    cond, msg = bank_interface.check_balance_interface(is_login)
    print(msg, end='\n\n')
    exit_now()


@login_auth('user')
# 还款
def top_up():
    money = input('请输入还款金额>>>:').strip()
    if money == 'q':
        exit_now()
        return
    cond, msg = bank_interface.top_up_interface(is_login, money)
    if cond:
        print(msg, end='\n\n')
        exit_now()
    else:
        print(msg, end='\n\n')


@login_auth('user')
# 提现
def withdraw():
    while True:
        money = input('请输入提现金额>>>:').strip()
        if money == 'q':
            exit_now()
            return
        cond, msg = bank_interface.withdraw_interface(is_login, money)
        if cond:
            print(msg, end='\n\n')
            exit_now()
            return
        else:
            print(msg, end='\n\n')


@login_auth('user')
def transfer():
    while True:
        to_username = input('请输入要转账的用户名>>>:').strip()
        if to_username == 'q':
            exit_now()
            return
        money = input('请输入转账金额>>>:').strip()
        if to_username == is_login:
            print('不能自己给自己转账,请重新输入!', end='\n\n')
            continue
        cond, msg = bank_interface.transfer_interface(is_login, to_username, money)
        if cond:
            print(msg, end='\n\n')
            exit_now()
            return
        else:
            print(msg, end='\n\n')


@login_auth('user')
def check_flow():
    flow_list = bank_interface.check_flow_interface(is_login)
    for i, v in enumerate(flow_list, start=1):
        print(f"{i}. {v}")
    exit_now()


@login_auth('user')
def shop():
    from core.shop_src import run
    run()


@login_auth('admin')
def admin():
    from core.admin_src import run
    run()


func_dict = {
    '1': register,
    '2': login,
    '3': check_balance,
    '4': top_up,
    '5': withdraw,
    '6': transfer,
    '7': check_flow,
    '8': shop,
    '9': admin,

}


def run():
    while True:
        print("""
        ====== Welcome to ATM and Shop ======
        +           -1. 注册功能              +
        +           -2. 登录功能              +
        +           -3. 查看余额              +
        +           -4. 还款功能              +
        +           -5. 提现功能              +
        +           -6. 转账功能              +
        +           -7. 查看流水              +
        +           -8. 购物功能              +
        +           -9. 管理功能              +
        ================= end ================
        """)
        choice = input('请输入想要执行的功能编号>>>:').strip()
        if choice in func_dict:
            func_dict.get(choice)()
        else:
            print('输入的功能编号不存在')
