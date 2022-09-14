# 数据处理层

import os
import json
from conf.settings import USER_DB_DIR, SHOP_DB_DIR


# 查看用户数据
def user_select(username):
    user_db_path = os.path.join(USER_DB_DIR, f"{username}.json")
    if os.path.exists(user_db_path):
        with open(user_db_path, 'r', encoding='utf8') as f:
            return json.load(f)


# 保存用户数据
def user_save(user_dict):
    user_db_path = os.path.join(USER_DB_DIR, f"{user_dict['username']}.json")
    with open(user_db_path, 'w', encoding='utf8') as f:
        json.dump(user_dict, f, ensure_ascii=False)


# 查看商品信息
def shop_select():
    shop_path = os.path.join(SHOP_DB_DIR, 'shop_db.json')
    if not os.path.exists(shop_path):  # 如果商品文件不存在 就创建文件并写入一个空列表
        with open(shop_path, 'w', encoding='utf8') as f:
            json.dump([], f, ensure_ascii=False)
            return []
    with open(shop_path, 'r', encoding='utf8') as f:
        return json.load(f)


# 保存商品
def shop_save(shop_list):
    shop_path = os.path.join(SHOP_DB_DIR, 'shop_db.json')
    with open(shop_path, 'w', encoding='utf8') as f:
        json.dump(shop_list, f, ensure_ascii=False)
