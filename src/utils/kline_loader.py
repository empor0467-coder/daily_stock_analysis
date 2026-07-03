import akshare as ak
import pandas as pd

def get_stock_hfq_daily(stock_code: str, bar_count: int = 120) -> pd.DataFrame:
    """
    获取A股前复权日K数据
    :param stock_code: A股代码 如603505
    :param bar_count: 获取K线根数，默认120根
    :return: 清洗好的K线DataFrame
    """
    df_raw = ak.stock_zh_a_hist(
        symbol=stock_code,
        period="daily",
        adjust="hfq"
    )
    # 只保留核心字段
    df = df_raw[["日期", "开盘", "最高", "最低", "收盘", "成交量"]].copy()
    df = df.tail(bar_count).reset_index(drop=True)
    return df
