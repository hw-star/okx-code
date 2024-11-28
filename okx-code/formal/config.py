# --*-- conding:utf-8 --*--
# @Time : 2024/11/20 下午12:16
# @Author : HWS
# @Email : xxxx@163.com
# @description : 配置文件：配置账号API相关信息，配置策略链接
# @Software : PyCharm

import os


# OKX API信息
# api_key
API_KEY = ""
# api_secret
API_KEY_SECRET = ""
# api_passphrase
API_PASSPHRASE = ""
# 是否模拟交易  true：flag：1   false：flag：0
IS_PAPER_TRADING = False


PARAMS_PATH = os.path.abspath(os.path.dirname(__file__) + "/basics.yaml")
