def calculate_buy_zone(box_info: dict) -> dict:
    """
    根据箱体数据计算三层买入区间+止损
    box_info 来自 tech_calc.get_box_support_resistance
    """
    box_low = box_info["box_low"]
    box_high = box_info["box_high"]
    ma20 = box_info["ma20_support"]
    current = box_info["current_price"]
    box_mid = round((box_low + box_high) / 2, 2)

    # 1. 长线安全底仓区：箱体下沿~箱体中轨
    safe_zone_low = round(min(ma20, box_mid * 0.96), 2)
    safe_zone_high = box_mid

    # 2. 中性加仓区间：箱体中轨 ~ 箱体上沿93%位置
    add_zone_low = safe_zone_high
    add_zone_high = round(box_high * 0.93, 2)

    # 3. 短线突破买点：站稳箱体上沿才可介入
    breakout_buy = box_high

    # 统一止损：买入价下跌7%强制减仓
    stop_loss_ratio = 0.93

    return {
        "current_price": current,
        "box_range": f"{box_low} ~ {box_high}",
        "ma20_support": ma20,
        "safe_buy_zone": f"{safe_zone_low} ~ {safe_zone_high} 【长线底仓，优先低吸】",
        "add_position_zone": f"{add_zone_low} ~ {add_zone_high} 【企稳后加仓区间】",
        "breakout_buy_point": f"{breakout_buy} 【放量突破箱体再参与，短线风险高】",
        "stop_loss_rule": "入场价格 × 0.93，浮亏7%执行减仓止损"
    }
