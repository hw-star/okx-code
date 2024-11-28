# --*-- conding:utf-8 --*--
# @Time : 2024/11/21 下午3:10
# @Author : HWS
# @Email : xxxx@163.com
# @description : WebSocket方式获取数据（订阅频道）
# @Software : PyCharm

import asyncio
import datetime
import json
from typing import Callable, List, Dict
from okx.websocket.WsPublicAsync import WsPublicAsync
from formal.utils.OkxEnum import *
from formal import *
from formal.service.market_service.LinshiTest import LinshiTest

import logging
logger = logging.getLogger("WsPublic")
logger.setLevel(logging.WARNING)

class WebSocketClient:
    """
    根据WebSocketAPI 创建基础类
    """
    def __init__(self, url: str, callback: Callable):
        self.url = url
        self.callback = callback
        self.ws = None

    async def start(self):
        self.ws = WsPublicAsync(url=self.url)
        await self.ws.start()

    async def subscribe(self, args: List[Dict]):
        if self.ws:
            await self.ws.subscribe(args, self.callback)

    async def unsubscribe(self, args: List[Dict]):
        if self.ws:
            await self.ws.unsubscribe(args, self.callback)

    async def consume(self):
        if self.ws:
            try:
                await self.ws.consume()
            except Exception as e:
                await self.stop()

    async def stop(self):
        if self.ws:
            await self.ws.stop_sync()
            print("WebSocket connection closed.")


class WebSocketManager:
    """
    管理WebSocket客户端 程序启动类
    """
    def __init__(self, url: str, args: List[Dict]):
        self.client = WebSocketClient(url, self.public_callback)
        self.args = args

    # @staticmethod
    # def deal_time_ts_to_datetime(ts):
    #     return datetime.datetime.fromtimestamp(int(ts) / 1000)


    # @staticmethod
    # def handle_message(message):
    #     if isinstance(message, str):
    #         try:
    #             message = json.loads(message)
    #             return message
    #         except json.JSONDecodeError:
    #             print("Invalid JSON format:", message)

    # @staticmethod
    # def run_linshi(data_list, start):
    #     instId = data_list.get("instId")
    #     markPx = data_list.get("markPx")  # markPx
    #     ts = data_list.get("ts")
    #     div_ts = WebSocketManager.deal_time_ts_to_datetime(ts)
    #     sell_price = WebSocketManager.calculate_sell_price(0.1, 15)
    #     if float(markPx) >= sell_price:  # 市价卖出
    #         start.place_orders_market_sell("MEMEFI")
    #     print(f"okx消息： {instId}现价：{markPx}    时间：{div_ts}")

    # @staticmethod
    # def calculate_sell_price(buy_price, profit_percentage):
    #     """
    #     根据买入价格和目标收益百分比，计算卖出限价
    #
    #     :param buy_price: 买入价格（单位：USDT）
    #     :param profit_percentage: 目标收益百分比（例如15表示15%）
    #     :return: 卖出限价（单位：USDT）
    #     """
    #     sell_price = buy_price * (1 + profit_percentage / 100)
    #     return round(sell_price, 2)  # 保留两位小数


    @staticmethod
    def public_callback(message):
        """
        处理 WebSocket返回的消息
        :param message: 服务器推送所有消息
        :return:
        """
        print(message)

        # try:
        #     message = WebSocketManager.handle_message(message)
        #
        #     if "event" in message and message["event"] == "subscribe":
        #         print(f"订阅消息: {message}")
        #     elif "data" in message:
        #         data_list = message["data"]
        #         if isinstance(data_list, list) and len(data_list) > 0:
        #             start = LinshiTest()
        #             WebSocketManager.run_linshi(data_list[0], start)
        #             # instId = data_list[0].get("instId")
        #             # markPx = data_list[0].get("markPx")  # markPx
        #             # ts = data_list[0].get("ts")
        #             # div_ts = WebSocketManager.deal_time_ts_to_datetime(ts)
        #             # print(f"okx消息： {instId}现价：{markPx}    时间：{div_ts}")
        #         else:
        #             print("The '数据非 list/empty.")
        #     else:
        #         print(f"未知消息格式: {message}")
        # except json.JSONDecodeError:
        #     print(f"处理json失败: {message}")
        # except Exception as e:
        #     print(f"bug: {e}")



    async def run(self):
        await self.client.start()
        await self.client.subscribe(self.args)

        try:
            # websocket保持通信
            while True:
                await asyncio.sleep(1)
        except Exception as e:
            await self.client.stop()

    async def run_forever(self):
        # 网络断开，每5分钟启动重连
        while True:
            try:
                await self.run()
            except queue.Empty:
                pass
            except Exception as e:
                print("net error. Reconnecting in 5 seconds...")
                await asyncio.sleep(5)

# if __name__ == '__main__':
#     try:
#         url = "wss://ws.okx.com:8443/ws/v5/public"
#         args = [
#             {"channel": WebSocketChannelsAll.MARK_PRICE.value, "instId": "MEMEFI-USDT"}
#         ]
#         manager = WebSocketManager(url, args)
#         asyncio.run(manager.run_forever())
#     except KeyboardInterrupt:
#         print("程序已手动终止！")
#     except Exception as e:
#         print(f"程序发生错误: {e}")
