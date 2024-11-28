# --*-- conding:utf-8 --*--
# @Time : 2024/11/22 上午9:55
# @Author : HWS
# @Email : xxxx@163.com
# @description : 暂时使用-买入，卖出
# @Software : PyCharm

from okx.Trade import TradeAPI
from okx.Account import AccountAPI
from formal.config import *
import time

class LinshiTest():
    trade_api: TradeAPI
    account_api: AccountAPI

    def __init__(self, api_key=API_KEY, api_key_secret=API_KEY_SECRET, api_passphrase=API_PASSPHRASE,
                 is_paper_trading: bool = IS_PAPER_TRADING):
        self.trade_api = TradeAPI(api_key=api_key, api_secret_key=api_key_secret, passphrase=api_passphrase,
                                  flag='0' if not is_paper_trading else '1', debug=False)
        self.account_api = AccountAPI(api_key=api_key, api_secret_key=api_key_secret, passphrase=api_passphrase,
                                      flag='0' if not is_paper_trading else '1', debug=False)


    def place_orders_limit(self, ccy, all_pay, price):
        """
        限价买入

        :param ccy: 货币
        :param all_pay: 总金额
        :param price: 单价
        :return:
        """
        max_retries = 11  # 最大重试次数，防止死循环
        retry_count = 0

        while True:
            try:
                result = self.trade_api.place_order(
                    instId=ccy + "-USDT",  # 交易对
                    tdMode="cash",  # 现货交易
                    side="buy",  # 买入
                    ordType="limit",  # 限价单
                    px=str(price),  # 限价
                    sz=str(round(all_pay / price, 6)),  # 购买数量，精度为 6 位小数
                )

                print(f"买入尝试结果：{result}")

                if result['code'] == "0":
                    print(f"成功买入，时间是：{result['data'][0]['ts']}")
                    break  # 退出循环
                else:
                    print("买入失败，重新尝试...")

            except Exception as e:
                print(f"发生错误：{e}")

            retry_count += 1
            if retry_count >= max_retries:
                print("达到最大重试次数，停止买入操作")
                break

            # 添加延迟，避免短时间内频繁请求
            time.sleep(0.5)

    def place_orders_algo(self):
        result = self.trade_api.place_order(
            instId="",
            tdMode="cash",
            side="buy",
            ordType="trigger",
            sz="100",
            tpTriggerPx="10000",
            tpTriggerPxType="last"

        )
        print(f"买入：{result}")
        if result['code'] == "0":
            print(f"成功买入，时间是：{result['data'][0]['ts']}")
        else:
            print("买入失败")

    def place_orders_limit_sell(self, ccy, price):
        """
        限价卖出

        :param ccy: 货币
        :param price: 单价
        :return:
        """
        amount_to_sell: float  # 卖出数量
        max_retries = 11  # 最大重试次数
        retry_count = 0

        while True:
            try:
                res = self.account_api.get_account_balance(
                    ccy=ccy
                )
                amount_to_sell = res['data'][0]['details'][0]['availBal']
                # 发起限价卖出请求
                result = self.trade_api.place_order(
                    instId=ccy + "-USDT",  # 交易对
                    tdMode="cash",  # 现货交易
                    side="sell",  # 卖出
                    ordType="limit",  # 限价单
                    px=str(price),  # 限价
                    sz=str(amount_to_sell),  # 卖出数量
                )

                print(f"卖出尝试结果：{result}")

                if result['code'] == "0":
                    print(f"成功卖出，时间是：{result['data'][0]['ts']}")
                    break  # 退出循环
                else:
                    print("卖出失败，重新尝试...")

            except Exception as e:
                print(f"发生错误：{e}")

            retry_count += 1
            if retry_count >= max_retries:
                print("达到最大重试次数，停止卖出操作")
                break

            # 添加延迟，避免频繁调用
            time.sleep(0.5)

    def place_orders_market_sell(self, ccy):
        amount_to_sell: float  # 卖出数量
        max_retries = 11  # 最大重试次数
        retry_count = 0

        while True:
            try:
                res = self.account_api.get_account_balance(
                    ccy=ccy
                )
                if (res['data'][0]['details']) == []:
                    print(f"你没有 {ccy} 币")
                    break
                amount_to_sell = res['data'][0]['details'][0]['availBal']
                # 发起市价卖出请求
                result = self.trade_api.place_order(
                    instId=ccy + "-USDT",  # 交易对
                    tdMode="cash",  # 现货交易
                    side="sell",  # 卖出
                    ordType="market",  # 市价单
                    sz=str(amount_to_sell),  # 卖出数量
                )

                print(f"卖出尝试结果：{result}")

                if result['code'] == "0":
                    print(f"成功卖出，时间是：{result['data'][0]['ts']}")
                    break  # 退出循环
                else:
                    print("卖出失败，重新尝试...")

            except Exception as e:
                print(f"发生错误：{e}")

            retry_count += 1
            if retry_count >= max_retries:
                print("达到最大重试次数，停止卖出操作")
                break

            # 添加延迟，避免频繁调用
            time.sleep(0.5)


if __name__ == "__main__":
    start = LinshiTest()
    start.place_orders_market_sell("SOL")
    #start.place_orders_limit("SOL", 258.11, 258.11)
