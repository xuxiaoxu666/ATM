import os
import sys

# 添加到解释器环境变量
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

#  启动项目
if __name__ == '__main__':
    from core import user_src

    user_src.run()
