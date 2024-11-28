# --*-- conding:utf-8 --*--
# @Time : 2024/11/20 下午12:13
# @Author : HWS
# @Email : xxxx@163.com
# @description : 通过config.py的链接读取basics.yaml的策略配置信息
# @Software : PyCharm

import traceback
import yaml

from formal.config import PARAMS_PATH


class ParamsLoader:
    def __init__(self):
        self.params = dict()
        self._inited = False

    def load_params(self) -> None:
        """
        读取basics.yaml的策略信息
        :return: 字典（两层）
        """
        try:
            with open(PARAMS_PATH, 'r') as file:
                params = yaml.safe_load(file)
            self.params = params
        except Exception as e:
            print(traceback.format_exc())

    def get_strategy_params(self, *args):
        """
        获取策略参数
        :param args: 单一/无
        :return: 格式：字典
        """
        if not self._inited:
            self.load_params()
        strategy_params = self.params.get("strategy")
        for arg in args:
            strategy_params = strategy_params.get(arg)
            if strategy_params is None:
                return
        return strategy_params


"""
测试代码

if __name__ == "__main__":
    loader = ParamsLoader()
    loader.load_params()
    strategy_params = loader.get_strategy_params()
    print(strategy_params)
"""