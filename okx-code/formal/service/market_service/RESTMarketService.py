# --*-- conding:utf-8 --*--
# @Time : 2024/11/20 下午3:48
# @Author : HWS
# @Email : xxxx@163.com
# @description : Rest方式获取数据
# @Software : PyCharm

from formal.config import *
import logging
import threading
import time
import traceback

from okx.exceptions import OkxAPIException, OkxParamsException, OkxRequestException
from okx.MarketData import MarketAPI
from okx.PublicData import PublicAPI
from formal.service.market_service.model.Tickers import *
from formal.service.market_service.model.MarkPx import *
from formal import *


class RESTMarketService:
    def __init__(self, is_paper_trading=IS_PAPER_TRADING):
        super().__init__()
        self.market_api = MarketAPI(flag='0' if not is_paper_trading else '1', debug=False)
        self.public_api = PublicAPI(flag='0' if not is_paper_trading else '1', debug=False)


    def run(self) -> None:
        while 1:
            try:
                json_response = self.market_api.get_tickers(instType=InstType.SPOT.value)
                tickers: Tickers = tickers_container[0]
                tickers.update_from_json(json_response)
                mark_px_cache: MarkPxCache = mark_px_container[0]
                json_response = self.public_api.get_mark_price(instType=InstType.SWAP.value)
                mark_px_cache.update_from_json(json_response)
                time.sleep(2)
                print(tickers_container, mark_px_container)
            except (OkxAPIException, OkxParamsException, OkxRequestException):
                logging.warning(traceback.format_exc())
                time.sleep(5)
            except Exception as e:
                print(e)

"""
测试代码

if __name__ == "__main__":
    rest_mds = RESTMarketService()
    rest_mds.start()
"""
