# 银行相关接口
from db.db_handle import user_select, user_save
from lib.commen import money_is_correct, get_now_ftime, get_log

logger = get_log('银行相关日志')


# 查看余额接口
def check_balance_interface(username):
    balance = user_select(username)['balance']
    return True, f"""
            姓名:{username}
            账户余额:{balance}元
    """


# 还款接口
def top_up_interface(username, money):
    money = money_is_correct(money)
    if not money:
        return False, '输入的金额不合法,请重新输入!'
    print(money)
    money = float(money)
    user_dict = user_select(username)
    user_dict['balance'] += money
    user_dict['flow'].append(f'用户{username}在{get_now_ftime()}还款{money}元')
    user_save(user_dict)
    logger.info(f'用户{username}还款{money}元成功')
    return True, f"还款成功,当前账户余额{user_dict['balance']}元"


# 提现接口
def withdraw_interface(username, money):
    money = money_is_correct(money)
    if not money:
        return False, '输入的金额不合法,请重新输入!'
    money = float(money)
    from conf.settings import CHARGE
    user_dict = user_select(username)
    if user_dict['balance'] < money * (1 + CHARGE):
        return False, '当前账户余额不足,自动返回上一级菜单!'
    user_dict['balance'] -= money * (1 + CHARGE)
    user_dict['flow'].append(f'用户{username}在{get_now_ftime()}提现{money}元')
    user_save(user_dict)
    logger.info(f'用户{username}提现{money}元成功')
    return True, f"提现成功,手续费{money * CHARGE}当前账户余额{user_dict['balance']}元"


# 转账接口
def transfer_interface(username, to_username, money):
    to_user_dict = user_select(to_username)
    if not to_user_dict:
        return False, '转账用户名不存在,请重新输入!'
    money = money_is_correct(money)
    if not money:
        return False, '输入金额不合法,请重新输入'
    money = float(money)
    user_dict = user_select(username)
    if user_dict['balance'] < money:
        return False, '您的余额不足,无法完成转账'
    user_dict['balance'] -= money
    user_dict['flow'].append(f'{username}在{get_now_ftime()}给用户{to_username}转账{money}元')
    user_save(user_dict)
    logger.info(f'{username}给用户{to_username}转账{money}元')
    to_user_dict['balance'] += money
    to_user_dict['flow'].append(f'{to_username}在{get_now_ftime()}收到用户{username}转账{money}元')
    user_save(to_user_dict)
    logger.info(f'{to_username}收到用户{username}转账{money}元')
    return True, f"转账成功,当前账户余额{user_dict['balance']}元"


# 查看流水接口
def check_flow_interface(username):
    return user_select(username)['flow']
