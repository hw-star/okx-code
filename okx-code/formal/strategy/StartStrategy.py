# --*-- conding:utf-8 --*--
# @Time : 2024/11/22 上午10:28
# @Author : HWS
# @Email : xxxx@163.com
# @description : @TODO
# @Software : PyCharm

from formal.strategy.BaseStrategy import BaseStrategy

class StartStrategy(BaseStrategy):
    def __init__(self):
        super().__init__()

    def order_operation_div(self):
        """
        自己的策略
        :return: place_order_list, amend_order_list, cancel_order_list
        """