import json

from tradingview_ta import *

from con import Controller

Symbols = ["FX_IDC:EURUSD", "FX_IDC:GBPUSD", "FX_IDC:AUDUSD", "FX_IDC:NZDUSD", "FX_IDC:USDCHF", "FX_IDC:USDJPY",
           "FX_IDC:USDCAD", "FX_IDC:EURJPY", "FX_IDC:GBPJPY", "FX_IDC:AUDJPY", "FX_IDC:NZDJPY", "FX_IDC:CHFJPY",
           "FX_IDC:CADJPY", "FX_IDC:EURGBP", "FX_IDC:EURAUD", "FX_IDC:EURNZD", "FX_IDC:EURCHF", "FX_IDC:EURCAD",
           "FX_IDC:GBPAUD", "FX_IDC:GBPNZD", "FX_IDC:GBPCHF", "FX_IDC:GBPCAD", "FX_IDC:AUDNZD", "FX_IDC:AUDCHF",
           "FX_IDC:AUDCAD", "FX_IDC:NZDCHF", "FX_IDC:NZDCAD", "FX_IDC:CADCHF"]

Intervals = {Interval.INTERVAL_1_DAY, Interval.INTERVAL_4_HOURS, Interval.INTERVAL_1_HOUR, Interval.INTERVAL_15_MINUTES}
Ratings = {"NEUTRAL": 0, "BUY": 1, "STRONG_BUY": 2, "SELL": -1, "STRONG_SELL": -2}

con = Controller()


def get_price(symbol):
    if symbol == "XAUUSD":
        handle = TA_Handler(
            symbol="GOLD",
            screener="cfd",
            exchange="TVC",
            interval=Interval.INTERVAL_1_MINUTE
        )
    elif symbol == "BTCUSD":
        handle = TA_Handler(
            symbol="BTCUSDT",
            screener="crypto",
            exchange="BINANCE",
            interval=Interval.INTERVAL_1_MINUTE
        )
    else:
        handle = TA_Handler(
            symbol=symbol,
            screener="forex",
            exchange="FX_IDC",
            interval=Interval.INTERVAL_1_MINUTE
        )
    analysis = handle.get_analysis()
    return analysis.indicators["close"]


def upsert(symbol, timeframe, analysis):
    ma = Ratings[analysis.moving_averages['RECOMMENDATION']]
    os = Ratings[analysis.oscillators['RECOMMENDATION']]
    con.upsert_ta(symbol, timeframe, ma, os)
    if timeframe == Interval.INTERVAL_15_MINUTES:
        con.update_signal(symbol, analysis.indicators["close"])
    if timeframe == Interval.INTERVAL_1_HOUR:
        con.upsert_indicator(symbol, analysis.indicators["open"], analysis.indicators["high"], analysis.indicators["low"],
                             analysis.indicators["close"], analysis.indicators["volume"], analysis.indicators["W.R"], analysis.indicators["EMA20"])


def fetch():
    for interval in Intervals:
        data = get_multiple_analysis(screener="forex", interval=interval, symbols=Symbols)
        for symbol in Symbols:
            analysis = data[symbol]
            upsert(analysis.symbol, interval, analysis)
        handle = TA_Handler(
            symbol="GOLD",
            screener="cfd",
            exchange="TVC",
            interval=interval
        )
        analysis = handle.get_analysis()
        upsert("XAUUSD", interval, analysis)
        handle = TA_Handler(
            symbol="BTCUSDT",
            screener="crypto",
            exchange="BINANCE",
            interval=interval
        )
        analysis = handle.get_analysis()
        upsert("BTCUSD", interval, analysis)
        handle = TA_Handler(
            symbol="ETHUSDT",
            screener="crypto",
            exchange="BINANCE",
            interval=interval
        )
        analysis = handle.get_analysis()
        upsert("ETHUSD", interval, analysis)
    tas = con.get_tas()
    print(json.dumps(tas))


def find_signals():
    tas = con.get_tas()
    for ta in tas:
        symbol = ta[0]
        contrarian = ta[1]
        trend = ta[2]
        entry = ta[3]
        open1, high1, low1, close1, volume1, wpr1, ema1 = con.get_indicator(symbol, 1)
        open2, high2, low2, close2, volume2, wpr2, ema2 = con.get_indicator(symbol, 2)
        divergence = (high1 - low1 > (high2 - low2) * 1.1 and volume1 * 1.1 < volume2) or ((high1 - low1) * 1.1 < high2 - low2 and volume1 > volume2 * 1.1)
        if close1 > open1 and close2 < open2 and divergence:
            entry += 1
        if close1 < open1 and close2 > open2 and divergence:
            entry += -1
        if low1 < ema1 < close1 and wpr2 < -55 and -45 < wpr1:
            entry += 1
        if high1 > ema1 > close1 and wpr2 > -45 and -55 > wpr1:
            entry += -1
        if contrarian > 0 and trend > 1 and entry > 5:
            price = get_price(symbol)
            con.insert_signal(0, symbol, 1, 1, price)
            print("Signal " + symbol + " contrarian:" + str(contrarian) + " trend:" + str(trend) + " entry:" + str(entry))
        if contrarian < 0 and trend < -1 and entry < -5:
            price = get_price(symbol)
            con.insert_signal(0, symbol, -1, 1, price)
            print("Signal " + symbol + " contrarian:" + str(contrarian) + " trend:" + str(trend) + " entry:" + str(entry))
    signals = con.get_signals_delay()
    with open('public/signals.json', 'w') as file:
        json.dump(signals, file)


if __name__ == "__main__":
    fetch()
    con.calculate_contrarian()
    con.update_signals_mm()
    find_signals()
