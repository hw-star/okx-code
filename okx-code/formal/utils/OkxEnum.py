# --*-- conding:utf-8 --*--
# @Time : 2024/11/21 下午2:27
# @Author : HWS
# @Email : xxxx@163.com
# @description : @TODO
# @Software : PyCharm

from enum import Enum, EnumMeta


class InstType(Enum):
    """
    金融类型.
    """
    MARGIN = "MARGIN"  # 保证金交易
    SWAP = "SWAP"  # 永续合约
    FUTURES = "FUTURES"  # 期货
    OPTION = "OPTION"  # 期权
    SPOT = "SPOT"  # 现货交易


class MgnMode(Enum):
    """
    保证金模式
    """
    cross = "cross"  # 全仓模式
    isolated = "isolated"  # 逐仓


class PosSide(Enum):
    """
    仓位方向
    """
    long = "long"
    short = "short"
    net = "net"


class OptType(Enum):
    """
    期权
    """
    CALL = "C"
    PUT = "P"


class CtType(Enum):
    """
    合约类型
    """
    LINEAR = "linear"
    INVERSE = "inverse"


class InstState(Enum):
    """
    交易工具状态
    """
    LIVE = "live"
    SUSPEND = "suspend"
    PREOPEN = "preopen"
    TEST = "test"


class OrderCategory(Enum):
    """
    订单种类
    """
    normal = "normal"  # 普通订单
    twap = "twap"
    adl = "adl"
    full_liquidation = "full_liquidation"
    partial_liquidation = "partial_liquidation"
    delivery = "delivery"
    ddh = "ddh"


class OrderExecType(Enum):
    """
    订单执行类型
    """
    TAKER = "T"  # 吃单
    MAKER = "M"  # 挂单


class OrderType(Enum):
    """
    订单类型
    """
    MARKET = "market"  # 市价订单
    LIMIT = "limit"  # 限价订单
    POST_ONLY = "post_only"  # 只挂单
    FOK = "fok"  # 全部成交/取消订单
    IOC = "ioc"  # 立即成交/取消订单
    OPTIMAL_LIMIT_IOC = "optimal_limit_ioc"  # 最优限价订单


class OrderSide(Enum):
    """
    订单方向
    """
    BUY = "buy"  # 买入
    SELL = "sell"  # 卖出


class OrderState(Enum):
    """
    订单状态
    """
    CANCELED = "canceled"  # 已取消
    LIVE = "live"  # 活跃中
    PARTIALLY_FILLED = "partially_filled"  # 部分成交
    FILLED = "filled"  # 已成交


class ListEnumMeta(EnumMeta):
    """
    枚举值列表实现了 __contains__ 方法,可直接用 in 运算符检查值是否属于某个枚举类
    """

    def __contains__(cls, item):
        return item in [v.value for v in cls.__members__.values()]


class OrderOp(Enum, metaclass=ListEnumMeta):
    """
    订单操作
    """
    ORDER = "order"  # 下单
    BATCH_ORDER = "batch-orders"  # 批量下单
    CANCEL = "cancel-order"  # 撤单
    BATCH_CANCEL = "batch-cancel-orders"  # 批量撤单
    AMEND = "amend-order"  # 修改订单
    BATCH_AMEND = "batch-amend-order"  # 批量修改订单


class TdMode(Enum, metaclass=ListEnumMeta):
    """
    交易模式
    """
    CASH = "cash"  # 现金
    ISOLATED = "isolated"  # 独立仓位
    CROSS = "cross"  # 全仓


class AccountConfigMode(Enum, metaclass=ListEnumMeta):
    """
    账户配置模式
    """
    CASH = 1  # 现金账户模式
    SINGLE_CCY_MARGIN = 2  # 单币种保证金模式
    MULTI_CCY_MARGIN = 3  # 多币种保证金模式
    PORTFOLIO_MARGIN = 4  # 投资组合保证金模式


class InstIdAll(Enum, metaclass=ListEnumMeta):
    """
    货币ID，待补充....
    """
    BTC_USDT = "BTC-USDT"  # 比特币
    PEPE_USDT = "PEPE-USDT"  # 佩佩币
    ETH_USDT = "ETH-USDT"  # 以太坊
    SOL_USDT = "SOL-USDT"  # sol
    DOGE_USDT = "DOGE-USDT"  # 狗狗币
    SHIB_USDT = "SHIB-USDT"  # 屎币
    ETHFI_USDT = "ETHFI-USDT"  # xxx


class RestChannelsAll(Enum, metaclass=ListEnumMeta):
    """
    RestAPI 通道ID
    """
    MARKET_PRICE = "mark-price"
    CINSTRUMENTS = "instruments"  # 获取交易产品基础信息
    DELIVERY_EXERCISE_HISTORY = "delivery-exercise-history"  # 获取3个月内的交割合约的交割记录和期权的行权记录
    OPEN_INTEREST = "open-interest"  # 获取持仓总量（单个交易产品）
    FUNDING_RATE = "funding-rate"  # 获取永续合约当前资金费率
    FUNDING_RATE_HISTORY = "funding-rate-history"  # 获取永续合约历史资金费率
    PRICE_LIMIT = "price-limit"  #查询单个交易产品的最高买价和最低卖价
    OPT_SUMMARY = "opt-summary"  # 查询期权详细信息
    ESTIMATED_PRICE = "estimated-price"  # 获取预估交割 / 行权价格
    DISCOUNT_RATE_INTEREST_FREE_QUOTA = "discount-rate-interest-free-quota"  # 获取免息额度和币种折算率等级
    TIME = "time"  # 获取系统时间
    MARK_PRICE = "mark-price"  # 获取标记价格
    POSITION_TIERS = "position-tiers"  # 获取衍生品仓位档位
    INTEREST_RATE_LOAN_QUOTA = "interest-rate-loan-quota"  # 获取市场借币杠杆利率和借币限额
    UNDERLYING = "underlying"  # 获取衍生品标的指数
    INSURANCE_FUND = "insurance-fund"  # 获取风险准备金余额
    CONVERT_CONTRACT_COIN = "convert-contract-coin"  # 张币转换
    INSTRUMENT_TICK_BANDS = "instrument-tick-bands"  # 获取期权价格梯度
    PREMIUM_HISTORY = "premium-history"  # 获取溢价历史数据
    INDEX_TICKERS = "index-tickers"  # 获取指数行情
    INDEX_CANDLES = "index-candles"  # 获取指数K线数据
    HISTORY_INDEX_CANDLES = "history-index-candles"  # 获取指数历史K线数据
    MARK_PRICE_CANDLES = "mark-price-candles"  # 获取标记价格K线数据
    HISTORY_MARK_PRICE_CANDLES = "mark-price-candles"  # 获取标记价格历史K线数据
    OPEN_ORACLE = "open-oracle"  # Oracle上链交易数据
    EXCHANGE_RATE = "exchange-rate"  # 获取法币汇率
    INDEX_COMPONENTS = "index-components"  # 获取指数成分数据



class WebSocketChannelsAll(Enum, metaclass=ListEnumMeta):
    """
    WebSocketAPI 通道ID
    """
    INSTRUMENTS = "instruments"  # 产品频道
    OPEN_INTEREST = "open-interest"  # 持仓总量频道
    FUNDING_RATE = "funding-rate"  # 资金费率频道
    PRICE_LIMIT = "price-limit"  # 限价频道
    OPT_SUMMARY = "opt-summary"  # 期权定价频道
    ESTIMATED_PRICE = "estimated-price"  # 预估交割 / 行权价格频道
    MARK_PRICE = "mark-price"  # 标记价格频道
    INDEX_TICKERS = "index-tickers"  # 指数行情频道
    MARK_PRICE_CANDLE3M = "mark-price-candle3M"  # 标记价格K线频道
    INDEX_CANDLE3M = "index-candle3M"  # 指数K线频道
