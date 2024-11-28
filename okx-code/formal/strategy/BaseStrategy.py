# --*-- conding:utf-8 --*--
# @Time : 2024/11/20 下午12:56
# @Author : HWS
# @Email : xxxx@163.com
# @description : @TODO
# @Software : PyCharm

import time
import traceback
from abc import ABC, abstractmethod
from typing import List, Dict, Tuple
import logging
from formal.config import *

from okx.Account import AccountAPI
from okx.Trade import TradeAPI
from okx.Status import StatusAPI
from formal.utils.OkxEnum import *
import asyncio

from formal.service.market_service.WsMarketService import WebSocketManager
from formal.service.market_service.RESTMarketService import RESTMarketService
from formal.strategy.params.ParamsLoader import ParamsLoader

class BaseStrategy(ABC):
    trade_api: TradeAPI
    status_api: StatusAPI
    account_api: AccountAPI

    def __init__(self, api_key=API_KEY, api_key_secret=API_KEY_SECRET, api_passphrase=API_PASSPHRASE,
                 is_paper_trading: bool = IS_PAPER_TRADING):
        self.trade_api = TradeAPI(api_key=api_key, api_secret_key=api_key_secret, passphrase=api_passphrase,
                                  flag='0' if not is_paper_trading else '1', debug=False)
        self.status_api = StatusAPI(flag='0' if not is_paper_trading else '1', debug=False)
        self.account_api = AccountAPI(api_key=api_key, api_secret_key=api_key_secret, passphrase=api_passphrase,
                                      flag='0' if not is_paper_trading else '1', debug=False)
        self.args = [
            {"channel": WebSocketChannelsAll.MARK_PRICE.value, "instId": "MEMEFI-USDT"}
        ]
        self.mds = WebSocketManager(
            url="wss://ws.okx.com:8443/ws/v5/public?brokerId=9999" if is_paper_trading
            else "wss://ws.okx.com:8443/ws/v5/public", args=self.args
        )
        self.rest_mds = RESTMarketService(is_paper_trading)
        # self.oms = WssOrderService(
        #     url="wss://ws.okx.com:8443/ws/v5/private?brokerId=9999" if is_paper_trading
        #     else "wss://ws.okx.com:8443/ws/v5/private")
        self.params_loader = ParamsLoader()

    @abstractmethod
    def order_operation_div(self):
        pass

    def place_orders(self, order_request_list):
        """
        # 可增加部分规则
        # order_data_list = []
        # for order_request in order_request_list:
        #     strategy_order = StrategyOrder(
        #         inst_id=order_request.inst_id, ord_type=order_request.ord_type, side=order_request.side,
        #         size=order_request.size,
        #         price=order_request.price,
        #         client_order_id=order_request.client_order_id,
        #         strategy_order_status=StrategyOrderStatus.SENT, tgt_ccy=order_request.tgt_ccy
        #     )
        #     order_data_list.append(order_request.to_dict())
        #     print(f"PLACE ORDER {order_request.ord_type.value} {order_request.side.value} {order_request.inst_id} "
        #           f"{order_request.size} @ {order_request.price}")
        #     if len(order_data_list) >= 20:
        #         self._place_orders(order_data_list)
        #         order_data_list = []
        # if order_data_list:
        #     self._place_orders(order_data_list)
        """
        if order_request_list:
            self._place_orders(order_request_list[0])

    def _place_orders(self, order_data_list: List[Dict]):
        """
        下订单
        """
        result = self.trade_api.place_multiple_orders(order_data_list)
        print(result)
        time.sleep(2)
        if result["code"] == '1':
            for order_data in order_data_list:
                client_order_id = order_data['clOrdId']
                # 交易成功  数据处理位置
        else:
            data = result['data']
            for single_order_data in data:
                client_order_id = single_order_data["clOrdId"]
                # 交易失败  数据处理位置

    def amend_orders(self, order_request_list):
        """
        类似买入  可增加部分规则
        """
        if order_request_list:
            self._amend_orders(order_request_list[0])

    def _amend_orders(self, order_data_list: List[Dict]):
        """
        修改订单 多个
        """
        result = self.trade_api.amend_multiple_orders(order_data_list)


    def cancel_orders(self, order_request_list):
        """
        取消订单 可增加部分规则
        """
        if order_request_list:
            self._cancel_orders(order_request_list[0])

    def _cancel_orders(self, order_data_list: List[Dict]):
        """
        取消订单 多个
        """
        result = self.trade_api.cancel_multiple_orders(order_data_list)


    def _health_check(self) -> bool:
        try:
            # 订单检查
            pass
        except ValueError:
            return False
        """
        其他检查 不通过 return False    
        """
        return True

    def _update_strategy_order_status(self):
        # 订单更新
        pass


    def get_params(self):
        """
        获取strategy.params 下的参数
        :return:
        """
        self.params_loader.load_params()


    def risk_summary(self):
        # 风险检测
        pass

    def check_status(self):
        status_response = self.status_api.status("ongoing")
        if status_response.get("data"):
            print(status_response.get("data"))
            return False
        return True

    def _set_account_config(self):
        account_config = self.account_api.get_account_config()
        if account_config.get("code") == '0':
            self._account_mode = AccountConfigMode(int(account_config.get("data")[0]['acctLv']))

    def _run_exchange_connection(self):
        asyncio.run(self.mds.run_forever())


    def run(self):
        self._set_account_config()  # 可选配
        self._run_exchange_connection()
        while 1:
            try:
                exchange_normal = self.check_status()
                if not exchange_normal:
                    raise ValueError("There is a ongoing maintenance in OKX.")
                self.get_params()
                result = self._health_check()
                self.risk_summary()
                if not result:
                    print(f"Health Check result is {result}")
                    time.sleep(5)
                    continue
                # summary
                self._update_strategy_order_status()
                place_order_list, amend_order_list, cancel_order_list = self.order_operation_div()
                # print(place_order_list)
                # print(amend_order_list)
                # print(cancel_order_list)

                self.place_orders(place_order_list)
                self.amend_orders(amend_order_list)
                self.cancel_orders(cancel_order_list)

                time.sleep(1)
            except:
                print(traceback.format_exc())
                time.sleep(20)