import pandas as pd
import ta
from src.utils.kline_loader import get_stock_hfq_daily

def calc_all_tech_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """计算全套技术指标 MA5/MA20/MA60 MACD RSI 成交量均线"""
    # 均线
    df["ma5"] = ta.trend.sma_indicator(df["收盘"], window=5)
    df["ma20"] = ta.trend.sma_indicator(df["收盘"], window=20)
    df["ma60"] = ta.trend.sma_indicator(df["收盘"], window=60)

    # MACD
    macd_obj = ta.trend.MACD(df["收盘"])
    df["macd_line"] = macd_obj.macd()
    df["macd_signal"] = macd_obj.macd_signal()

    # RSI6 短期强弱
    df["rsi6"] = ta.momentum.rsi(df["收盘"], window=6)

    # 成交量均线
    df["vol_ma5"] = ta.trend.sma_indicator(df["成交量"], window=5)
    return df

def get_box_support_resistance(df: pd.DataFrame, window: int = 60) -> dict:
    """获取近60日箱体高低点、20日线支撑、现价"""
    recent_data = df.tail(window)
    box_low = round(recent_data["最低"].min(), 2)
    box_high = round(recent_data["最高"].max(), 2)
    current_price = round(df["收盘"].iloc[-1], 2)
    ma20_price = round(df["ma20"].iloc[-1], 2)
    return {
        "box_low": box_low,
        "box_high": box_high,
        "ma20_support": ma20_price,
        "current_price": current_price
    }

def judge_price_trend(df: pd.DataFrame) -> str:
    """判断短期趋势：超买/超卖/多头/高位偏离均线/空头"""
    last_row = df.iloc[-1]
    rsi_val = last_row["rsi6"]
    price = last_row["收盘"]
    ma20 = last_row["ma20"]

    if rsi_val > 70:
        return "短期超买，存在回调回落压力，不适合现价重仓"
    elif rsi_val < 30:
        return "短期超卖，存在低吸布局机会"
    elif price > ma20 * 1.15:
        return "股价大幅偏离20日线，建议等待回踩支撑再买入"
    elif price > ma20:
        return "站稳20日均线，中期多头趋势，小幅回踩可加仓"
    else:
        return "股价跌破20日线，短期空头，观望为主"

def full_kline_analysis(stock_code: str) -> tuple[pd.DataFrame, dict, str]:
    """统一入口：一键获取K线、指标、箱体、趋势"""
    df_k = get_stock_hfq_daily(stock_code)
    df_tech = calc_all_tech_indicators(df_k)
    box_info = get_box_support_resistance(df_tech)
    trend_tip = judge_price_trend(df_tech)
    return df_tech, box_info, trend_tip
